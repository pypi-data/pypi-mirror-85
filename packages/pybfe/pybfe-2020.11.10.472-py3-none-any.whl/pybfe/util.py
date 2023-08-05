#   Copyright 2019 Intentionet
#
#   Licensed under the proprietary License included with this package;
#   you may not use this file except in compliance with the License.
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""Generic utility functions for PybfE."""
import os
import random
import tempfile
import uuid
import zipfile
from io import BytesIO
from typing import BinaryIO, Optional

# Max length for snapshot/network names
_MAX_NAME_LEN = 150

# Minimum timestamp supported by ZIP format
# See issue https://bugs.python.org/issue34097
_MIN_ZIP_TIMESTAMP = 315561600.0


def rand_int() -> int:
    """Generate random 32bit int."""
    return random.randrange(-2147483648, 2147483647)  # 32bit signed int range


def get_uuid() -> str:
    """Generate and return a UUID as a string."""
    return str(uuid.uuid4())


def read_zip(path: Optional[str]) -> Optional[bytes]:
    """Read zip data for specified zip or path, zipping path if necessary."""
    if path is None:
        return None

    if os.path.isdir(path):
        fd = zip_from_dir(path)
        # Seek to origin so the full zip data is read
        fd.seek(0)
        return fd.read()
    elif os.path.isfile(path):
        if not zipfile.is_zipfile(path):
            raise ValueError("{} is not a valid zip file".format(path))
        with open(path, "rb") as fd:
            return fd.read()
    else:
        raise ValueError("Supplied path does not exist: {}".format(path))


def zip_from_file_text(text: str, filename: str) -> BinaryIO:
    """Creates an in-memory zip file for a single file snapshot."""
    data = BytesIO()
    with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED, False) as zf:
        zf.writestr(filename, text)
    return data


def zip_from_dir(dir_path: str) -> BinaryIO:
    """Creates an in-memory zip file for specified filesystem directory."""
    data = BytesIO()
    with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED, False) as zf:
        rel_root = os.path.abspath(os.path.join(dir_path, os.path.pardir))

        for root, _dirs, files in os.walk(dir_path):
            zf.write(root, os.path.relpath(root, rel_root), zipfile.ZIP_STORED)
            for f in files:
                filename = os.path.join(root, f)
                arcname = os.path.join(os.path.relpath(root, rel_root), f)

                # Zipped files must be from 1980 or later
                # So copy any file older than that to a tempfile to bump the timestamp
                if os.path.getmtime(filename) < _MIN_ZIP_TIMESTAMP:
                    with tempfile.NamedTemporaryFile("w+b") as temp_file, open(
                        filename, "rb"
                    ) as file_src:
                        temp_file.write(file_src.read())
                        temp_file.flush()
                        zf.write(temp_file.name, arcname)
                else:
                    zf.write(filename, arcname)
    return data


def text_with_platform(text: str, platform: Optional[str]) -> str:
    """Returns the text with platform prepended if needed."""
    if platform is None:
        return text
    p = platform.strip().lower()
    return "!RANCID-CONTENT-TYPE: {}\n{}".format(p, text)
