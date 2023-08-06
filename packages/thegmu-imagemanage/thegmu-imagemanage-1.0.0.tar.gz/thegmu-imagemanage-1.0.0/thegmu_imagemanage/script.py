#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    script.py
    ~~~~~~~~~

    Command line script utilities.

    Most notably :func:`runcmd` that runs Linux
    bash command strings and outputs to console as needed.

"""

from datetime import datetime
import inspect
import os
import re
import socket
import subprocess
import sys


class ScriptException(Exception):
    """Exception specific to this file, notably the 'initlock' function."""


def begin():
    """Print :func:`timestamp` with BEGIN."""
    timestamp('BEGIN')


def command_exists(command_name):
    """Given the name of an operating system program
    assumed to be in the current path then return True or
    False if the command exists.

    :param commmand_name: the command name

    :return True: if the command exists.
    """

    if (command_name.find(' ') > -1):
        command_name = command_name[:command_name.find(' ')]

    cmd = "command -v " + command_name
    try:
        output_line = runcmd(cmd, console=False,
                             exception_continue=True,
                             encoding='ascii')
        output_line = str(output_line).strip()
    except subprocess.CalledProcessError:
        output_line = "not found"

    if (output_line.find(command_name) > -1):
        return True

    return False


def end():
    """Print :func:`timestamp` with END."""
    timestamp('END')


def env_string_replace(env_string, env_vars=None, empty_sub=False):
    """Replace all enviornment variables in a string with the environment variable value.

    #. If "env_vars" list is given then ignore os.environ and use this list.
    #. ${HOME}: all substitutions variables require curly braces as in ${HOME}.
    #. If "env_vars" dict is given the both key and values are taken from the dictionary.
    #. If an environment variable does not exist then no substitution is made.
    #. If empty_sub is True then  if an environment variable does not exist
       it will be replaced with an empty string.

    :param env_string: the string for substituion with env variables.
    :param env_vars: substitution for os.envioron list of environment variables.
    :param empty_sub: If True then variables not found are removed,
        otherwise the they are left as in the string.

    """
    if (env_vars is None):
        env_vars = os.environ
    elif (isinstance(env_vars, (list, tuple))):
        env_vars = dict((x, os.getenv(x)) for x in env_vars if x in os.environ)
    else:
        assert isinstance(env_vars, dict),\
            "env_string_replace: env_vars is not a list or dict: %s" % (env_vars, )

    env_re = re.compile(r'\$\{([^\}]+)\}')
    env_replace = ""
    env_next = env_re.search(env_string)

    while (env_next):
        env_replace += env_string[:env_next.span()[0]]
        if (env_next.group(1) in env_vars):
            env_replace += env_vars[env_next.group(1)]
        elif (not empty_sub):
            env_replace += env_string[env_next.span()
                                      [0]:env_next.span()[1]]
        env_string = env_string[env_next.span()[1]:]
        env_next = env_re.search(env_string)

    env_replace += env_string

    return env_replace


def fatal(msg, exit_ok=True):
    """Prints timestamp() with 'FATAL' to stderr prepended
    to a msg. Exit with -1 unless exit_ok is False.

    :param exit_ok: If True then call sys.exit(-1) after printing message.

    """

    warn_prefix = timestamp('FATAL', True)
    warn(msg, warn_prefix=warn_prefix)
    if (exit_ok is True):
        sys.exit(-1)


def getnow(now_type=None, target_datetime=None):
    """getnow() get a log file timestamp.

    :param now_type: format option:
        #: None: 20190401:103226.82
        #: 'script': 2019-04-01-10:32:26
        #: 'script_date': 2019-04-01
        #: 'SQL': 2019-04-01-10:32:26

    :param target_datetime: datetime.datetime() object.
        When None then defaults to datetime.now().

    """

    nowstr = None
    if(now_type is None):
        if (target_datetime is None):
            now = datetime.now()
        else:
            now = target_datetime
        nowstr = '%d%02d%02d:%02d%02d%02d.%02d' % (
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second,
            now.microsecond / 10000,
        )
    elif now_type in ('script', 'SQL', 'script_date'):
        if (target_datetime is None):
            nowstr = '%s' % datetime.today()
        else:
            nowstr = '%s' % (target_datetime, )
        nowstr = nowstr[:-7]
        if (now_type in ('script', )):
            nowstr = nowstr.replace(' ', '-')
        if (now_type in ('script_date', )):
            nowstr = nowstr[:10]

    return nowstr


def get_hostname(host_name_only=False):
    """Retrun :meth:`socket.gethostbyaddr` string of the FQDN,
    or fully qualified domain name.

    :param host_name_only: short name only
        Example::

            localhost.localdomain -> localhost

    """
    fqdn = socket.gethostbyaddr(socket.gethostname())[0]
    if ((host_name_only is True) and (fqdn.find('.') > -1)):
        return fqdn[:fqdn.find('.')]
    return fqdn


def get_log_frame():
    """stack trace log frame of current function."""

    callee_frame_list = inspect.getouterframes(inspect.currentframe())
    if len(callee_frame_list) > 3:
        frame = callee_frame_list[3]
    else:
        frame = callee_frame_list.pop()
    function_name = frame[3]
    if function_name == '<module>':
        function_name = '__main__'

    log_frame = [os.path.basename(frame[1]), function_name, frame[2]]
    return log_frame


def initlock(lockpath):
    """
    Use a lock file to ensure only a single instance of a script is running at any
    one time.

    #. The process id, PID, is the first and only line of the lock file.
    #. Subsequent calls to :func:`initlock` check if the process corresponding
       to the PID is running and if not then acquires the lock, else the program
       exits.

    .. note:: initlock fails if Linux account permission is denied by file permissions.


    :param lockpath: The file name to hold the PID, for example::

        /tmp/myscript.sh.lock

    """

    _name = 'initlock'

    if (os.path.exists(lockpath)):
        pid = None
        with open(lockpath, 'r') as lock_fh:
            pid = lock_fh.readline().strip()

        if (pid is not None):
            cmd = 'ps --no-headers -p %s' % pid

            test_output = runcmd(
                cmd,
                exception_continue=True,
                encoding='utf-8')
            """An integer value indicates an exception when console is false."""
            if (not isinstance(test_output, int)):

                test_output = test_output.strip()

                if (test_output[:len(pid)] == pid):
                    msg = "%s is running for file %s, (%s)." % (
                        _name, lockpath, test_output)
                    raise ScriptException(msg)

        with open(lockpath, 'w') as lock_fh:
            lock_fh.write(str(os.getpid()) + os.linesep)
        os.chmod(lockpath, 0o0777)


def msg_error_code(msg, error_code):
    """Create a new msg with 'ERRORCODE error_code:' for keyword log parsing.

    :param msg: one line log message.
    :param error_code: any string but typically digits only.

    """
    return "ERRORCODE %s: %s" % (error_code, msg)


def print_header(char, msg, for_return=False, width=80):
    """Print 3 lines per message using character line
    separators of the specified char, for example::

        ++++++++++++++++++++++++++++++++++++++++
        print_header passing char as '+'.
        ++++++++++++++++++++++++++++++++++++++++

    :param char: The character to repeat.
    :param msg: A one line log message.
    :param for_return: If True return as string.
    :param width: How many char to repeat, default is 80.

    """
    charline = char * width
    output = charline + os.linesep + msg + os.linesep + charline
    if for_return:
        return output + os.linesep
    print(output)
    return None


def print_dashes(msg, for_return=False):
    """Call :func:`print_header` with char '-'"""
    return print_header('-', msg, for_return)


def print_hashes(msg, for_return=False):
    """Call :func:`print_header` with char '#'"""
    return print_header('#', msg, for_return)


def print_sql_comment(msg, for_return=False):
    """Prefix '--' to every line passed in msg.

    :param msg: A multi-line log message.
    :param for_return: If True then return the string.

    """

    prefix = '-- '
    output = prefix + os.linesep + prefix + ' ' + msg + os.linesep + prefix
    if for_return:
        return output + os.linesep
    print(output)
    return None


def runcmd(
        cmd,
        console=False,
        exception_continue=False,
        encoding=None,
        return_code=False):
    """
    Characterized subprocess.check_call/check_output design patterns.

    .. note:: stderr is always redirected to stdout.

    :param cmd: A Linux command.
    :param console: If True then cmd is printed first
        than output is sent to stdout.
    :param exception_continue: If True exceptions become warnings
        and execution continues.
    :param encoding: binary bytes are returned unless encoding
        is passed as 'utf-8', 'ascii' or other encoding.
    :param return_code: Only return the integer return
        code value when console is True or an exception occurs.

    """

    if console:
        print(cmd)
    response = None

    if (return_code):
        encoding = None

    try:
        if (console):
            subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)
            encoding = None
            response = 0
        else:
            if (return_code):
                subprocess.check_output(
                    cmd, stderr=subprocess.STDOUT, shell=True)
                response = 0
            else:
                response = subprocess.check_output(
                    cmd, stderr=subprocess.STDOUT, shell=True)

    except subprocess.CalledProcessError as call_error:
        response = call_error.returncode
        encoding = None
        if (call_error.output):
            call_error.output = "%s: return code(%s): %s" % (
                cmd, call_error.returncode, call_error.output)
        else:
            call_error.output = "%s: return code(%s)" % (
                cmd, call_error.returncode)
        if (not exception_continue):
            raise call_error
        if (console):
            warn(call_error.output)

    if (encoding is None):
        return response

    return response.decode(encoding)


def success(msg='success', eol=True, success_name=None):
    """Print function name with 'success' or an optional msg to stdout.

    :param msg: optional log message.
    :param eol: if True then append os.linesep.
    :param success_name: Substitute the function name with this string.

    """

    if (eol is True):
        msg += os.linesep

    if (success_name is None):
        success_name = "%s " % get_log_frame()[0]

    sys.stdout.write(success_name + msg)


def timestamp(msg='TIMESTAMP', for_return=False):
    """print a log message using a prefix of timestamp, file name,
    function name and line number prefix.

    Example::

        [2019-04-01-11:02:07] case.py.run.605 % hello

    :param msg: A one line log message.
    :param for_return: If True return the msg.

    """

    log_frame = get_log_frame()
    msg = '[%s] %s.%s.%s %% %s ' % (
        getnow('script'), log_frame[0], log_frame[1], log_frame[2], msg)
    if (for_return is True):
        return msg
    sys.stdout.write(msg + os.linesep)
    return None


def warn(msg, eol=True, warn_prefix=None):
    """prints timestamp('WARNING) to stderr along with the msg.
    Example:
    [2019-04-01-11:07:25] system_test.py.test00_python_stuff.50 % WARNING hello

    :param msg: A one line log message.
    :param eol: If True append os.linesep to the msg.
    :param warn_prefix: Replace timestamp('WARNING') with this string.

    """

    msg = '%s' % msg
    if (warn_prefix is None):
        warn_prefix = timestamp('WARNING', True)
    if (eol is True):
        msg += os.linesep
    sys.stderr.write(warn_prefix + msg)
