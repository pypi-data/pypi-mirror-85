"commands"

import threading, time

from obj import Default, Object, get, keys, save, update
from ofn import format
from prs import elapsed, parse

starttime = time.time()

def cmd(event):
    "list commands (cmd)"
    c = sorted(keys(event.src.cbs))
    if c:
        event.reply(",".join(c))

def thr(event):
    "list tasks (tsk)"
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        update(o, thr)
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        result.append((up, psformat % (thrname, elapsed(up))))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append(txt)
    if res:
        event.reply(" | ".join(res))
