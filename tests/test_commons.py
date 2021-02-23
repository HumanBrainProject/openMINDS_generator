#   Copyright (c) 2018, EPFL/Human Brain Project PCO
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
import os
import zipfile
from io import BytesIO
from unittest import TestCase


#   limitations under the License.
from pip._vendor import requests

from generator.generate_json_schema import JsonSchemaGenerator


class TestGenerator(TestCase):

    def _load_core_from_github(self):
        r = requests.get("https://github.com/HumanBrainProject/openMINDS_core/releases/download/v3.0.0/core_schema-templates_v3.0.0.zip", stream=True)
        z = zipfile.ZipFile(BytesIO(r.content))
        z.extractall(os.path.join(os.path.dirname(os.path.realpath(__file__)), "expanded"))

    def test_generate_json_schema(self):
        self._load_core_from_github()

        JsonSchemaGenerator("test").generate()
