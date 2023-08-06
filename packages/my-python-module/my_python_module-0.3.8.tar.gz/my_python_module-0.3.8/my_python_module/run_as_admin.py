#!/usr/bin/env python
# -*-coding:utf-8-*-

import win32api, win32con
import sys, os, traceback, types


def is_admin():
    """@return: True if the current user is an 'Admin' whatever that
    means (root on Unix), otherwise False.

    Warning: The inner function fails unless you have Windows XP SP2 or
    higher. The failure causes a traceback to be printed and this
    function to return False.
    """

    import win32security
    # WARNING: requires Windows XP SP2 or higher!
    try:
        adminSid = win32security.CreateWellKnownSid(
            win32security.WinBuiltinAdministratorsSid, None)
        return win32security.CheckTokenMembership(None, adminSid)
    except:
        traceback.print_exc()
        print("Admin check failed, assuming not an admin.")
        return False


def run_as_admin(cmdLine=None):
    """Attempt to relaunch the current script as an admin using the same
    command line parameters.  Pass cmdLine in to override and set a new
    command.  It must be a list of [command, arg1, arg2...] format.

    Set wait to False to avoid waiting for the sub-process to finish. You
    will not be able to fetch the exit code of the process if wait is
    False.

    Returns the sub-process return code, unless wait is False in which
    case it returns None.

    @WARNING: this function only works on Windows.
    """

    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    if cmdLine is None:
        if sys.argv[0].endswith('.py'):
            cmdLine = [sys.executable] + sys.argv
        else:
            cmdLine = sys.argv
    elif type(cmdLine) not in (types.TupleType, types.ListType):
        raise ValueError("cmdLine is not a sequence.")

    cmd = '"%s"' % (cmdLine[0],)
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'  # causes UAC elevation prompt.

    win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)
