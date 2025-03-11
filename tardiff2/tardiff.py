# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

from __future__ import annotations
from prettytable import PrettyTable
from tardiff2.opts import TarDiffOpts
from typing import Any
from typing import TYPE_CHECKING
import stat
import tarfile

if TYPE_CHECKING:
    from pathlib import Path


def tardiff(files: list[Path], *, opts: TarDiffOpts | None = None,
        quiet: bool = False) -> tuple[bool, dict[Path, Any]]:
    """
    perform a tar-diff

    Args:
        files: the list of tar files to compare
        opts (optional): the runtime options to consider
        quiet (optional): whether to dump results to the standard output stream

    Returns:
        tuple of the difference state and result data

    Raises:
        TardiffError
    """

    if not opts:
        opts = TarDiffOpts()

    if opts.strip < 0:
        msg = 'invalid strip-components value'
        raise TardiffInvalidStripCountError(msg)

    # unique file list
    files = list(dict.fromkeys(files))

    # should have at least two files
    if len(files) < 2:
        msg = 'need at least two files'
        raise TardiffRequireTwoFilesError(msg)

    # verify each file exists
    for file in files:
        if not file.is_file():
            msg = f'file is missing: {file}'
            raise TardiffFileMissingError(msg)

        if not tarfile.is_tarfile(file):
            msg = f'file is not a tar-file: {file}'
            raise TardiffFileInvalidError(msg)

    # compile a list of tar-file entries with tracked data
    entries: list[TarEntry] = []
    for file in files:
        with tarfile.open(file) as tar:
            entry = TarEntry(file)

            for member in tar.getmembers():
                parts = member.name.split('/', opts.strip)
                if len(parts) <= opts.strip:
                    continue

                new_name = parts[opts.strip]
                if member.isdir():
                    if opts.ignore_dirs:
                        continue
                    new_name += '/'

                entry.names.add(new_name)
                entry.mapping[new_name] = member

            entries.append(entry)

    entry0 = entries[0]

    # prepare diff results to capture
    has_differences = False
    mdb: dict[str, Any] = {}
    results: dict[Path, Any] = {}
    for entry in entries:
        results[entry.path] = {
            'extra': set(),
            'missing': set(),
            'modified': {},
        }

    # compile a list of files that exist in any of the provided archives as
    # well as a common set of files that exist in all provided archives
    all_names = entry0.names.copy()
    common_names = entry0.names.copy()
    for entry in entries[1:]:
        all_names.update(entry.names)
        common_names.intersection_update(entry.names)

    # track missing and extra files per file entry
    for entry in entries:
        missing_entries = all_names.difference(entry.names)
        extra_entries = entry.names.difference(common_names)

        results[entry.path]['missing'].update(missing_entries)
        results[entry.path]['extra'].update(extra_entries)

        if missing_entries or extra_entries:
            has_differences = True

    # look for modified files between each tarfile entry
    if not opts.only_names:
        for name in common_names:
            track: dict[Path, dict[str, str]] = {}
            base_tar_nfo = entry0.mapping[name]

            for entry in entries[1:]:
                node_tar_nfo = entry.mapping[name]

                # compare each attribute for differences
                for ac in opts.attribs:
                    base_val = getattr(base_tar_nfo, ac)
                    node_val = getattr(node_tar_nfo, ac)

                    if base_val != node_val:
                        if ac == 'mode':
                            base_val = _tardiff_modestr(base_val)
                            node_val = _tardiff_modestr(node_val)

                        track.setdefault(entry0.path, {})[ac] = base_val
                        track.setdefault(entry.path, {})[ac] = node_val

                # if we tracked any differences between this file as our base
                # entry, track in the modified database and our result set
                # the detected attribute differences
                if entry.path in track:
                    mdb.setdefault(name, {})[entry.path] = track[entry.path]
                    results[entry.path]['modified'][name] = track[entry.path]

            # if we tracked any differences, also include the base entry in
            # our modified database and result set
            if track:
                mdb.setdefault(name, {})[entry0.path] = track[entry0.path]
                results[entry0.path]['modified'][name] = track[entry0.path]
                has_differences = True

    # completed looking for differences; print results if configured for it
    if has_differences and not quiet:
        _tardiff_results(results, mdb, opts)

    # return the state to the caller
    return has_differences, results


def _tardiff_results(results: dict[Path, Any], modified_db: dict[str, Any],
        opts: TarDiffOpts) -> None:
    """
    print tardiff results to the standard output stream

    Args:
        results: the results of a tar-diff event
        modified_db: a more detailed modified database
        opts: the runtime options to consider
    """

    has_modified = False

    for entry, data in results.items():
        print()
        print(f'{entry.name}]')

        if data['extra']:
            print('  (extra entries)')
            for file in sorted(data['extra']):
                print(f'    {file}')

        if data['missing']:
            print('  (missing entries)')
            for file in sorted(data['missing']):
                print(f'    {file}')

        if data['modified']:
            has_modified = True

            if not opts.detailed:
                print('  (modified entries)')
                for file in sorted(data['modified']):
                    print(f'    {file}')

    if has_modified and opts.detailed:
        table = PrettyTable()

        # compile columns using file names
        field_names = ['Modified File']
        for mdb_entries in modified_db.values():
            field_names.extend(entry.name for entry in mdb_entries)
            break

        # unique column names
        seen_field_names: dict[str, int] = {}
        unique_field_names: list[str] = []

        for field_name in field_names:
            if field_name in seen_field_names:
                seen_field_names[field_name] += 1
                idx = seen_field_names[field_name]
                new_field_name = f'{field_name} ({idx})'
            else:
                seen_field_names[field_name] = 0
                new_field_name = field_name

            unique_field_names.append(new_field_name)

        # apply columns and other options
        table.field_names = unique_field_names
        table.align['Modified File'] = 'l'

        # build rows; the first column being the (stripped) file name entry
        # and trailing columns being the detected attributes that have a
        # difference compared to all the other files
        for fname, mdb_entries in sorted(modified_db.items()):
            values = [fname]
            values.extend(_attribstr(entry) for entry in mdb_entries.values())

            table.add_row(values, divider=True)

        print()
        print(table)


def _attribstr(value: dict[str, str]) -> str:
    return '\n'.join('{}={}'.format(*o) for o in value.items())


def _tardiff_modestr(value: int) -> str:
    """
    converts a tar member mode value into a mode string

    Args:
        value: the mode value

    Returns:
        the mode string
    """
    return stat.filemode(int(oct(value), 8))[1:]


class TarEntry:
    def __init__(self, path: Path) -> None:
        """
        tardiff tar entry

        Holds a series of tracked results for a given tarfile tracked in
        a tardiff invoke.

        Args:
            path: the path of the file

        Attributes:
            mapping: a map from a file name entry to a cached TarInfo instance
            names: the set of detected filenames in the tarfile
            path: the path of the file
        """
        self.mapping: dict[str, tarfile.TarInfo] = {}
        self.names: set[str] = set()
        self.path = path


class TardiffError(Exception):
    pass


class TardiffFileInvalidError(TardiffError):
    pass


class TardiffFileMissingError(TardiffError):
    pass


class TardiffInvalidStripCountError(TardiffError):
    pass


class TardiffRequireTwoFilesError(TardiffError):
    pass
