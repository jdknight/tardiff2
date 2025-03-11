# SPDX-License-Identifier: BSD-2-Clause
# Copyright jdknight

# tar file attributes to check by default
DEFAULT_ATTRIBS = [
    'devmajor',
    'devminor',
    'gid',
    'gname',
    'linkname',
    'mode',
    'size',
    'type',
    'uid',
    'uname',
]

# other supported attributes to check for users requesting all attributes
EXTRA_ATTRIBS = [
    'chksum',
    'mtime',
    'offset',
    'offset_data',
]

# extended attributes that a user can use if explicitly opted for
EXTENDED_ATTRIBS = [
    'pax_headers',
]
