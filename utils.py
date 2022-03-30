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
