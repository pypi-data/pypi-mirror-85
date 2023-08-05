"find objects (fnd)"

import os, time
import obj

from dbs import find, list_files
from obj import cdir, fntime, get, keys
from ofn import format
from prs import elapsed

def fnd(event):
    "locate and show objects on disk"
    if not event.args:
        return event.reply(" | ".join(list_files(obj.wd)))
    nr = -1
    for otype in get(event.src.names, event.args[0], [event.args[0]]):
        for fn, o in find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            txt = "%s %s" % (str(nr), format(o, event.xargs, skip=event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
