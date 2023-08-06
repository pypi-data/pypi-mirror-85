#!/usr/bin/env python
# coding=utf-8
import os

import setuptools

with open("README.md", "r", encoding="UTF-8") as f:
    long_desc = f.read()

with open("LICENSE", "r", encoding="UTF-8") as f:
    license_txt = f.read()

setuptools.setup(
    name="alphamini",
    version="1.1.0",
    author='logic.peng',
    author_email='logic.peng@ubtrobot.com',
    description="python sdk for ubtech alpha mini robot",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="GPLv3",
    python_requires='>=3.7',
    # url="",
    packages=setuptools.find_packages(exclude=["*.test", "*.test.*"]),  # 排除掉测试包
    # packages=setuptools.find_namespace_packages(where=os.curdir + "/mini"),
    # packages=['mini'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'setup_py_pkg = mini.tool.script.cli:cli_setup_py_pkg',
            'install_py_pkg = mini.tool.script.cli:cli_install_py_pkg',
            'uninstall_py_pkg = mini.tool.script.cli:cli_uninstall_py_pkg',
            'run_py_pkg = mini.tool.script.cli:cli_run_py_pkg',
            'run_cmd = mini.tool.script.cli:cli_run_cmd',
            'query_py_pkg = mini.tool.script.cli:cli_show_py_pkg',
            'list_py_pkg = mini.tool.script.cli:cli_list_py_pkg',
            'adb_enable = mini.tool.script.cli:cli_adb_enable',
            'adb_disable = mini.tool.script.cli:cli_adb_disable',
        ],
    },
    install_requires=[
        'websockets',
        'ifaddr',
        'protobuf',
        'click',
    ],
    zip_safe=False
)
