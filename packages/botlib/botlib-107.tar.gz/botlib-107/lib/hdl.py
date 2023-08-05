"handler (hdl)"

import importlib, inspect, obj, os, queue, sys, threading, time
import importlib.util

from obj import Default, Object, Ol, spl, update
from prs import parse
from thr import launch, get_exception

debug = False

class Event(Default):

    "event class"

    __slots__ = ("prs", "src")

    def __init__(self):
        super().__init__()
        self.done = threading.Event()
        self.result = []
        
    def direct(self, txt):
        "send txt to console"
        print(txt)

    def parse(self, txt):
        "parse an event"
        self.prs = Default()
        parse(self.prs, txt)
        args = self.prs.txt.split()
        if args:
            self.cmd = args.pop(0)
        if args:
            self.args = list(args)
            self.rest = " ".join(self.args)
            self.otype = args.pop(0)
        if args:
            self.xargs = args

    def ready(self):
        self.done.set()
        
    def reply(self, txt):
        "add txt to result"
        self.result.append(txt)

    def show(self):
        "display result"
        for txt in self.result:
            self.direct(txt)
        self.ready()
        
    def wait(self):
        self.done.wait()

class Handler(Object):

    "basic event handler"

    threaded = False

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.names = Ol()
        self.queue = queue.Queue()
        self.stopped = False

    def clone(self, hdl):
        update(self.cbs, hdl.cbs)

    def cmd(self, txt):
        e = Event()
        e.txt = txt
        return self.dispatch(e)

    def dispatch(self, event):
        "run callbacks for event"
        if not event.src:
            event.src = self
        event.parse(event.txt)
        if event.cmd and event.cmd in self.cbs:
            self.cbs[event.cmd](event)
            event.show()
        event.ready()

    def files(self):
        return list_files(obj.wd)

    def init(self, mns):
        "call init() of modules"
        for mn in spl(mns):
            try:
                spec = importlib.util.find_spec(mn)
            except ModuleNotFoundError:
                print("%s not found" % mn)
                continue
            if spec:
                mod = self.intro(direct(mn))
                func = getattr(mod, "init", None)
                if func:
                    func(self)

    def intro(self, mod):
        "introspect a module"
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if "event" in o.__code__.co_varnames:
                if o.__code__.co_argcount == 1:
                    self.register(key, o) 
        for _key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                self.names.append(o.__name__.lower(), t)
        return mod

    def handler(self):
        "handler loop"
        while not self.stopped:
            event = self.queue.get()
            if not event:
                break
            if self.threaded:
                event.thrs = []
                event.thrs.append(launch(self.dispatch, event, name=event.cmd))
                continue
            self.dispatch(event)

    def put(self, e):
        "put event on queue"
        self.queue.put_nowait(e)

    def register(self, name, callback):
        "register a callback"
        self.cbs[name] = callback

    def scan(self, modname="", path=""):
        "scan a modules directory"
        if modname:
            path = os.path.dirname(direct(modname).__file__)
        elif not path:
            path = os.path.dirname(obj.__file__)
        sys.path.insert(0, path)
        for mn in [x[:-3] for x in os.listdir(path)
                          if x and x.endswith(".py")
                          and not x.startswith("__")
                          and not x == "setup.py"]:
            self.intro(direct(mn))

    def start(self):
        "start handler"
        launch(self.handler, name="Handler.handler")

    def stop(self):
        "stop handler"
        self.stopped = True
        self.queue.put(None)

    def walk(self, pkgnames):
        "walk over packages and load their modules"
        for name in spl(pkgnames):
            mod = direct(name)
            for n in [x[:-3] for x in os.listdir(mod.__path__[0])
                                if x.endswith(".py")]:
                self.intro(direct("%s.%s" % (name, n)))
            
    def wait(self):
        if not self.stopped:
            while 1:
                time.sleep(30.0)

def direct(name, pname=''):
    "load a module"
    return importlib.import_module(name, pname)

def mods(mn):
    "return all modules in a package"
    try:
        spec = importlib.util.find_spec(mn)
    except ModuleNotFoundError:
        print("%s not found" % mn)
        return
    modules = []
    if spec:
        pkg = direct(mn)
        path = pkg.__file__ or pkg.__path__[0]
        m = [x.split(os.sep)[-1][:-3] for x in os.listdir(path) 
                                     if x.endswith(".py")
                                     and not x == "setup.py"]
        
        for mm in m:
            mmm = "%s.%s" % (mn, mm)
            try:
                spec = importlib.util.find_spec(mmm)
            except ModuleNotFoundError:
                print("%s not found" % mn)
                continue
            modules.append(direct(mmm))
    return modules
