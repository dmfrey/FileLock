from distutils.core import setup

setup(
    name='FileLock',
    version='0.1.0',
    author='Evan Fosmark',
    author_email='me@evanfosmark.com',
    packages=['filelock','filelock.test'],
    url='https://github.com/dmfrey/FileLock',
    license='LICENSE.txt',
    description='File locking library',
    long_description=open('README.txt').read()
)
