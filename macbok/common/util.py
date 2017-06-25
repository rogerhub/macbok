import functools
import os
import pwd

from os import path


@functools.lru_cache()
def Username():
  user = pwd.getpwuid(os.getuid())
  return user.pw_name


def Which(name):
  env_path = os.environ.get("PATH")
  if env_path:
    for bin_directory in env_path.split(":"):
      full_path = path.join(bin_directory, name)
      if path.exists(full_path):
        return full_path


def BashQuote(s):
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
