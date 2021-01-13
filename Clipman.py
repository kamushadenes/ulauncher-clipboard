import os
import subprocess
from lib import logger, execGet, findExec, pidOf


name = "Clipman"
client = "clipman"


def canStart():
    return bool(findExec(client))


def isRunning():
    return bool(pidOf("clipman"))


def isEnabled():
    return canStart() and isRunning()


def start():
    pass
    # subprocess.call([client, 'start'])


def add(text):
    pass
    # subprocess.call([client, 'add', text])


def getHistory():
    # The only separator options are zero bytes and line breaks.
    # Line breaks are very likely to be in the actual clipboard entries, so we can't use that.
    # Zero bytes are less likely, but would not be my first choice.
    return execGet(
        "sh", "-c", "{0} pick --max-items=30 --tool=STDOUT --print0".format(client)
    ).split("\x00")
