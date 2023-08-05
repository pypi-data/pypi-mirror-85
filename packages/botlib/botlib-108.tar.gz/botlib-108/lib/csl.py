"console (csl)"

import atexit, readline

from hdl import Event, Handler
from thr import launch
from trm import termsave, termreset

cmds = []

class Console(Handler):

    "console class"

    def announce(self, txt):
        "silence announcing"

    def direct(self, txt):
        "print txt"
        print(txt.rstrip())

    def input(self):
        "loop for input"
        while 1:
            event = self.poll()
            self.put(event)
            event.wait()
            
    def poll(self):
        "wait for input"
        e = Event()
        e.orig = repr(self)
        e.otxt = e.txt = input("> ")
        return e

    def say(self, channel, txt):
        "strip channel from output"
        self.direct(txt)

    def start(self):
        "start console"
        super().start()
        launch(self.input, name="Console.input")

def complete(text, state):
    "complete matches"
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def getcompleter():
    "return the completer"
    return readline.get_completer()

def setcompleter(commands):
    "set the completer"
    cmds.extend(commands)
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))
