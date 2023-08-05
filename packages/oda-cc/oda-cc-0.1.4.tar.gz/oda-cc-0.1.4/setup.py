from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name="oda-cc",
        version = "0.1.4",
        author = "Volodymyr Savchenko",
        author_email = "contact@volodymyrsavchenko.com",
        description = (""
                       ""),
        license = "MIT",
        keywords = "oda",
        url = "http://packages.python.org/oda-cc",
        packages=['odacc', 'tests'],
        long_description=read('README'),
        entry_points={
           "console_scripts": [
                 "oda-cc = odacc.cli:cli"
           ]
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
        ],
        install_requires=[
            "click",
        ]
)
