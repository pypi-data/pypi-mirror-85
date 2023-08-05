"version (ver)"

import irc

def ver(event):
     event.reply("BOTLIB %s" % irc.__version__)