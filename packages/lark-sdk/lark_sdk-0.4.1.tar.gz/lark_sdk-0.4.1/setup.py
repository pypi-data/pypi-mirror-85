#!/usr/bin/env python
# coding: utf-8
"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = []

test_requirements = [
    "pytest>=3",
]

setup(
    author="holegots",
    author_email="gaopengyang@bytedance.com",
    python_requires=">=2.7,!=3.0.*,!=3.1.*",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="A python sdk that implements all the features of the official documentation (not implemented).",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    include_package_data=True,
    keywords="lark_sdk",
    name="lark_sdk",
    packages=find_packages(include=["lark_sdk", "lark_sdk.*"]),
    test_suite="tests",
    use_2to3=True,
    tests_require=test_requirements,
    url="https://github.com/fuergaosi233/lark_sdk",
    version="0.4.1",
    zip_safe=False,
)
