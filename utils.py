import os

from hashids import Hashids

import settings


def get_last_seq():
    last_seq = 0
    if os.path.isfile(settings.LAST_SEQ_FILE):
        with open(settings.LAST_SEQ_FILE, 'r') as f:
            last_seq = f.read()
    return int(last_seq)


def save_last_seq(last_seq):
    with open(settings.LAST_SEQ_FILE, 'w') as f:
        f.write(str(last_seq))


def unique_id_generator(last_seq, upper_bound_id):
    # Use last_seq from stored file if exists
    start_seq = last_seq + 1

    hashids = Hashids(salt=settings.HASHIDS_SALT, min_length=settings.HASHIDS_MIN_LENGTH)

    for i in range(start_seq, upper_bound_id+start_seq):
        yield (i, hashids.encode(i))
