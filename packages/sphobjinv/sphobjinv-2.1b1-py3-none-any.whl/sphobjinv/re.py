r"""*Helper regexes for* ``sphobjinv``.

``sphobjinv`` is a toolkit for manipulation and inspection of
Sphinx |objects.inv| files.

**Author**
    Brian Skinn (bskinn@alum.mit.edu)

**File Created**
    5 Nov 2017

**Copyright**
    \(c) Brian Skinn 2016-2020

**Source Repository**
    https://github.com/bskinn/sphobjinv

**Documentation**
    https://sphobjinv.readthedocs.io/en/latest

**License**
    The MIT License; see |license_txt|_ for full license terms

**Members**

"""

import re

from sphobjinv.data import DataFields
from sphobjinv.enum import HeaderFields


#: Compiled |re| |bytes|  pattern for comment lines in decompressed
#: inventory files
pb_comments = re.compile(b"^#.*$", re.M)

#: Compiled |re| |bytes| pattern for project line
pb_project = re.compile(
    r"""
    ^                        # Start of line
    [#][ ]Project:[ ]        # Preamble
    (?P<{}>.*?)              # Lazy rest of line is the project name
    \r?$                     # Ignore possible CR at EOL
    """.format(
        HeaderFields.Project.value
    ).encode(
        encoding="utf-8"
    ),
    re.M | re.X,
)

#: Compiled |re| |bytes| pattern for version line
pb_version = re.compile(
    r"""
    ^                        # Start of line
    [#][ ]Version:[ ]        # Preamble
    (?P<{}>.*?)              # Lazy rest of line is the version
    \r?$                     # Ignore possible CR at EOL
    """.format(
        HeaderFields.Version.value
    ).encode(
        encoding="utf-8"
    ),
    re.M | re.X,
)

#: Regex pattern string used to compile
#: :data:`~sphobjinv.re.p_data` and
#: :data:`~sphobjinv.re.pb_data`
ptn_data = (
    r"""
    ^                        # Start of line
    (?P<{0}>[^#]\S+)         # --> Name
    \s+                      # Dividing space
    (?P<{1}>\w+)             # --> Domain
    :                        # Dividing colon
    (?P<{2}>\w+)             # --> Role
    \s+                      # Dividing space
    (?P<{3}>\S+)             # --> Priority
    \s+                      # Dividing space
    (?P<{4}>\S+)             # --> URI
    \s+                      # Dividing space
    (?P<{5}>.+?)             # --> Display name, lazy b/c possible CR
    \r?$                     # Ignore possible CR at EOL
    """
).format(
    DataFields.Name.value,
    DataFields.Domain.value,
    DataFields.Role.value,
    DataFields.Priority.value,
    DataFields.URI.value,
    DataFields.DispName.value,
)

#: Compiled |re| |bytes| regex pattern for data lines in |bytes| decompressed
#: inventory files
pb_data = re.compile(ptn_data.encode(encoding="utf-8"), re.M | re.X)

#: Compiled |re| |str| regex pattern for data lines in |str| decompressed
#: inventory files
p_data = re.compile(ptn_data, re.M | re.X)
