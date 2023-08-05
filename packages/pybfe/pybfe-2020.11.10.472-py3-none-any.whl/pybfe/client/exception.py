#   Copyright 2020 Intentionet
#
#   Licensed under the proprietary License included with this package;
#   you may not use this file except in compliance with the License.
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""Contains special exceptions thrown by BfE."""
from typing import Any


class Response(object):
    """requests-like Response object supporting status_code"""

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code  # type: int


class HTTPError(Exception):
    """requests-like HTTPError containing Response"""

    def __init__(self, status_code: int, *args: Any, **kwargs: Any) -> None:
        self.response = Response(status_code)
        super(HTTPError, self).__init__(*args, **kwargs)  # type: ignore
