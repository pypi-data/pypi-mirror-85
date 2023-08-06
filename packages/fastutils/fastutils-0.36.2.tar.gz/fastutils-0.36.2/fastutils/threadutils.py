
import time
import logging
import threading
from queue import Queue
from queue import Empty
from . import funcutils
from . import sysutils

logger = logging.getLogger(__name__)
get_ident = threading.get_ident

class StartOnTerminatedService(RuntimeError):
    pass

class LoopIdle(RuntimeError):
    pass

class ServiceCore(object):

    def __init__(self):
        # service inner setup
        self.setup()

    def setup(self):
        # service are alway work in new thread.
        # and there is only one work thread for a service.
        self.work_thread_starting_lock = threading.Lock()
        self.work_thread = None
        # service is always ready while not terminated.
        # so that before you terminate a service, you can start and stop the service many times.
        self.terminate_flag = False
        self.terminated_time = None
        self.stop_flag = False
        self.start_time = None
        self.stop_time = None
        self.stoped_time = None
        self.is_running = False

    def start(self):
        if not self.is_running:
            logger.debug("Service {0} starting...".format(self.name))
        else:
            logger.debug("Service {0} already started.".format(self.name))
        if self.terminated_time:
            logger.warn("Can not start on terminated thread.")
            raise StartOnTerminatedService()
        self.stop_flag = False
        self.start_time = time.time()
        self.stop_time = None
        self.stoped_time = None
        with self.work_thread_starting_lock:
            if self.work_thread is None:
                self.work_thread = threading.Thread(target=self.main)
                self.work_thread.setDaemon(True)
                self.work_thread.start()

    def join(self, timeout=-1):
        stime = time.time()
        while self.is_running:
            if timeout >= 0 and time.time() - stime >= timeout:
                return False
            time.sleep(1)
        return True

    def stop(self, wait=True, wait_timeout=-1):
        if self.is_running:
            logger.debug("Service {0} stopping...".format(self.name))
        else:
            logger.debug("Service {0} already stoped.".format(self.name))
        self.stop_flag = True
        self.stop_time = time.time()
        if wait:
            stime = time.time()
            while self.is_running:
                if wait_timeout > 0 and time.time() - stime > wait_timeout:
                    break
                else:
                    time.sleep(1)

    def terminate(self, wait=True, wait_timeout=-1):
        logger.debug("Service {0} terminating...".format(self.name))
        self.terminate_flag = True
        stime = time.time()
        self.stop(wait, wait_timeout)
        if wait:
            while not self.terminated_time:
                if wait_timeout > 0 and time.time() - stime > wait_timeout:
                    break
                else:
                    time.sleep(1)

    def main(self):
        while not self.terminate_flag:
            if self.stop_flag:
                time.sleep(1)
                continue
            try:
                self.is_running = True
                message = "Service {0} started.".format(self.name)
                logger.debug(message)
                loop_data = {
                    "self": self,
                    "_service": self,
                    "_server": self.server,
                }
                loop_data.update(self.kwargs)
                loop_data["_loop_data"] = loop_data
                while not self.stop_flag:
                    try:
                        message = "Service {} calling service_loop {}".format(self.name, self.service_loop)
                        logger.debug(message)
                        service_loop_result = funcutils.call_with_inject(self.service_loop, loop_data)
                        loop_data["_service_loop_result"] = service_loop_result
                        message = "Service {} call service_loop {} finished, result={}".format(self.name, self.service_loop, service_loop_result)
                        logger.debug(message)
                    except LoopIdle:
                        if self.on_loop_idle:
                            message = "Service {} got LoopIdle error, calling on_loop_idle: {}".format(self.name, self.on_loop_idle)
                            logger.debug(message)
                            on_loop_idle_result = funcutils.call_with_inject(self.on_loop_idle, loop_data)
                            try:
                                loop_data["_on_loop_idle_result"] = on_loop_idle_result
                                message = "Service {} got LoopIdle error and call on_loop_idle {} finished, result={}".format(self.name, self.on_loop_idle, on_loop_idle_result)
                                logger.debug(message)
                            except Exception as on_loop_idle_error:
                                loop_data["_on_loop_idle_error"] = on_loop_idle_error
                                error_message = "Service {} got LoopIdle error and call on_loop_idle {} got error again, on_loop_idle_error={}".format(self.name, self.on_loop_idle, on_loop_idle_error)
                                logger.exception(error_message)
                        else:
                            message = "Service {} got LoopIdle error but has NO on_loop_idle setting, do NOTHING...".format(self.name)
                            logger.debug(message)
                    except Exception as loop_error:
                        loop_data["_loop_error"] = loop_error
                        error_message = "Service {} got error in service loop, lopp_error={}".format(self.name, loop_error)
                        logger.exception(error_message)
                        if self.on_loop_error:
                            try:
                                on_loop_error_result = funcutils.call_with_inject(self.on_loop_error, loop_data)
                                loop_data["_on_loop_error_result"] = on_loop_error_result
                            except Exception as error:
                                logger.exception("Service {} got error in on_loop_error...".format(self.name))
                    finally:
                        if self.on_loop_finished:
                            try:
                                on_loop_finished_result = funcutils.call_with_inject(self.on_loop_finished, loop_data)
                                loop_data["_on_loop_finished_result"] = on_loop_finished_result
                            except Exception as on_loop_finished_error:
                                loop_data["_on_loop_finished_error"] = on_loop_finished_error
                                error_message = "Service {} call on_loop_finished {} and got error: {}".format(self.name, self.on_loop_finished, on_loop_finished_error)
                                logger.exception(error_message)
                    if self.loop_interval:
                        try:
                            time.sleep(self.loop_interval)
                        except InterruptedError:
                            self.terminate(wait=False)
                            break
            finally:
                self.is_running = False
                self.stoped_time = time.time()
                logger.debug("Service {0} stopped.".format(self.name))
        self.terminated_time = time.time()
        logger.debug("Service {0} terminated.".format(self.name))


