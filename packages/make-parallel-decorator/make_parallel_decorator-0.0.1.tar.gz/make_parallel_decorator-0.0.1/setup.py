from setuptools import setup

setup(
    name='make_parallel_decorator',
    version="0.0.1",
    description='This is a decorator that can be used to convert a normal function into multi threaded',
    py_modules=['MakeParallel'],
    package_dir={'': 'src'},
    classifiers=[]
)