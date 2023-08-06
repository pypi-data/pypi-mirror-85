import datetime
import logging

from fastutils import randomutils
from fastutils import sysutils
from fastutils import threadutils

from django.utils import timezone
from django.db.models import Q
from django.db import close_old_connections

from django_db_lock.client import DjangoDbLock
from django_db_lock.client import get_default_lock_service

logger = logging.getLogger(__name__)


class SimpleTaskService(object):

    def __init__(self, model, lock_service, worker_name, batch_size=1, **extra_server_kwargs):
        self.model = model
        self.lock_service = lock_service
        self.worker_name = worker_name
        self.batch_size = batch_size
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name
        self.extra_server_kwargs = extra_server_kwargs

    def get_ready_tasks(self):
        # get ready tasks
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        lock_name = self.model.GET_READY_TASKS_LOCK_NAME_TEMPLATE.format(app_label=app_label, model_name=model_name)
        timeout = self.model.GET_READY_TASKS_LOCK_TIMEOUT
        with DjangoDbLock(self.lock_service, lock_name, str(randomutils.uuid4()), timeout) as locked:
            if not locked:
                return []
            tasks = []
            now = timezone.now()
            for task in self.model.objects.filter(status=self.model.READY).filter(ready_time__lte=now).filter(Q(expire_time=None) | Q(expire_time__gte=now)).order_by("mod_time")[:self.batch_size]:
                task.start(self.worker_name, save=True)
                tasks.append(task)
                logger.debug("task {} have been fetched and will be handled soon...".format(task))
            return tasks

    def reset_dead_tasks(self):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        lock_name = self.model.RESET_DEAD_TASKS_LOCK_NAME_TEMPLATE.format(app_label=app_label, model_name=model_name)
        timeout = self.model.RESET_DEAD_TASKS_LOCK_TIMEOUT
        with DjangoDbLock(self.lock_service, lock_name, str(randomutils.uuid4()), timeout) as locked:
            if not locked:
                return []
            dead_time_limit = timezone.now() - datetime.timedelta(seconds=self.model.TASK_DOING_TIMEOUT)
            tasks = []
            for task in self.model.objects.filter(status=self.model.DOING).filter(start_time__lte=dead_time_limit):
                task.reset(save=True)
                tasks.append(task)
            logger.debug("{} dead tasks have been reset...".format(len(tasks)))
            return tasks

    def do_task(self, _task):
        logging.debug("doing task {0}...".format(_task))
        _task.do_task(self.worker_name)

    def serve_forever(self, wait=True):
        params = {}
        params.update(self.extra_server_kwargs)
        if not "on_produce_error" in params:
            params["on_produce_error"] = close_old_connections
        if not "on_consume_error" in params:
            params["on_consume_error"] = close_old_connections
        if not "on_produce_idle" in params:
            params["on_produce_idle"] = self.reset_dead_tasks
        self.server = threadutils.SimpleProducerConsumerServer(
            produce=self.get_ready_tasks,
            consume=self.do_task,
            **self.extra_server_kwargs,
        )
        self.server.start()
        if wait:
            self.server.join()
        return self.server

    def join(self, wait_timeout=-1):
        return self.server.join(wait_timeout)

    def stop(self, wait=True, wait_timeout=-1):
        return self.server.stop(wait, wait_timeout)
    
    def terminate(self, wait=True, wait_timeout=-1):
        return self.server.terminate(wait, wait_timeout)

    @classmethod
    def serve(cls, model, lock_service=None, worker_name_prefix=None, batch_size=1, wait=True, **extra_server_kwargs):
        the_lock_service = lock_service or get_default_lock_service()
        the_worker_name_prefix = worker_name_prefix or cls.__name__
        worker_name = sysutils.get_worker_id(the_worker_name_prefix)
        service = cls(model, the_lock_service, worker_name=worker_name, batch_size=batch_size, **extra_server_kwargs)
        service.serve_forever(wait)
        return service
