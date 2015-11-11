import types
from macbok.common.task import Task


_primitive_types = (bool, int, basestring)


def execute(task_generator):
    """
    The main entry point. This function runs a task generator sequentially. The argument should be a
    function that returns the task generator.

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
            print "Running", repr(task)
        run_result = task.run()
        if run_result is not None:
            return _execute_task(run_result)
    elif task is None or any(map(lambda t: isinstance(task, t), _primitive_types)):
        return task
    elif hasattr(task, "__call__"):
        return task()
    else:
        raise RuntimeError("Unrecognized task: %s" % repr(task))
