# -*- coding: utf-8 -*-
import os
import sys
from io import open
from setuptools import setup
from setuptools import find_packages

def get_version(template_text):
    for line in template_text.splitlines():
        line = line.strip()
        if line.startswith("version"):
            _, name = line.split("=")
            name = name.strip()
            return name[1:-1]
    return ""

import lua_resty_fastutils
here = os.path.abspath(os.path.dirname(__file__))

rockspec_filename = os.path.abspath(os.path.join(os.path.dirname(lua_resty_fastutils.__file__), "./src/.rockspec"))
with open(rockspec_filename, "r", encoding="utf-8") as fobj:
    version = get_version(fobj.read()).replace("-", ".")
print("rockspec_filename=", rockspec_filename)
print("version=", version)

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="lua-resty-fastutils",
    version=version,
    description="Collection of simple utils.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    url="https://github.com/zencore-cn/zencore-issues",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=[],
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["manage_lua_resty_fastutils", "lua_resty_fastutils"],
    entry_points={
        "console_scripts": [
            "manage-lua-resty-fastutils = manage_lua_resty_fastutils:manager",
        ]
    },
    zip_safe=False,
    include_package_data=True,
)
