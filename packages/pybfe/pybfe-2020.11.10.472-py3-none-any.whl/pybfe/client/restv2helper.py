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
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, Optional

from intentionet.bfe.proto.api_gateway_pb2 import WorkMgrV2Request, WorkMgrV2Response
from pybatfish.client.consts import CoordConstsV2
from pybatfish.datamodel.referencelibrary import (
    NodeRoleDimension,
    NodeRolesData,
    ReferenceBook,
)
from pybatfish.util import BfJsonEncoder
from pybfe.client.exception import HTTPError

if TYPE_CHECKING:
    from pybfe.client.session import Session

_encoder = BfJsonEncoder()

__all__ = [
    "delete_network_object",
    "delete_node_role_dimension",
    "delete_reference_book",
    "delete_snapshot_object",
    "get_answer",
    "get_network_object",
    "get_node_role_dimension",
    "get_node_roles",
    "get_reference_book",
    "get_reference_library",
    "get_snapshot_input_object",
    "get_snapshot_object",
    "put_network_object",
    "put_node_role_dimension",
    "put_reference_book",
    "put_snapshot_object",
]


def delete_network_object(session: "Session", key: str) -> None:
    """Deletes extended object with given key for the current network."""
    path = "{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS, session.network, CoordConstsV2.RSC_OBJECTS
    )
    _delete(session, path, {CoordConstsV2.QP_KEY: key})


def delete_node_role_dimension(session: "Session", dimension: str) -> None:
    """Deletes the definition of the given node role dimension for the active network."""
    if not session.network:
        raise ValueError("Network must be set to delete a node role dimension")
    if not dimension:
        raise ValueError("Dimension must be a non-empty string")
    path = "{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_NODE_ROLES,
        dimension,
    )
    _delete(session, path)


def delete_reference_book(session: "Session", book_name: str) -> None:
    """Deletes the definition of the given reference book name."""
    if not session.network:
        raise ValueError("Network must be set to delete a reference book")
    if not book_name:
        raise ValueError("Book name must be a non-empty string")
    path = "{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_REFERENCE_LIBRARY,
        book_name,
    )
    _delete(session, path)


def delete_snapshot_object(
    session: "Session", key: str, snapshot: Optional[str] = None
) -> None:
    """Deletes extended object with given key for the current snapshot."""
    path = "{}/{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_SNAPSHOTS,
        session.get_snapshot(snapshot),
        CoordConstsV2.RSC_OBJECTS,
    )
    _delete(session, path, {CoordConstsV2.QP_KEY: key})


def get_answer(
    session: "Session", question: str, params: Dict[str, Optional[str]]
) -> Dict[str, Any]:
    """Get answer for the specified question."""
    path = "{}/{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_QUESTIONS,
        question,
        CoordConstsV2.RSC_ANSWER,
    )
    return _get_dict(session, path, params)


def get_network_object(session: "Session", key: str) -> str:
    """Gets extended object with given key for the current network."""
    path = "{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS, session.network, CoordConstsV2.RSC_OBJECTS,
    )
    return str(_get(session, path, {CoordConstsV2.QP_KEY: key}, decode=False))


def get_snapshot_input_object(
    session: "Session", key: str, snapshot: Optional[str] = None
) -> BytesIO:
    """Gets input object with given key for the current snapshot."""
    path = "{}/{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_SNAPSHOTS,
        session.get_snapshot(snapshot),
        CoordConstsV2.RSC_INPUT,
    )
    return _get_stream(session, path, {CoordConstsV2.QP_KEY: key})


def get_snapshot_object(
    session: "Session", key: str, snapshot: Optional[str] = None,
) -> str:
    """Gets extended object with given key for the current snapshot."""
    path = "{}/{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_SNAPSHOTS,
        session.get_snapshot(snapshot),
        CoordConstsV2.RSC_OBJECTS,
    )
    return str(_get(session, path, {CoordConstsV2.QP_KEY: key}, decode=False))


def get_node_role_dimension(session: "Session", dimension: str) -> Dict[str, Any]:
    """Gets the defintion of the given node role dimension for the active network."""
    if not session.network:
        raise ValueError("Network must be set to get node roles")
    if not dimension:
        raise ValueError("Dimension must be a non-empty string")
    path = "{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_NODE_ROLES,
        dimension,
    )
    return _get_dict(session, path)


def get_node_roles(session: "Session") -> Dict[str, Any]:
    """Gets the definitions of node roles for the active network."""
    if not session.network:
        raise ValueError("Network must be set to get node roles")
    path = "{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS, session.network, CoordConstsV2.RSC_NODE_ROLES
    )
    return _get_dict(session, path)


