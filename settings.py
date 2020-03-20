"""
   Copyright 2020 Newlogic

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import os
import logging


logging.root.setLevel(logging.NOTSET)
logging.basicConfig(format='%(message)s', level=logging.NOTSET)

BASE_DIR = os.path.dirname(__file__)

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
FONTS_DIR = os.path.join(TEMPLATES_DIR, 'assets', 'fonts')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
QR_FILE_DIR = os.path.join(OUTPUT_DIR, 'qr_codes')

PREVIEW = False
HASHIDS_SALT = os.environ.get("HASHIDS_SALT", 'TOBECHANGED')
HASHIDS_MIN_LENGTH = 5
