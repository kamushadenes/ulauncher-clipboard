import logging
import subprocess
import cgi
from time import sleep
from distutils.spawn import find_executable as findExec
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from actions import DoNothingAction, ExtensionCustomAction, RenderResultListAction

logger = logging.getLogger('ulauncher-clipboard')

def tryOr(function, args, fallback):
    try:
        return apply(function, args)
    except Exception:
        return fallback

def tryInt(string, fallback):
    return tryOr(int, [string, 10], fallback)

def pidOf(name):
    # Get the first pid (there may be many space-separated pids), and parse to int
    # Should probably be rewritten in a more "pythonic" way since lambdas can't do multiple lines/statements
    _pidOf = lambda name: int(subprocess.check_output(['pidof', name]).split(' ', 1)[0], 10)
    return tryOr(_pidOf, [name], False)

def ensureStatus(provider, attempts=0):
    running = provider.isRunning()

    if not running:
        logger.info('Attempting to start provider %s', provider.name)
        if not provider.canStart() or attempts > 30:
            logger.warn('Could not start provider %s (%i attempts)', provider.name, 0)
            return false

        provider.start()
        sleep(0.05 * attempts)
        return ensureStatus(provider, attempts + 1)

    isEnabled = provider.isEnabled()

    if not isEnabled:
        logger.warn('Provider %s is disabled', provider.name)

    return isEnabled

def showStatus(status):
    return RenderResultListAction([ExtensionResultItem(
        name          = status,
        on_enter      = DoNothingAction(),
        highlightable = False
    )])

def entryAsResult(query, entry):
    entryArr = entry.strip().split('\n')
    context = []
    pos = 0

    if query:
        line = filter(lambda l: query in l.lower(), entryArr)[0]
        pos = entryArr.index(line)

    if pos > 0:
        line = entryArr[pos - 1].strip()
        if line:
            context.append('...' + line)

    context.append(entryArr[pos])

    if len(entryArr) > pos + 1:
        line = entryArr[pos + 1].strip()
        if line:
            context.append(line + '...')

    encoded = list(map(cgi.escape, context))

    return ExtensionSmallResultItem(
        icon     = 'edit-paste.png',
        name     = '\n'.join(encoded),
        on_enter = ExtensionCustomAction(entry)
    )