from setuptools import setup, find_packages
 
 
setup(
    name = "egg-demo",
    version = "1.0.2",
    author = "zsmlinux",
    url = "http://www.zsmlinux.org",
    author_email = "zsmlinux@163.com",
    packages=find_packages(),
    entry_points={
        'cbc': ['cbcscript=src.demo:test'],
        'cbrc': ['cbcscript=src.demo:test'],
    }
)
