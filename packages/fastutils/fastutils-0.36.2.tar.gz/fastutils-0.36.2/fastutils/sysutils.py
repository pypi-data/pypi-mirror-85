import os
import psutil
import socket
import threading



def get_worker_id(prefix=None):
    """worker_id = prefix:hostname:process-id:thread-id
    """
    worker_inner_id = "{}:{}:{}".format(socket.gethostname(), os.getpid(), threading.get_ident())
    if prefix:
        return prefix + ":" + worker_inner_id
    else:
        return worker_inner_id


def get_daemon_application_pid(pidfile):
    if os.path.exists(pidfile) and os.path.isfile(pidfile):
        with open(pidfile, "r", encoding="utf-8") as fobj:
            pid = int(fobj.read().strip())
        try:
            p = psutil.Process(pid=pid)
            return pid
        except psutil.NoSuchProcess:
            return 0
    else:
        return 0
