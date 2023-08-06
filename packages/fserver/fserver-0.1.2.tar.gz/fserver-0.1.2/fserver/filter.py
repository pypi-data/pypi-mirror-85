try:
    from urllib.parse import unquote, quote
except:
    from urllib import unquote, quote

# from werkzeug.utils import secure_filename
# from werkzeug.utils import text_type
from werkzeug import utils

text_type = utils.text_type
import sys

PY2 = sys.version_info[0] == 2

import os
import re

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = (
    "CON",
    "AUX",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "LPT1",
    "LPT2",
    "LPT3",
    "PRN",
    "NUL",
)




s = '魔兽.txt'
# s = quote(s)
print(s)
s = secure_filename(s)
print(s)
