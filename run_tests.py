#!/usr/bin/env python3
"""Lightweight test runner to execute simple test files without pytest.

This runner finds python files under `server/testing` and executes them
in an isolated namespace. Tests should use plain `assert` statements.
"""
import glob
import runpy
import sys
from pathlib import Path


def run_test_file(path: Path) -> bool:
    namespace = {"__name__": "__main__"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        exec(compile(code, str(path), "exec"), namespace)
        return True
    except AssertionError:
        print(f"FAIL: {path}")
        return False
    except Exception as e:
        print(f"ERROR: {path} -> {e}")
        return False


def main() -> int:
    base = Path(__file__).resolve().parent
    test_dir = base / "server" / "testing"
    files = sorted(test_dir.glob("test_*.py")) + sorted(test_dir.glob("*_test.py"))
    if not files:
        print("No test files found in server/testing")
        return 0

    total = len(files)
    passed = 0
    for f in files:
        ok = run_test_file(f)
        if ok:
            print(f"PASS: {f}")
            passed += 1

    print(f"\nSummary: {passed}/{total} tests passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
