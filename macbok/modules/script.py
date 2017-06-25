from macbok.common.task import Task
import os
import subprocess


class Script(Task):
  def __init__(self, command, _internal=False, _bytes=False):
    """Runs a shell command.

    Args:
      _internal: If this script should act as a "hidden node", and not be
          exposed to the user. Set this to true, if this script is an
          informational command and does not require interaction. If
          _internal is true, then the command standard output will be
          yielded to the caller.
      _bytes: Return the result as bytes, rather than decoding to utf8.
    """
    self.command = command
    self._internal = _internal
    self._bytes = _bytes

  def __repr__(self):
    arguments = [repr(self.command)]
    if self._internal:
      arguments.append("_internal=%s" % repr(self._internal))
    if self._bytes:
      arguments.append("_bytes=%s" % repr(self._bytes))
    return "Script(%s)" % (", ".join(arguments))

  def is_hidden(self):
    return self._internal

  def run(self):
    output_file = None
    error_file = None
    if self._internal:
      output_file = subprocess.PIPE
      error_file = open(os.devnull, "r+")
    args = ["/bin/sh", "-c", self.command]
    process = subprocess.Popen(args, stdout=output_file, stderr=error_file)
    if self._internal:
      output_bytes = process.communicate()[0]
      if self._bytes:
        return output_bytes
      else:
        return output_bytes.decode("utf8")
    else:
      process.wait()
      if process.returncode != 0:
        raise ValueError("Command %s returned non-zero exit status %s" %
                         (repr(self.command), repr(process.returncode)))
