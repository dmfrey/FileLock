from distutils.core import setup

setup(
    name='FileLock',
    version='0.1.0',
    author='dmfrey',
    author_email='dmfrey@gmail.com',
    packages=['filelock','filelock.test'],
    url='http://test.com',
    license='LICENSE.txt',
    description='File locking library',
    long_description=open('README.txt').read()
)
