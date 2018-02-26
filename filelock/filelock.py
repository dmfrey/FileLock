
# Library imports
import os
import time
import errno


# Exceptions
class FileLockException(Exception):
    pass


class FileLock(object):

    def __init__(self, file_name: str, timeout: float=10, delay: float=0.05):
        """
        A file locking mechanism that has context-manager support so
        you can use it in a with statement. This should be relatively cross
        compatible as it doesn't rely on msvcrt or fcntl for the locking.

        Specify the file to lock and optionally the maximum timeout and the delay
        between each attempt to lock.
        :param file_name:
        :param timeout:
        :param delay:
        """
        self._is_locked = False
        self.lockfile = os.path.join(os.getcwd(), "%s.lock" % file_name)
        self.file_name = file_name
        self.timeout = timeout
        self.delay = delay

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    def acquire(self):
        """
        Acquire the lock, if possible. If the lock is in use, it check again
        every `wait` seconds. It does this until it either gets the lock or
        exceeds `timeout` number of seconds, in which case it throws
        an exception.

        :return:
        """
        # Fetch start time (now)
        start_time = time.time()

        # Start looping to try and get the file lock
        while True:

            # Try to create the lock file and open it
            try:
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)

            # Catch all OSError exceptions
            except OSError as e:

                # If the OSError is anything other than "file already exists error", reraise
                if e.errno != errno.EEXIST:
                    raise

                # If we have exceeded the timeout duration, raise an exception
                if start_time + self.timeout > time.time():
                    raise FileLockException("Timeout occured.")

                # We haven't timed out yet, but still can't get the lock.
                # Sleep for the delay duration, before we loop round and try again
                time.sleep(self.delay)

        # If we get here, we finally managed to get the lock. Set the flag true
        self._is_locked = True

    def release(self, force_release: bool=False):
        """
        Get rid of the lock by deleting the lockfile.
        When working in a `with` statement, this gets automatically
        called at the end.
        Setting force_release to true deletes the lock file, regardless who made it
        :return:
        """
        # If we have the lock, delete the lock file and clear the is locked flag
        if self.is_locked or force_release:
            os.close(self.fd)
            os.unlink(self.lockfile)
            self._is_locked = False

    def __enter__(self):
        """
        Activated when used in the with statement.
        Should automatically acquire a lock to be used in the with block.
        :return:
        """
        # If we don't have the lock, get it, then return this instance
        if not self.is_locked:
            self.acquire()
        return self

    def __exit__(self, *args, **kwargs):
        """
        Activated at the end of the with statement.
        It automatically releases the lock if it isn't locked.
        :return:
        """
        # If we have the lock, release it
        if self._is_locked:
            self.release()

    def __del__(self):
        """
        Make sure that the FileLock instance doesn't leave a lockfile
        lying around.
        :return:
        """
        self.release()