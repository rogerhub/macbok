import collections
import threading


class Task(object):
  _task_locks = collections.defaultdict(threading.Lock)
  _task_locks_lock = threading.Lock()

  def task_lock(self):
    """Returns the task lock for this class.

    Task locks are shared between all members of a class. The task lock should
    be used to make sure that only one instance of the task is running at a
    time.
    """
    with self._task_locks_lock:
      return self._task_locks[self.__class__]

  def is_hidden(self):
    """Returns whether the task should be hidden from the user."""
    return False
