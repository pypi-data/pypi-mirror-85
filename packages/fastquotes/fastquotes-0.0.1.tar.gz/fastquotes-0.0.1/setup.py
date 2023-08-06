from setuptools import setup
import os

def strip_comments(l):
    return l.split('#', 1)[0].strip()

def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f)).readlines()]))

setup(
    name="fastquotes",
    version="0.0.1",
    author="nocilantro",
    url="https://github.com/YangzhenZhao/fastquotes",
    install_requires=reqs('requirements.txt'),
    packages=["fastquotes"],
)
