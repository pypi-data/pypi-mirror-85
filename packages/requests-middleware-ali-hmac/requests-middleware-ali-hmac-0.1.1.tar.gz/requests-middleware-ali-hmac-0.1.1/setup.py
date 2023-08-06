# encoding=utf-8
from __future__ import print_function
from setuptools import setup, find_packages
from os import path as os_path
import sys


# 读取文件内容
def read_file(filename):
    with open(os_path.join(os_path.abspath(os_path.dirname(__file__)), filename)) as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name="requests-middleware-ali-hmac",
    version="0.1.1",
    author="xiaxichen",  # 作者名字
    python_requires='>=2.7.0',  # python环境,
    author_email="xiaxichen1@163.com",
    description="requests middleware for generate signature amap apistore",
    long_description=read_file('README.md'),  # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    license="MIT",
    url="",  # github地址或其他地址
    packages=find_packages(),
    py_modules=['requests_middleware_ali_hmac'],  # 要打包哪些，.py文件，
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    install_requires=read_requirements('req.txt'),
    zip_safe=True,
)
