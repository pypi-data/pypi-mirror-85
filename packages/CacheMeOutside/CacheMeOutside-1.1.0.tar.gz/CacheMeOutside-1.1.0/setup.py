from setuptools import setup

setup(
    name = "CacheMeOutside",
    version = "1.1.0",
    author = "Jack McKeown",
    author_email = "jackamckeown+cmo@gmail.com",
    description = ("A simple library which wraps arbitrary functions with (optionally) persistent caching."),
    license = "BSD",
    keywords = "cache persistent simple",
    py_modules=["cacheMeOutside"],
    setup_requires=['wheel']
)