class Service(ServiceCore):

    def __init__(self, service_loop, kwargs=None, server=None, name=None, on_loop_error=None, on_loop_idle=None, on_loop_finished=None, loop_interval=0):
        self.service_loop = service_loop
        self.kwargs = kwargs or {}
        self.server = server
        self.name = name or service_loop.__name__
        self.on_loop_error = on_loop_error
        self.on_loop_idle = on_loop_idle
        self.on_loop_finished = on_loop_finished
        self.loop_interval = loop_interval
        super().__init__()

class ServiceBase(ServiceCore):
    name = None
    loop_interval = 0
  
    def __init__(self):
        self.args = ()
        self.kwargs = {}
        super().__init__()

    def on_loop_finished(self):
        pass

    def on_loop_error(self, error):
        pass

    def service_loop(self):
        raise NotImplementedError()



class SimpleProducerConsumerServer(object):

    def __init__(self,
            produce,
            consume,
            name=None,
            queue_size=0,
            consume_pull_timeout=5,
            produce_sleep=2,
            on_produce_error=None,
            on_produce_finished=None,
            on_produce_idle=None,
            on_consume_error=None,
            on_consume_finished=None,
            on_consume_idle=None,
            producer_number=1,
            produce_kwargs=None,
            consumer_number=5,
            consume_kwargs=None,
            ):
        self.produce = produce
        self.consume = consume
        self.name = name or sysutils.get_worker_id("SimpleProducerConsumerServer")
        self.consume_pull_timeout = consume_pull_timeout
        self.produce_sleep = produce_sleep
        self.on_produce_error = on_produce_error
        self.on_produce_finished = on_produce_finished
        self.on_produce_idle = on_produce_idle
        self.on_consume_error = on_consume_error
        self.on_consume_finished = on_consume_finished
        self.on_consume_idle = on_consume_idle
        self.producer_number = producer_number
        self.produce_kwargs = produce_kwargs or {}
        self.consumer_number = consumer_number
        self.consume_kwargs = consume_kwargs or {}
        self.producers = []
        self.consumers = []
        self.queue = Queue(queue_size)

    def start(self):
        self.start_producers()
        self.start_consumers()
    
    def stop(self, wait=True, wait_timeout=-1):
        for producer in self.producers:
            producer.stop(wait=False)
        for consumer in self.consumers:
            consumer.stop(wait=False)
        if wait:
            self.join(wait_timeout)

    def terminate(self, wait=True, wait_timeout=-1):
        for producer in self.producers:
            producer.terminate(wait=False)
        for consumer in self.consumers:
            consumer.terminate(wait=False)
        if wait:
            self.join(wait_timeout)

    def join(self, timeout=-1):
        stime = time.time()
        while True:
            living_producers = 0
            living_consumers = 0
            for service in self.producers:
                if service.is_running:
                    living_producers += 1
            for service in self.consumers:
                if service.is_running:
                    living_consumers += 1
            if living_producers == 0 and living_consumers == 0:
                return True
            if timeout >= 0 and time.time() - stime >= timeout:
                return False
            time.sleep(1)

    def start_producers(self):
        for index in range(self.producer_number):
            name = self.name + ":producer#{0}".format(index+1)
            producer = Service(self._produce, server=self, name=name, kwargs=self.produce_kwargs, on_loop_error=self.on_produce_error, on_loop_idle=self.on_produce_idle, on_loop_finished=self.on_produce_finished)
            producer.start()
            self.producers.append(producer)
    
    def start_consumers(self):
        for index in range(self.consumer_number):
            name = self.name + ":consumer#{0}".format(index+1)
            consumer = Service(self._consume, server=self, name=name, kwargs=self.consume_kwargs, on_loop_error=self.on_consume_error, on_loop_idle=self.on_consume_idle, on_loop_finished=self.on_consume_finished)
            consumer.start()
            self.consumers.append(consumer)

    def _produce(self, _loop_data):
        logger.debug("doing _produce")
        tasks = funcutils.call_with_inject(self.produce, _loop_data)
        logger.debug("doing _produce got tasks={0}".format(tasks))
        if tasks:
            for task in tasks:
                self.queue.put(task)
        else:
            raise LoopIdle()

    def _consume(self, _loop_data):
        logger.debug("doing _consume")
        try:
            task = self.queue.get(timeout=self.consume_pull_timeout)
            _loop_data["_task"] = task
            logger.debug("doing _consume got task={}".format(task))
        except Empty:
            raise LoopIdle()
        return funcutils.call_with_inject(self.consume, _loop_data)
