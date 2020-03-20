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

from hashids import Hashids

import settings


def get_last_seq_file(dir):
    return os.path.join(dir, '.last_seq')

def get_last_seq(dir=settings.BASE_DIR):
    last_seq = 0
    last_seq_file = get_last_seq_file(dir)
    if os.path.isfile(last_seq_file):
        with open(last_seq_file, 'r') as f:
            last_seq = f.read()
    return int(last_seq)


def save_last_seq(last_seq, dir=settings.BASE_DIR):
    last_seq_file = get_last_seq_file(dir)
    with open(last_seq_file, 'w') as f:
        f.write(str(last_seq))


def unique_id_generator(last_seq, upper_bound_id):
    # Use last_seq from stored file if exists
    start_seq = last_seq + 1

    hashids = Hashids(salt=settings.HASHIDS_SALT, min_length=settings.HASHIDS_MIN_LENGTH, alphabet='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')

    for i in range(start_seq, upper_bound_id+start_seq):
        yield (i, hashids.encode(i))
