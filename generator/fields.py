"""
Representations of metadata fields

"""

# Copyright 2018-2020 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import warnings
from datetime import date, datetime
from collections.abc import Iterable, Mapping

from dateutil import parser as date_parser

class Field(object):
    """Representation of a metadata field"""

    def __init__(self, name, types, path, required=False, default=None, multiple=False,
                 strict=False, reverse=None, doc=""):
        self.name = name
        if isinstance(types, (type, str)):
            self._types = (types,)
        else:
            self._types = tuple(types)
        self._resolved_types = False
        self.path = path
        self.required = required
        self.default = default
        self.multiple = multiple
        self.strict_mode = strict
        self.reverse = reverse
        self.doc = doc

    def __repr__(self):
        return "Field(name='{}', types={}, path='{}', required={}, multiple={})".format(
            self.name, self._types, self.path, self.required, self.multiple)