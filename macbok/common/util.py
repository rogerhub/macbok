import os
import pwd
import threading
from itertools import repeat
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
    for bin_directory in env_path.split(":"):
      full_path = join(bin_directory, name)
      if exists(full_path):
        return full_path


def bash_quote(s):
  """Escape argument for bash.

  This is a POSIX-compatible argument escape function designed for bash. Use
  this to quote variable arguments that you send to `container.bash("...")`.

  Note that pipes.quote and subprocess.list2cmdline both produce the INCORRECT
  value to use in this scenario. Do not use those. Use this.

  Args:
    s: An argument to escape.

  Returns:
    The escaped argument.
  """
  return "'" + s.replace("'", "'\\''") + "'"
