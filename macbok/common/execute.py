from __future__ import print_function

import logging
import types
from macbok.common.task import Task

_primitive_types = (bool, int, type(u""), type(b""), dict)


def Execute(task_generator):
  """Execute a task generator.

  This is the main entry point for macbok. Call this function with the function
  that configures the system.

  Args:
    task_generator: A generator that yields configuration tasks.
  """
  _ExecuteTask(task_generator(), suppress_failures=True)


def _ExecuteTask(task, suppress_failures=False):
  if isinstance(task, types.GeneratorType):
    value = None
    while True:
      try:
        value = _ExecuteTask(task.send(value))
      except StopIteration:
        return value
      except Exception:
        if suppress_failures:
          logging.exception('Exception raised while executing task')
          value = None
        else:
          raise
  elif isinstance(task, Task):
    if hasattr(task, "OnlyIf"):
      if not _ExecuteTask(task.OnlyIf()):
        return
    if not task.Hidden():
      print("Running", repr(task))
    run_result = task.Run()
    if run_result is not None:
      return _ExecuteTask(run_result)
  elif task is None or any(isinstance(task, t) for t in _primitive_types):
    return task
  elif hasattr(task, "__call__"):
    return task()
  else:
    raise RuntimeError("Unrecognized task: %s" % repr(task))
