def ver(event):
    from irc import __version__
    event.reply("BOTLIB %s" % __version__)
