import sys


def is_under_unittest() -> bool:
    return "unittest" in sys.modules.keys()
