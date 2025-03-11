# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from pathlib import Path
from tempfile import TemporaryDirectory
import os
import unittest


class TardiffTestCase(unittest.TestCase):
    """
    a tardiff unit test case

    Provides a `unittest.TestCase` implementation that tardiff unit tests
    should inherit from. This test class provides the following capabilities:

    - Prepares a temporary working directory to allow creating test tar files
      into that will be automatically deleted.
    """

    def run(self, result: unittest.TestResult | None = None) -> None:
        """
        run the test

        Run the test, collecting the result into the TestResult object passed
        as result. See `unittest.TestCase.run()` for more details.

        Args:
            result (optional): the test result to populate
        """

        with TemporaryDirectory(prefix='.tardiff-') as tmpdir:
            owd = Path.cwd()
            try:
                os.chdir(tmpdir)
                super().run(result)
            finally:
                os.chdir(owd)
