# About

    A file locking mechanism that has context-manager support so 
    you can use it in a with statement. This should be relatively cross
    compatible as it doesn't rely on msvcrt or fcntl for the locking.
    

    Originally posted at http://www.evanfosmark.com/2009/01/cross-platform-file-locking-support-in-python/
# Usage
```python
from filelock import FileLock

with FileLock("myfile.txt.lock"):
    print("Lock acquired.")
    with open("myfile.txt"):
        # work with the file as it is now locked
```
