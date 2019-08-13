import cProfile
import mypyc_black
from functools import partial, wraps
from typing import Tuple
from pathlib import Path

fs = partial(mypyc_black.format_str, mode=mypyc_black.FileMode())
THIS_FILE = Path(__file__)
# PATH_TO_ORIG_TESTS = Path("/Users/skalapatapu/black/tests/test_black.py")
THIS_DIR = THIS_FILE.parent
EMPTY_LINE = "# EMPTY LINE WITH WHITESPACE" + " (this comment will be removed)"

def read_data(name: str, data: bool = True) -> Tuple[str, str]:
    """read_data('test_name') -> 'input', 'output'"""
    if not name.endswith((".py", ".pyi", ".out", ".diff")):
        name += ".py"
    _input: List[str] = []
    _output: List[str] = []
    base_dir = THIS_DIR / "data" if data else THIS_DIR
    with open(base_dir / name, "r", encoding="utf8") as test:
        lines = test.readlines()
    result = _input
    for line in lines:
        line = line.replace(EMPTY_LINE, "")
        if line.rstrip() == "# output":
            result = _output
            continue

        result.append(line)
    if _input and not _output:
        # If there's no output marker, treat the entire file as already pre-formatted.
        _output = _input[:]
    return "".join(_input).strip() + "\n", "".join(_output).strip() + "\n"

source, expected = read_data("black", data=False)

def test_black():
	actual = mypyc_black.format_str(src_contents = source, mode = mypyc_black.FileMode())
	# actual = fs(source)
	# mypyc_black.assert_equivalent(source, actual)
	# mypyc_black.assert_stable(source, actual, mypyc_black.FileMode())

cProfile.run('test_black()', sort = 'tottime')