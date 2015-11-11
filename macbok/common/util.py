import os
import pwd
import threading
from itertools import imap, repeat
from os.path import exists, join


def memoize(fn):
    lock = threading.Lock()
    valid = [False]
    value = [None]

    def wrapped(*args, **kwargs):
        with lock:
            if valid[0]:
                return value[0]
            else:
                value[0] = fn(*args, **kwargs)
                valid[0] = True
                return value[0]

    def reset():
        with lock:
            valid[0] = False
            value[0] = None

    wrapped.reset = reset
    return wrapped


@memoize
def get_username():
    user = pwd.getpwuid(os.getuid())
    return user.pw_name


def which(name):
    env_path = os.environ.get("PATH")
    if env_path:
        matches = filter(exists, imap(join, env_path.split(":"), repeat(name)))
        if matches:
            return matches[0]


def bash_quote(s):
    """
    POSIX-compatible argument escape function designed for bash. Use this to quote variable
    arguments that you send to `container.bash("...")`.

    Note that pipes.quote and subprocess.list2cmdline both produce the INCORRECT value to use in
    this scenario. Do not use those. Use this.

    """

    return "'" + s.replace("'", "'\\''") + "'"
