"tasks (tsk)"

import queue, sys, threading, time, traceback

from obj import Object

class Task(threading.Thread):

    "task class"

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))
        self.sleep = 0
        self.state = Object()

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def run(self):
        "run a task"
        func, args = self._queue.get()
        self.setName(self._name)
        self._result = func(*args)
        
    def wait(self, timeout=None):
        "wait for task to finish"
        super().join(timeout)
        return self._result

def launch(func, *args, **kwargs):
    "start a task"
    name = kwargs.get("name", None) 
    if not name:        
        if "__func__" in dir(func):
            name = func.__func__.__qualname__
    if not name:
            name = str(func)
    t = Task(func, *args, name=name, daemon=True)
    t.start()
    return t

def get_exception(txt="", sep=" "):
    "print exception trace"
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        if "python3" in elem[0] or "<frozen" in elem[0]:
            continue
        result.append("%s:%s" % (elem[0], elem[1]))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res
