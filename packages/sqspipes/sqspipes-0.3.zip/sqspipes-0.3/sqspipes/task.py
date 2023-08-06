import json
import random
import time
import traceback
import uuid

import boto3
from botocore.errorfactory import ClientError
from multiprocessing import Lock

from .utils.task_pool import TaskPool, TaskError, TaskCallback


class EmptyTaskOutput(object):
    pass


class TaskRunner(object):

    def __init__(self, fn, in_queue_names, config):
        self.fn = fn
        self.in_queue_names = in_queue_names
        self.results = []
        self._result_mutex = Lock()
        self.out_queues = []
        self._out_queue_names = None

        self.domain = config['domain']
        self.name = config['name']
        self.fifo = config['fifo']
        self.aws_config = config['aws_config']
        self.workers = config.get('workers', 1)
        self.priority_levels = list(reversed(range(config.get('priorities', 1))))
        self.final = config.get('final', False)
        self.interval = config.get('interval', 0)
        self.ignore_none = config.get('ignore_none', True)

    def queue_name(self, priority):
        base_name = '%s-%s' % (self.domain, self.name)
        suffix = '.fifo' if self.fifo else ''

        if not priority:
            return '%s%s' % (base_name, suffix)

        return '%s--p%d%s' % (base_name, priority, suffix)

    @property
    def out_queue_names(self):
        if self.final:
            return []

        if self._out_queue_names is not None:
            return self._out_queue_names

        self._out_queue_names = [
            self.queue_name(priority)
            for priority in self.priority_levels
        ]

        return self._out_queue_names

    def set_workers(self, workers):
        self.workers = workers

    def in_queues(self, min_priority=None, max_priority=None):
        # no input queues?
        if not self.in_queue_names:
            return []

        sqs = self.sqs()

        retrieved = False
        retries = 0
        while not retrieved:
            in_queues = []
            try:
                for p, in_queue_name in enumerate(self.in_queue_names):
                    priority = len(self.in_queue_names) - p - 1
                    if not(
                            (min_priority is None or priority >= min_priority) and
                            (max_priority is None or priority <= max_priority)
                    ):
                        continue

                    in_queues.append(sqs.get_queue_by_name(QueueName=in_queue_name))
                    retrieved = True
            except ClientError as e:
                # only handle non-existing queue error
                if e.response.get('Error', {}).get('Code', '') != 'AWS.SimpleQueueService.NonExistentQueue':
                    raise

                # wait until input queues are created
                retrieved = False
                retries += 1
                if retries == 1:
                    print('Waiting for input queues...')

                time.sleep(2)

        if retries > 0:
            print('OK')

        return in_queues

    def sqs(self):
        return boto3.resource(
            'sqs',
            self.aws_config['region'],
            aws_access_key_id=self.aws_config['key'],
            aws_secret_access_key=self.aws_config['secret'],
        )

    def setup(self):
        sqs = self.sqs()

        self.out_queues = []
        for queue_name in self.out_queue_names:
            try:
                q = sqs.get_queue_by_name(QueueName=queue_name)
            except ClientError as e:
                # only handle non-existing queue error
                if e.response.get('Error', {}).get('Code', '') != 'AWS.SimpleQueueService.NonExistentQueue':
                    raise

                attrs = {
                    'VisibilityTimeout': '120',
                }

                if self.fifo:
                    attrs.update({
                        'FifoQueue': 'true',
                    })

                q = sqs.create_queue(QueueName=queue_name, Attributes=attrs)

            self.out_queues = [q] + self.out_queues

    def _on_task_finish(self, task_meta, task_output):
        # add to results
        self._result_mutex.acquire()
        self.results.append(task_output)

        # action after sending result message
        post_process_callback, post_process_callback_args = None, None

        if not(
            ((task_output is None) and self.ignore_none) or
            (isinstance(task_output, EmptyTaskOutput))
        ):
            if (not self.final) and (type(task_output) != TaskError):
                # if priority is a callable,
                # it will be calculated from the extracted message
                if callable(task_meta.get('priority')):
                    task_meta['priority'] = task_meta['priority'](task_output)

                # check if task output contains a post process callback
                if type(task_output) == TaskCallback:
                    post_process_callback = task_output.callback
                    post_process_callback_args = task_output.callback_args
                    task_output = task_output.result

                # also write to queues for next task to pick up
                try:
                    message_params = {
                        'MessageBody': json.dumps({
                            'meta': task_meta,
                            'value': task_output
                        }),
                    }

                    if self.fifo:
                        message_params.update({
                            'MessageDeduplicationId': str(uuid.uuid4()),
                            'MessageGroupId': '-',
                        })

                    self.out_queues[task_meta['priority']].send_message(**message_params)
                except:
                    traceback.print_exc()

        # run the callback
        if post_process_callback:
            post_process_callback(*post_process_callback_args)

        self._result_mutex.release()

    @staticmethod
    def get_messages(in_queues):
        # receive messages
        messages = []
        for in_queue in in_queues:
            if messages:
                break

            while True:
                try:
                    messages += in_queue.receive_messages(MaxNumberOfMessages=10)
                    break
                except:
                    # wait for a while
                    time.sleep(1)

        return messages

    def process(self, args, priority, pool=None, in_queues=None):
        if not pool:
            pool = TaskPool(self.workers, callback=self._on_task_finish)

        # get messages
        messages = self.get_messages(in_queues=in_queues or [])

        if not in_queues:
            pool.run_task(self.fn, args, meta={
                'priority': priority
            })

            # interval could either be a function or a number
            if callable(self.interval):
                _interval = self.interval()
            else:
                _interval = self.interval

            time.sleep(_interval)

        elif messages:
            # get payloads from messages & delete them from sqs
            payloads = []
            for message in messages:
                payloads.append(json.loads(message.body))
                message.delete()

            # run tasks
            for payload in payloads:
                pool.run_task(self.fn, (payload['value'],) + args, payload['meta'])

        # return any available results
        if self.results:
            self._result_mutex.acquire()

            _error = None
            for result in self.results:
                if type(result) == TaskError:

                    _error = result.error
                else:
                    yield result

            if _error:
                raise _error

            self.results = []
            self._result_mutex.release()

    def _run(self, args, priority=0, min_priority=None, max_priority=None):
        # create the thread pool
        pool = TaskPool(self.workers, callback=self._on_task_finish)

        # get input queues
        in_queues = self.in_queues(min_priority, max_priority)

        while True:
            for result in self.process(args=args, in_queues=in_queues, priority=priority, pool=pool):
                yield result

    def run(self, args, priority=0, iterate=False, min_priority=None, max_priority=None):
        _call = self._run(args, priority=priority, min_priority=min_priority, max_priority=max_priority)
        if iterate:
            return _call

        for _ in self._run(args, priority=priority):
            pass
