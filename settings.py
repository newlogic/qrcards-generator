import os
import logging


logging.root.setLevel(logging.NOTSET)
logging.basicConfig(format='%(message)s', level=logging.NOTSET)

BASE_DIR = os.path.dirname(__file__)

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
FONTS_DIR = os.path.join(TEMPLATES_DIR, 'assets', 'fonts')
LAST_SEQ_FILE = os.path.join(BASE_DIR, '.last_seq')
QR_FILE_DIR = os.path.join(BASE_DIR, 'qr_codes')

HASHIDS_SALT = os.environ.get("HASHIDS_SALT", '$6$O1UAtet1RQADaQRI')
HASHIDS_MIN_LENGTH = 12

SELF_REGISTRATION_BASE_URL = os.environ.get("SELF_REGISTRATION_BASE_URL", "https://ukr.reg.scope.wfp.org/")
SELF_REGISTRATION_URL = os.environ.get("SELF_REGISTRATION_URL", f"{SELF_REGISTRATION_BASE_URL}ukr/code/?code=")