def get_reference_book(session: "Session", book_name: str) -> Dict[str, Any]:
    """Gets the reference book for the active network."""
    if not session.network:
        raise ValueError("Network must be set to get a reference book")
    if not book_name:
        raise ValueError("Book name must be a non-empty string")
    path = "{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_REFERENCE_LIBRARY,
        book_name,
    )
    return _get_dict(session, path)


def get_reference_library(session: "Session") -> Dict[str, Any]:
    """Gets the reference library for the active network."""
    if not session.network:
        raise ValueError("Network must be set to get the reference library")
    path = "{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS, session.network, CoordConstsV2.RSC_REFERENCE_LIBRARY
    )
    return _get_dict(session, path)


def get_snapshot_inferred_node_roles(
    session: "Session", snapshot: Optional[str] = None
) -> Dict[str, Any]:
    """Gets suggested definitions and hypothetical assignments of node roles for the active network and snapshot."""
    if not session.network:
        raise ValueError("Network must be set to get node roles")
    path = "{}/{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_SNAPSHOTS,
        session.get_snapshot(snapshot),
        CoordConstsV2.RSC_INFERRED_NODE_ROLES,
    )
    return _get_dict(session, path)


def get_snapshot_inferred_node_role_dimension(
    session: "Session", dimension: str, snapshot: Optional[str] = None
) -> Dict[str, Any]:
    """Gets the suggested definition and hypothetical assignments of node roles for the given inferred dimension for the active network and snapshot."""
    if not session.network:
        raise ValueError("Network must be set to get node roles")
    path = "{}/{}/{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_SNAPSHOTS,
        session.get_snapshot(snapshot),
        CoordConstsV2.RSC_INFERRED_NODE_ROLES,
        dimension,
    )
    return _get_dict(session, path)


def _get_work_log_path(network: str, snapshot: str, work_id: str) -> str:
    return "{}/{}/{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        network,
        CoordConstsV2.RSC_SNAPSHOTS,
        snapshot,
        CoordConstsV2.RSC_WORK_LOG,
        work_id,
    )


def get_work_log(session: "Session", snapshot: Optional[str], work_id: str) -> str:
    """Retrieve the log for a work item with a given ID."""
    if not session.network:
        raise ValueError("Network must be set to get work log")

    path = _get_work_log_path(session.network, session.get_snapshot(snapshot), work_id)
    return str(_get(session, path, dict(), False))


def get_component_versions(session: "Session") -> Dict[str, Any]:
    """Get a dictionary of backend components (e.g. Batfish, Z3) and their versions."""
    return _get_dict(session, "version")


def get_question_templates(session: "Session", verbose: bool) -> Dict:
    """Get question templates from the backend.

    :param verbose: if True, even hidden questions will be returned.
    """
    return _get_dict(
        session,
        path="{}".format(CoordConstsV2.RSC_QUESTION_TEMPLATES),
        params={CoordConstsV2.QP_VERBOSE: verbose},
    )


def put_network_object(session: "Session", key: str, data: str) -> None:
    """Put data as extended object with given key for the current network."""
    path = "{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS, session.network, CoordConstsV2.RSC_OBJECTS
    )
    _put(session, path, data, {CoordConstsV2.QP_KEY: key}, encode=False)


def put_node_role_dimension(session: "Session", dimension: NodeRoleDimension) -> None:
    """Adds a new node role dimension to the active network."""
    if not session.network:
        raise ValueError("Network must be set to add node role dimension")
    path = "{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_NODE_ROLES,
        dimension.name,
    )
    _put(session, path, dimension)


def put_node_roles(session: "Session", node_roles_data: NodeRolesData) -> None:
    """Writes the definitions of node roles for the active network. Completely replaces any existing definitions."""
    if not session.network:
        raise ValueError("Network must be set to get node roles")
    path = "{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS, session.network, CoordConstsV2.RSC_NODE_ROLES
    )
    _put(session, path, node_roles_data, content_type="application/json")


def put_reference_book(session: "Session", book: ReferenceBook) -> None:
    """Put a reference book to the active network."""
    if not session.network:
        raise ValueError("Network must be set to add reference book")
    path = "{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_REFERENCE_LIBRARY,
        book.name,
    )
    _put(session, path, book)


def put_snapshot_object(
    session: "Session", key: str, data: str, snapshot: Optional[str] = None
) -> None:
    """Put data as extended object with given key for the current snapshot."""
    path = "{}/{}/{}/{}/{}".format(
        CoordConstsV2.RSC_NETWORKS,
        session.network,
        CoordConstsV2.RSC_SNAPSHOTS,
        session.get_snapshot(snapshot),
        CoordConstsV2.RSC_OBJECTS,
    )
    _put(session, path, data, {CoordConstsV2.QP_KEY: key}, encode=False)


