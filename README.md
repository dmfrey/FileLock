FileLock
========

A file locking mechanism that has context-manager support so 
you can use it in a with statement. This should be relatively cross
compatible as it doesn't rely on msvcrt or fcntl for the locking.

Usage
=====

```python
from filelock import FileLock

with FileLock("myfile.txt"):
    # work with the file as it is now locked
    print("Lock acquired.")
```


Originally posted at http://www.evanfosmark.com/2009/01/cross-platform-file-locking-support-in-python/
