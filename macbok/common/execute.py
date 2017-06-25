from __future__ import print_function

import types
from macbok.common.task import Task

_primitive_types = (bool, int, type(u""), type(b""), dict)


def execute(task_generator):
  """Execute a task generator.

  This is the main entry point for macbok. Call this function with the function
  that configures the system.

  Args:
    task_generator: A generator that yields configuration tasks.
  """
  _execute_task(task_generator())


def _execute_task(task):
  if isinstance(task, types.GeneratorType):
    value = None
    while True:
      try:
        value = _execute_task(task.send(value))
      except StopIteration:
        return value
  elif isinstance(task, Task):
    if hasattr(task, "onlyif"):
      if not _execute_task(task.onlyif()):
        return
    if not task.is_hidden():
      print("Running", repr(task))
    run_result = task.run()
    if run_result is not None:
      return _execute_task(run_result)
  elif task is None or any(map(lambda t: isinstance(task, t), _primitive_types)):
    return task
  elif hasattr(task, "__call__"):
    return task()
  else:
    raise RuntimeError("Unrecognized task: %s" % repr(task))
