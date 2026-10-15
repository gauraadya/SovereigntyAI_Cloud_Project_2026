#!/usr/bin/env python3
"""
Test runner script for SovereigntyAI.
Runs the complete test suite with detailed output and exit code reporting.
"""

import unittest
import sys
from pathlib import Path

def run_all_tests():
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))

    print("=" * 65)
    print(" SovereigntyAI Compliance Framework — Automated Test Suite")
    print("=" * 65)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(project_root / "tests"), pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 65)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Successes:       {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:        {len(result.failures)}")
    print(f"Errors:          {len(result.errors)}")
    print("=" * 65)

    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
