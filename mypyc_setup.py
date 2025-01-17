# Copyright (C) 2018 Łukasz Langa
import ast
import re
from setuptools import setup
import sys
import os

assert sys.version_info >= (3, 6, 0), "black requires Python 3.6+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent


def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


def get_version() -> str:
    black_py = CURRENT_DIR / "mypyc_black.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(black_py, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))

USE_MYPYC = False
# To compile with mypyc, a mypyc checkout must be present on the PYTHONPATH
if len(sys.argv) > 1 and sys.argv[1] == '--use-mypyc':
    sys.argv.pop(1)
    USE_MYPYC = True
if os.getenv('BLACK_USE_MYPYC', None) == '1':
    USE_MYPYC = True

if USE_MYPYC:
    mypyc_targets = ['mypyc_black.py']

    from mypyc.build import mypycify, MypycifyBuildExt
    opt_level = os.getenv('MYPYC_OPT_LEVEL', '3')
    ext_modules = mypycify(
        mypyc_targets,
        ['--config-file=mypy.ini'],
        opt_level=opt_level,
        # Use multi-file compliation mode on windows because without it
        # our Appveyor builds run out of memory sometimes.
        multi_file=sys.platform == 'win32',
    )
else:
    ext_modules = []

setup(
    name="black",
    version=get_version(),
    description="The uncompromising code formatter.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="automation formatter yapf autopep8 pyfmt gofmt rustfmt",
    author="Łukasz Langa",
    author_email="lukasz@langa.pl",
    url="https://github.com/python/black",
    license="MIT",
    ext_modules = ext_modules,
    py_modules=["mypyc_black", "blackd",],
    packages=["blib2to3", "blib2to3.pgen2"],
    package_data={"blib2to3": ["*.txt"]},
    python_requires=">=3.6",
    zip_safe=False,
    install_requires=[
        "click>=6.5",
        "attrs>=18.1.0",
        "appdirs",
        "toml>=0.9.4",
        "typed-ast>=1.3.1",
    ],
    extras_require={"d": ["aiohttp>=3.3.2", "aiohttp-cors"]},
    test_suite="tests.mypyc_test_black",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={
        "console_scripts": [
            "black=mypyc_black:patched_main",
            "blackd=blackd:patched_main [d]",
        ]
    },
)