def _delete(
    session: "Session", path: str, params: Optional[Dict[str, Any]] = None
) -> None:
    """Make an HTTP(s) DELETE request to Batfish coordinator.

    :raises SSLError if SSL connection failed
    :raises ConnectionError if the coordinator is not available
    """
    _http_helper(
        session=session,
        path=path,
        method="DELETE",
        body=None,
        params=params,
        json_encode_body=False,
        json_decode_response=False,
        stream=False,
    )


def _get(
    session: "Session",
    path: str,
    params: Optional[Dict[str, Any]] = None,
    decode: bool = True,
    stream: bool = False,
) -> Any:
    """Make an HTTP(s) GET request to Batfish coordinator.

    :raises SSLError if SSL connection failed
    :raises ConnectionError if the coordinator is not available
    """
    return _http_helper(
        session=session,
        path=path,
        method="GET",
        body=None,
        params=params,
        json_encode_body=False,
        json_decode_response=decode,
        stream=stream,
    )


def _get_dict(
    session: "Session", path: str, params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make an HTTP(s) GET request to Batfish coordinator that should return a JSON dict.

    :raises SSLError if SSL connection failed
    :raises ConnectionError if the coordinator is not available
    """
    response = _get(session, path, params)
    return dict(response)


def _get_stream(
    session: "Session", path: str, params: Optional[Dict[str, Any]] = None
) -> BytesIO:
    """Make an HTTP(s) GET request to Batfish coordinator that should return a raw stream.

    :raises SSLError if SSL connection failed
    :raises ConnectionError if the coordinator is not available
    """
    resp = _get(session, path, params, decode=False, stream=True)
    assert isinstance(resp, BytesIO)
    return resp


def _post(
    session: "Session", path: str, obj: Any, params: Optional[Dict[str, Any]] = None
) -> None:
    """Make an HTTP(s) POST request to Batfish coordinator.

    :raises SSLError if SSL connection failed
    :raises ConnectionError if the coordinator is not available
    """
    _http_helper(
        session=session,
        path=path,
        method="POST",
        body=_encoder.default(obj),
        params=params,
        json_encode_body=True,
        json_decode_response=False,
        stream=False,
    )


def _put(
    session: "Session",
    path: str,
    body: Any,
    params: Optional[Dict[str, Any]] = None,
    encode: bool = True,
    content_type: Optional[str] = None,
) -> None:
    """Make an HTTP(s) PUT request to Batfish coordinator.

    :raises SSLError if SSL connection failed
    :raises ConnectionError if the coordinator is not available
    """
    _http_helper(
        session=session,
        path=path,
        method="PUT",
        body=_encoder.default(body),
        params=params,
        json_encode_body=encode,
        json_decode_response=False,
        stream=False,
        req_content_type=content_type,
    )


def _http_helper(
    session: "Session",
    path: str,
    method: str,
    body: Any,
    params: Optional[Dict[str, Optional[str]]],
    json_encode_body: bool,
    json_decode_response: bool,
    stream: bool,
    req_content_type: Optional[str] = None,
) -> Any:
    if stream and json_decode_response:
        raise ValueError("Only one of 'stream' and 'json_decode_response' may be True")
    body_str = body
    if json_encode_body:
        body_str = json.dumps(body_str)
    body_bytes = None
    if body_str is not None:
        body_bytes = body_str.encode("utf-8")
    encoded_params = (
        {key: str(val) for key, val in params.items() if val is not None}
        if params
        else {}
    )
    req = WorkMgrV2Request(
        credentials=session._credentials,
        body=body_bytes,
        method=method,
        params=encoded_params,
        path=path,
        req_content_type=req_content_type,
    )
    resp = session._api_gw.WorkMgrV2(req)  # type: WorkMgrV2Response
    if resp.status == 0:
        raise ConnectionError("Batfish Enterprise service is unavailable")
    if resp.status == 200 and stream:
        return BytesIO(resp.body)
    decoded_response = None  # type: Any
    if resp.body is not None:
        if resp.status == 200 and json_decode_response:
            decoded_response = json.loads(resp.body)
        else:
            decoded_response = resp.body.decode("utf-8")
    if resp.status != 200:
        raise HTTPError(
            resp.status,
            "WorkMgrV2: status: {}, status_text: {}, path: {}, body: {}".format(
                resp.status, resp.status_text, path, decoded_response,
            ),
        )
    return decoded_response
