from threading import Lock


class Task(object):
    _task_locks = {}
    _task_lock_lock = Lock()

    def task_lock(self):
        """
        Retrieves a lock, which is shared between all members of a class. Each different subclass
        of Task has a different task_lock. The task lock should be used to make sure that onlyl one
        instance of the task is running at a time.

        """
        with self._task_lock_lock:
            if self.__class__ not in self._task_locks:
                lock = Lock()
                self._task_locks[self.__class__] = lock
            else:
                lock = self._task_locks[self.__class__]
            return lock

    def is_hidden(self):
        """
        Gives sub-classes the ability to make themselves hidden nodes, which are not shown to the
        user.

        """
        return False
