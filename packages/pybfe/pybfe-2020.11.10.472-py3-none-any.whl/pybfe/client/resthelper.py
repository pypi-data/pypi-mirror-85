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

from __future__ import absolute_import, print_function

import json
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Union

from intentionet.bfe.proto.api_gateway_pb2 import WorkMgrV1Request, WorkMgrV1Response
from pybatfish.client.consts import CoordConsts
from pybatfish.exception import BatfishException
from pybatfish.util import BfJsonEncoder
from pybfe.client.exception import HTTPError

if TYPE_CHECKING:
    from pybfe.client.session import Session

_encoder = BfJsonEncoder()


def get_json_response(
    session: "Session",
    resource: str,
    jsonData: Optional[Dict[str, Optional[Union[str, Tuple[str, str]]]]] = None,
    file_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Send a request (POST or GET) to Batfish.

    :param session: :py:class:`~pybatfish.client.session.Session` object to use
    :param resource: the API endpoint to call on the Batfish server, string
    :param jsonData: any HTTP POST data to send, as a dictionary
    """
    response = _make_request(session, resource, jsonData, file_key)
    json_response = list(response)
    if json_response[0] != CoordConsts.SVC_KEY_SUCCESS:
        raise BatfishException(
            "Coordinator returned failure: {}".format(json_response[1])
        )
    return dict(json_response[1])


def _make_request(
    session: "Session",
    resource: str,
    json_data: Optional[Dict[str, Optional[Union[str, Tuple[str, str]]]]],
    file_key: Optional[str],
) -> Any:
    """Actually make a HTTP(s) request to Batfish coordinator.

    :raises ConnectionError if the coordinator is not available
    """
    file_data = None  # type: Optional[bytes]
    encoded_params = dict()  # type: Dict[str,str]
    if json_data is not None:
        for key, value in json_data.items():
            if value is None:
                continue
            if key == file_key:
                if isinstance(value, str):
                    file_data_str = value
                else:
                    file_data_str = value[1]
                file_data = file_data_str.encode("utf-8")
            else:
                encoded_params[key] = str(value)
    req = WorkMgrV1Request(
        credentials=session._credentials,
        params=encoded_params,
        file_data=file_data,
        file_param=file_key,
        resource=resource,
        resp_content_type="application/json",
    )
    resp = session._api_gw.WorkMgrV1(req)  # type: WorkMgrV1Response
    if resp.status == 0:
        raise ConnectionError("Batfish Enterprise service is unavailable")
    if resp.status != 200:
        error_body = resp.body.decode("utf-8") if resp.body is not None else None
        raise HTTPError(
            resp.status,
            "WorkMgrV1: status: {}, status_text: {}, resource: {}, body: {}".format(
                resp.status, resp.status_text, resource, error_body,
            ),
        )
    if resp.body is None:
        raise Exception(
            "WorkMgrV1: resource: {}, status was 200 OK but received empty response".format(
                resource
            )
        )
    return json.loads(resp.body)
