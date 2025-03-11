# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.opts import TarDiffOpts
from tardiff2.tardiff import TardiffFileInvalidError
from tardiff2.tardiff import TardiffFileMissingError
from tardiff2.tardiff import TardiffInvalidStripCountError
from tardiff2.tardiff import TardiffRequireTwoFilesError
from tardiff2.tardiff import tardiff
import unittest


class TestOpts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        tests_dir = Path(__file__).parent.resolve()
        cls.assets_dir = tests_dir / 'assets'

    def test_opts_default_strip_one(self) -> None:
        opts = TarDiffOpts()
        self.assertEqual(opts.strip, 1)

    def test_opts_tardiff_invalid_strip(self) -> None:
        opts = TarDiffOpts()
        opts.strip = -2

        with self.assertRaises(TardiffInvalidStripCountError):
            tardiff([], opts=opts)

    def test_opts_tardiff_missing(self) -> None:
        files = [
            self.assets_dir / 'example.tar',
            self.assets_dir / 'this-file-does-not-exist',
        ]

        with self.assertRaises(TardiffFileMissingError):
            tardiff(files)

    def test_opts_tardiff_non_tarfile(self) -> None:
        files = [
            self.assets_dir / 'example.tar',
            self.assets_dir / 'non-tar-file.txt',
        ]

        with self.assertRaises(TardiffFileInvalidError):
            tardiff(files)

    def test_opts_tardiff_not_enough_files(self) -> None:
        files = []
        with self.assertRaises(TardiffRequireTwoFilesError):
            tardiff(files)

        files = [
            self.assets_dir / 'example.tar',
        ]
        with self.assertRaises(TardiffRequireTwoFilesError):
            tardiff(files)

        files = [
            self.assets_dir / 'example.tar',
            self.assets_dir / 'example.tar',
        ]
        with self.assertRaises(TardiffRequireTwoFilesError):
            tardiff(files)
