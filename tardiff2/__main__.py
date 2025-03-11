# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from pathlib import Path
from tardiff2.defs import DEFAULT_ATTRIBS
from tardiff2.defs import EXTENDED_ATTRIBS
from tardiff2.defs import EXTRA_ATTRIBS
from tardiff2.opts import TarDiffOpts
from tardiff2.tardiff import tardiff
import argparse
import itertools
import os


def main() -> None:
    """
    mainline

    The mainline for tardiff.
    """

    try:
        parser = argparse.ArgumentParser(prog='tardiff2')
        parser.add_argument('file', nargs='+',
            help='Files to compare against')
        parser.add_argument('--all', action='store_true',
            help='Compare all known attributes')
        parser.add_argument('--ignore-directories', '-D', action='store_true',
            help='Ignore directory entries')
        parser.add_argument('--more', '-m', action='store_true',
            help='Show a more detailed comparison of file differences')
        parser.add_argument('--names', '-n', action='store_true',
            help='Only compare file names and not attributes')
        parser.add_argument('--strip-components', type=int, default=1,
            help='Strip given number of leading components from file names')
        parser.add_argument('--[no-]ATTRIB', action='store_true',
            help='Attributes to check or ignore')

        for entry in itertools.chain(
                DEFAULT_ATTRIBS, EXTRA_ATTRIBS, EXTENDED_ATTRIBS):
            parser.add_argument(f'--{entry}', action='store_true',
                help=argparse.SUPPRESS)
            parser.add_argument(f'--no-{entry}', action='store_true',
                help=argparse.SUPPRESS)

        args = parser.parse_args()

        files = []
        for fentry in args.file:
            path = Path(os.fsdecode(fentry))
            files.append(path)

        # compile a list of attributes to use
        attribs = set(DEFAULT_ATTRIBS)

        if args.all:
            attribs.update(EXTRA_ATTRIBS)

        for entry in itertools.chain(
                DEFAULT_ATTRIBS, EXTRA_ATTRIBS, EXTENDED_ATTRIBS):
            if getattr(args, entry):
                attribs.add(entry)

        for entry in itertools.chain(
                DEFAULT_ATTRIBS, EXTRA_ATTRIBS, EXTENDED_ATTRIBS):
            if getattr(args, f'no_{entry}'):
                attribs.remove(entry)

        # compile options to use for the tardiff check
        opts = TarDiffOpts(
            attribs=sorted(attribs),
            detailed=args.more,
            ignore_dirs=args.ignore_directories,
            only_names=args.names,
            strip=args.strip_components,
        )

        # perform a difference check of all provided tar files
        has_differences, _ = tardiff(files, opts=opts)
        if has_differences:
            raise SystemExit(1)

    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()
