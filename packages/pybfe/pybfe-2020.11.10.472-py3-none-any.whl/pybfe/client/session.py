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
"""Contains class definitions for Enterprise Pybatfish Sessions."""
import json
import operator
import os
import re
import time
import warnings
import zipfile
from io import BytesIO
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Text,
    Tuple,
    Union,
)
from urllib.parse import quote

import attr
from google.protobuf.json_format import MessageToDict, ParseDict

from intentionet.bfe.proto.api_gateway_pb2 import (
    CreateAdHocAssertionRequest,
    CreatePolicyRequest,
    DataRetentionPolicy,
    ForkSnapshotRequest,
    GetAdHocAssertionResultRequest,
    GetAdHocAssertionResultResponse,
    GetDataRetentionPolicyRequest,
    GetPolicyResultRequest,
)
from intentionet.bfe.proto.api_gateway_pb2 import Interface as InterfaceMessage
from intentionet.bfe.proto.api_gateway_pb2 import (
    ListPoliciesRequest,
    ListPolicyResultsMetadataRequest,
)
from intentionet.bfe.proto.api_gateway_pb2 import Node as NodeMessage
from intentionet.bfe.proto.api_gateway_pb2 import (
    SnapshotStatus,
    UpdateDataRetentionPolicyRequest,
)
from intentionet.bfe.proto.assertions.adhoc_pb2 import (
    AD_HOC_EXECUTION_STATUS_ERROR,
    AD_HOC_EXECUTION_STATUS_EXECUTED,
    AD_HOC_EXECUTION_STATUS_UNKNOWN,
    AdHocAssertion,
    AdHocAssertionId,
    AdHocAssertionResult,
)
from intentionet.bfe.proto.assertions.core_pb2 import (
    ASSERTION_STATUS_ERROR,
    ASSERTION_STATUS_PASS,
    ASSERTION_STATUS_PASS_WARN,
    AssertionInput,
)
from intentionet.bfe.proto.policies_api_pb2 import (
    Policy,
    PolicyId,
    PolicyResult,
    PolicyResultMetadata,
)
from pybatfish.client._facts import get_facts, load_facts, validate_facts
from pybatfish.client.asserts import (
    _format_df,
    _get_question_object,
    _raise_common,
    assert_filter_denies,
    assert_filter_has_no_unreachable_lines,
    assert_filter_permits,
    assert_no_duplicate_router_ids,
    assert_no_forwarding_loops,
    assert_no_incompatible_bgp_sessions,
    assert_no_undefined_references,
    assert_no_unestablished_bgp_sessions,
)
from pybatfish.client.consts import CoordConsts
from pybatfish.client.session import Asserts as BaseAsserts
from pybatfish.client.session import Session as BaseSession
from pybatfish.datamodel import (
    HeaderConstraints,
    Interface,
    NodeRoleDimension,
    NodeRolesData,
    PathConstraints,
    ReferenceBook,
    ReferenceLibrary,
)
from pybatfish.datamodel.answer import TableAnswer
from pybatfish.datamodel.answer.base import Answer
from pybatfish.datamodel.answer.table import is_table_ans
from pybatfish.exception import (
    BatfishAssertException,
    BatfishAssertWarning,
    BatfishException,
)
from pybfe.client import resthelper, restv2helper, workhelper
from pybfe.client.credentials import CallCredentialsPlugin
from pybfe.client.internal import _bf_get_question_templates
from pybfe.client.policy._policy import get_or_create_test, load_policy, write_policy
from pybfe.datamodel.aggregates import TopologyAggregates
from pybfe.datamodel.policy import (
    STATUS_ERROR,
    STATUS_FAIL,
    STATUS_PASS,
    Assert,
    CiProperties,
)
from pybfe.datamodel.policy import Policy as LegacyPolicy
from pybfe.datamodel.policy import Question, Test
from pybfe.question.question import Questions, _load_question_dict
from pybfe.util import (
    get_uuid,
    rand_int,
    read_zip,
    text_with_platform,
    zip_from_dir,
    zip_from_file_text,
)

if TYPE_CHECKING:
    from intentionet.bfe.proto.api_gateway_pb2 import (
        Credentials,
        NetworkStatus,
        NetworkMetadata as NetworkMetadataMessage,
        SnapshotMetadata as SnapshotMetadataMessage,
        SnapshotStatus,
    )
    from pybfe.datamodel.metadata import NetworkMetadata, SnapshotMetadata  # noqa

__all__ = ["Asserts", "Session"]

DEFAULT_NETWORK_PREFIX = "net_"
DEFAULT_SNAPSHOT_PREFIX = "snap_"

_PYTEST_CURRENT_TEST_VAR = "PYTEST_CURRENT_TEST"
_PYTEST_TEST_PATTERN = re.compile(r"(?P<policy_name>\w+)\.py::(?P<test_name>\w+)")

_NETWORK_OBJECT_TOPOLOGY_AGGREGATES = "topology_aggregates"
_NETWORK_OBJECT_TOPOLOGY_POSITIONS = "topology_positions"
_NETWORK_OBJECT_TOPOLOGY_ROOTS = "topology_roots"


class Asserts(BaseAsserts):
    """Contains assertions for a Session."""

    FILTER_DENIES_NAME = "Assert filter denies"
    FILTER_HAS_NO_UNREACHABLE_LINES_NAME = "Assert filter has no unreachable lines"
    FILTER_PERMITS_NAME = "Assert filter permits"
    FLOWS_FAIL_NAME = "Assert flows fail"
    FLOWS_SUCCEED_NAME = "Assert flows succeed"
    NO_FORWARDING_LOOPS_NAME = "Assert no forwarding loops"
    NO_DUPLICATE_ROUTER_IDS = "Assert no duplicate router IDs"
    NO_INCOMPATIBLE_BGP_SESSIONS_NAME = "Assert no incompatible BGP sessions"
    NO_INCOMPATIBLE_OSPF_SESSIONS_NAME = "Assert no incompatible OSPF sessions"
    NO_UNESTABLISHED_BGP_SESSIONS_NAME = "Assert no unestablished BGP sessions"
    NO_UNDEFINED_REFERENCES_NAME = "Assert no undefined references"
    VTEP_REACHABILITY_NAME = "Assert all VXLAN VTEPs are reachable from source VTEPs"

    # Name used for asserts when no name is specified or inferred
    DEFAULT_ASSERT_NAME = "No assertion name set"

    def __init__(self, session):
        self.session = session
        self.current_assertion = None  # type: Optional[Text]
        # Mapping to hold assertion<->questions association, before the assertion has been performed/created
        self.question_mapping = {}

    def assert_that(
        self,
        assertion: Union[Dict, AssertionInput],
        network: Optional[str] = None,
        snapshot: Optional[str] = None,
        soft: bool = False,
    ) -> bool:
        """
        Check if the specified assertion passes.

        :param assertion: assertion to check
        :type assertion: Union[Dict, AssertionInput]
        :param network: name of the network to run the assertion on, if not specified, the session's current network will be used
        :type network: Optional[str]
        :param snapshot: name of the snapshot to run the assertion on, if not specified, the session's current snapshot will be used
        :type snapshot: Optional[str]
        :param soft: whether this assertion is soft (i.e., generates a warning but not a failure)
        :type soft: bool
        :return: True if the assertion passes, False otherwise
        :rtype bool:
        :raises BatfishAssertException: if `soft` is not True and the assertion does not pass
        """
        network = self.session._get_network_or_raise(network)
        snapshot = self.session._get_snapshot_or_raise(snapshot)
        assert network is not None
        assert snapshot is not None
        return self._assert(
            self.run_assertion(assertion=assertion, network=network, snapshot=snapshot),
            soft=soft,
            network=network,
            snapshot=snapshot,
        )

    def _get_assertion_result(
        self, network: str, snapshot: str, id_: AdHocAssertionId
    ) -> GetAdHocAssertionResultResponse:
        """Get status and result for specified assertion."""
        req = GetAdHocAssertionResultRequest(
            credentials=self.session._credentials,
            network_name=network,
            snapshot_name=snapshot,
            id=id_,
        )
        return self.session._api_gw.GetAdHocAssertionResult(request=req)

    def _wait_for_assertion_complete(
        self, network: str, snapshot: str, id_: AdHocAssertionId
    ) -> None:
        """Wait until specified assertion is complete."""
        done = False
        while not done:
            result = self._get_assertion_result(network, snapshot, id_)
            current_status = result.status
            if current_status == AD_HOC_EXECUTION_STATUS_EXECUTED:
                return
            if current_status == AD_HOC_EXECUTION_STATUS_UNKNOWN:
                raise ValueError("Assertion not found")
            if current_status == AD_HOC_EXECUTION_STATUS_ERROR:
                raise ValueError(
                    "Assertion failed to run: {}".format(
                        result.result.result.metadata.error.message
                    )
                )
            # TODO smarter sleeping
            time.sleep(1)  # seconds
        return

    def _assert(
        self,
        adhoc_result: AdHocAssertionResult,
        network: str,
        snapshot: str,
        soft: bool = False,
    ) -> bool:
        """
        Assert the specified AdHocAssertionResult passed.

        :raises BatfishAssertException: if `soft` is not True and the assertion does not pass
        """
        # Extract actual assertion result from adhoc result container
        status = adhoc_result.result.metadata.status
        if status == ASSERTION_STATUS_ERROR:
            raise ValueError(
                "Error running assertion: {}".format(
                    adhoc_result.result.metadata.error.message
                )
            )
        passed = (
            status == ASSERTION_STATUS_PASS or status == ASSERTION_STATUS_PASS_WARN
        )  # type: bool

        if not soft and not passed:
            link = self.session._get_adhoc_assertion_dashboard_url(
                adhoc_result=adhoc_result, network=network, snapshot=snapshot
            )
            raise BatfishAssertException(
                "Assertion failed. Explore the failure with the dashboard: {link}".format(
                    link=link
                )
            )
        return passed

    @staticmethod
    def _to_assertion_input(assertion: Union[Dict, AssertionInput]) -> AssertionInput:
        """Validate assertion and convert assertion dict to assertion input if applicable."""
        if isinstance(assertion, Dict):
            assertion_input = ParseDict(assertion, AssertionInput())
        elif isinstance(assertion, AssertionInput):
            assertion_input = assertion
        else:
            raise ValueError("Unknown assertion type ({}).".format(type(assertion)))
        return assertion_input

    def run_assertion(
        self,
        assertion: Union[Dict, AssertionInput],
        network: Optional[str] = None,
        snapshot: Optional[str] = None,
    ) -> AdHocAssertionResult:
        """
        Run the specified assertion.

        :param assertion: assertion to run
        :type assertion: Union[Dict, AssertionInput]
        :param network: name of the network to run the assertion on, if not specified, the session's current network will be used
        :type network: Optional[str]
        :param snapshot: name of the snapshot to run the assertion on, if not specified, the session's current snapshot will be used
        :type snapshot: Optional[str]
        :return: raw result of the specified adhoc assertion
        :rtype AdHocAssertionResult:
        """
        # Validate input
        network = self.session._get_network_or_raise(network)
        snapshot = self.session._get_snapshot_or_raise(snapshot)
        assert network is not None
        assert snapshot is not None

        # Validate starting state and input
        assertion_input = self._to_assertion_input(assertion)

        # Create & run the assertion
        req = CreateAdHocAssertionRequest(
            credentials=self.session._credentials,
            network_name=network,
            snapshot_name=snapshot,
            assertion=AdHocAssertion(
                # Omit id, so one is provided by backend
                input=assertion_input,
            ),
        )
        res = self.session._api_gw.CreateAdHocAssertion(request=req)
        id_ = res.id

        # Wait for completion
        self._wait_for_assertion_complete(network, snapshot, id_)

        # Return result
        return self._get_assertion_result(network, snapshot, id_).result

    def assert_filter_denies(
        self,
        filters,
        headers,
        startLocation=None,
        soft=False,
        snapshot=None,
        df_format="table",
    ):
        # type: (str, HeaderConstraints, Optional[str], bool, Optional[str], str) -> bool
        """
        Check if a filter (e.g., ACL) denies a specified set of flows.

        :param filters: the specification for the filter (filterSpec) to check
        :param headers: :py:class:`~pybatfish.datamodel.flow.HeaderConstraints`
        :param startLocation: LocationSpec indicating where a flow starts
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param snapshot: the snapshot on which to check the assertion
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        :return: True if the assertion passes
        """
        self._set_assert_name(self.FILTER_DENIES_NAME)
        try:
            val = assert_filter_denies(
                filters, headers, startLocation, soft, snapshot, self.session, df_format
            )
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_filter_has_no_unreachable_lines(
        self, filters, soft=False, snapshot=None, df_format="table"
    ):
        # type: (str, bool, Optional[str], str) -> bool
        """
        Check that a filter (e.g. an ACL) has no unreachable lines.

        A filter line is considered unreachable if it will never match a packet,
        e.g., because its match condition is empty or covered completely by those of
        prior lines."

        :param filters: the specification for the filter (filterSpec) to check
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param snapshot: the snapshot on which to check the assertion
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        :return: True if the assertion passes
        """
        self._set_assert_name(self.FILTER_HAS_NO_UNREACHABLE_LINES_NAME)
        try:
            val = assert_filter_has_no_unreachable_lines(
                filters, soft, snapshot, self.session, df_format
            )
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_filter_permits(
        self,
        filters,
        headers,
        startLocation=None,
        soft=False,
        snapshot=None,
        df_format="table",
    ):
        # type: (str, HeaderConstraints, Optional[str], bool, Optional[str], str) -> bool
        """
        Check if a filter (e.g., ACL) permits a specified set of flows.

        :param filters: the specification for the filter (filterSpec) to check
        :param headers: :py:class:`~pybatfish.datamodel.flow.HeaderConstraints`
        :param startLocation: LocationSpec indicating where a flow starts
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param snapshot: the snapshot on which to check the assertion
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        :return: True if the assertion passes
        """
        self._set_assert_name(self.FILTER_PERMITS_NAME)
        try:
            val = assert_filter_permits(
                filters, headers, startLocation, soft, snapshot, self.session, df_format
            )
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_flows_fail(
        self, startLocation, headers, soft=False, snapshot=None, df_format="table"
    ):
        # type: (str, HeaderConstraints, bool, Optional[str], str) -> bool
        """
        Check if the specified set of flows, denoted by starting locations and headers, fail.

        :param startLocation: LocationSpec indicating where the flow starts
        :param headers: :py:class:`~pybatfish.datamodel.flow.HeaderConstraints`
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param snapshot: the snapshot on which to check the assertion
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        :return: True if the assertion passes
        """
        self._set_assert_name(self.FLOWS_FAIL_NAME)
        try:
            val = self._assert_flows_fail(startLocation, headers, soft, snapshot)
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def _raise_common_with_link(
        self, message: str, question: Question, soft: bool = False
    ) -> bool:
        """Util function for soft/hard exception raising which includes a link to the Dashboard in surfaced message."""
        __tracebackhide__ = operator.methodcaller(
            "errisinstance", BatfishAssertException
        )
        err_text = "Explore failure details with the Dashboard: {}\n{}".format(
            self.session._get_answer_dashboard_url(question.get_name()), message
        )
        if soft:
            warnings.warn(err_text, category=BatfishAssertWarning)
            return False
        else:
            raise BatfishAssertException(err_text)

    def _assert_flows_fail(self, startLocation, headers, soft=False, snapshot=None):
        # type: (str, HeaderConstraints, bool, Optional[str]) -> bool
        __tracebackhide__ = operator.methodcaller(
            "errisinstance", BatfishAssertException
        )

        kwargs = dict(
            pathConstraints=PathConstraints(startLocation=startLocation),
            headers=headers,
            actions="success",
        )

        q = _get_question_object(self.session, "reachability").reachability(**kwargs)
        df = q.answer(snapshot).frame()
        if len(df) > 0:
            message = "Found a flow that succeed, when expected to fail"
            flow = df.iloc[0]["Flow"]
            traces = df.iloc[0]["Traces"]
            trace = traces[0]
            extra = ""
            if len(traces) > 1:
                extra = "\nand {} more trace(s) not shown".format(len(traces) - 1)

            # TODO: fix pybf types
            return bool(
                self._raise_common_with_link(
                    "{}\nFlow:\n{}\n\nTrace #1:\n{}{}".format(
                        message, flow, trace, extra
                    ),
                    q,
                    soft,
                )
            )
        return True

    def assert_flows_succeed(
        self, startLocation, headers, soft=False, snapshot=None, df_format="table"
    ):
        # type: (str, HeaderConstraints, bool, Optional[str], str) -> bool
        """
        Check if the specified set of flows, denoted by starting locations and headers, succeed.

        :param startLocation: LocationSpec indicating where the flow starts
        :param headers: :py:class:`~pybatfish.datamodel.flow.HeaderConstraints`
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param snapshot: the snapshot on which to check the assertion
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        :return: True if the assertion passes
        """
        self._set_assert_name(self.FLOWS_SUCCEED_NAME)
        try:
            val = self._assert_flows_succeed(startLocation, headers, soft, snapshot)
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def _assert_flows_succeed(self, startLocation, headers, soft=False, snapshot=None):
        # type: (str, HeaderConstraints, bool, Optional[str]) -> bool
        __tracebackhide__ = operator.methodcaller(
            "errisinstance", BatfishAssertException
        )

        kwargs = dict(
            pathConstraints=PathConstraints(startLocation=startLocation),
            headers=headers,
            actions="failure",
        )

        q = _get_question_object(self.session, "reachability").reachability(**kwargs)
        df = q.answer(snapshot).frame()
        if len(df) > 0:
            message = "Found a flow that failed, when expected to succeed"
            flow = df.iloc[0]["Flow"]
            traces = df.iloc[0]["Traces"]
            trace = traces[0]
            extra = ""
            if len(traces) > 1:
                extra = "\nand {} more trace(s) not shown".format(len(traces) - 1)

            # TODO: fix pybf types
            return bool(
                self._raise_common_with_link(
                    "{}\nFlow:\n{}\n\nTrace #1:\n{}{}".format(
                        message, flow, trace, extra
                    ),
                    q,
                    soft,
                )
            )
        return True

    def assert_no_duplicate_router_ids(
        self, snapshot=None, nodes=None, protocols=None, soft=False, df_format="table"
    ):
        # type: (Optional[str], Optional[str], Optional[List[str]], bool, str) -> bool
        """Assert that there are no duplicate router IDs present in the snapshot.

        :param snapshot: the snapshot on which to check the assertion
        :param nodes: the nodes on which to run the assertion
        :param protocols: the protocol on which to use the assertion, e.g. bgp, ospf, etc.
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        """
        self._set_assert_name(self.NO_DUPLICATE_ROUTER_IDS)
        try:
            val = assert_no_duplicate_router_ids(
                snapshot, nodes, protocols, soft, self.session, df_format
            )

            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_no_forwarding_loops(self, snapshot=None, soft=False, df_format="table"):
        # type: (Optional[str], bool, str) -> bool
        """Assert that there are no forwarding loops in the snapshot.

        :param snapshot: the snapshot on which to check the assertion
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        """
        self._set_assert_name(self.NO_FORWARDING_LOOPS_NAME)
        try:
            val = assert_no_forwarding_loops(snapshot, soft, self.session, df_format)
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_no_incompatible_bgp_sessions(
        self,
        nodes=None,
        remote_nodes=None,
        status=None,
        snapshot=None,
        soft=False,
        df_format="table",
    ):
        # type: (Optional[str], Optional[str], Optional[str], Optional[str], bool, str) -> bool
        """Assert that there are no incompatible BGP sessions present in the snapshot.

        :param nodes: search sessions with specified nodes on one side of the sessions.
        :param remote_nodes: search sessions with specified remote_nodes on other side of the sessions.
        :param status: select sessions matching the specified `BGP session status specifier <https://github.com/batfish/batfish/blob/master/questions/Parameters.md#bgp-session-compat-status-specifier>`_, if none is specified then all statuses other than `UNIQUE_MATCH`, `DYNAMIC_MATCH`, and `UNKNOWN_REMOTE` are selected.
        :param snapshot: the snapshot on which to check the assertion
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        """
        self._set_assert_name(self.NO_INCOMPATIBLE_BGP_SESSIONS_NAME)
        try:
            val = assert_no_incompatible_bgp_sessions(
                nodes, remote_nodes, status, snapshot, soft, self.session, df_format
            )
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_no_incompatible_ospf_sessions(
        self,
        nodes=None,
        remote_nodes=None,
        snapshot=None,
        soft=False,
        df_format="table",
    ):
        # type: (Optional[str], Optional[str], Optional[str], bool, str) -> bool
        """Assert that there are no incompatible or unestablished OSPF sessions present in the snapshot.

        :param nodes: search sessions with specified nodes on one side of the sessions.
        :param remote_nodes: search sessions with specified remote_nodes on other side of the sessions.
        :param snapshot: the snapshot on which to check the assertion
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        """
        self._set_assert_name(self.NO_INCOMPATIBLE_OSPF_SESSIONS_NAME)
        try:

            from pybatfish.client.asserts import assert_no_incompatible_ospf_sessions

            val = assert_no_incompatible_ospf_sessions(
                nodes, remote_nodes, snapshot, soft, self.session, df_format
            )
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_no_unestablished_bgp_sessions(
        self,
        nodes=None,
        remote_nodes=None,
        snapshot=None,
        soft=False,
        df_format="table",
    ):
        # type: (Optional[str], Optional[str], Optional[str], bool, str) -> bool
        """Assert that there are no BGP sessions that are compatible but not established.

        :param nodes: search sessions with specified nodes on one side of the sessions.
        :param remote_nodes: search sessions with specified remote_nodes on other side of the sessions.
        :param snapshot: the snapshot on which to check the assertion
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        """
        self._set_assert_name(self.NO_UNESTABLISHED_BGP_SESSIONS_NAME)
        try:
            val = assert_no_unestablished_bgp_sessions(
                nodes, remote_nodes, snapshot, soft, self.session, df_format
            )
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_no_undefined_references(
        self, snapshot=None, soft=False, df_format="table"
    ):
        # type: (Optional[str], bool, str) -> bool
        """Assert that there are no undefined references present in the snapshot.

        :param snapshot: the snapshot on which to check the assertion
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        """
        self._set_assert_name(self.NO_UNDEFINED_REFERENCES_NAME)
        try:
            val = assert_no_undefined_references(
                snapshot, soft, self.session, df_format
            )
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def assert_vtep_reachability(self, snapshot=None, soft=False, df_format="table"):
        # type: (Optional[str], bool, str) -> bool
        """Assert that all VXLAN VTEPs are reachable from source VTEPs.

        :param snapshot: the snapshot on which to check the assertion
        :param soft: whether this assertion is soft (i.e., generates a warning but
            not a failure)
        :param df_format: How to format the Dataframe content in the output message.
            Valid options are 'table' and 'records' (each row is a key-value pairs).
        """
        self._set_assert_name(self.VTEP_REACHABILITY_NAME)
        try:
            val = self._assert_vtep_reachability_helper(snapshot, soft, df_format)
            return self._common_return(val, snapshot)
        except Exception as e:
            self._record_error(e, snapshot)
            raise e

    def _assert_vtep_reachability_helper(self, snapshot, soft, df_format):
        # type: (Optional[str], bool, str) -> bool
        __tracebackhide__ = operator.methodcaller(
            "errisinstance", BatfishAssertException
        )

        df = (
            _get_question_object(self.session, "vxlanReachabilityAnalyzer")
            .vxlanReachabilityAnalyzer()
            .answer(snapshot)
            .frame()
        )
        if len(df) > 0:
            # TODO: fix pybf types
            return bool(
                _raise_common(
                    "Found unreachable VTEPs, when none were expected\n{}".format(
                        _format_df(df, df_format)
                    ),
                    soft,
                )
            )
        return True

    def _set_assert_name(self, name):
        """Set current assert name."""
        self.current_assertion = name

    def _common_return(self, result: bool, snapshot: Optional[str]) -> bool:
        # Assert-result is True when the assert passes and False when it fails
        if result:
            return self._record_result(
                result=result,
                status=STATUS_PASS,
                message="Assertion passed!",
                snapshot=snapshot,
            )
        return self._record_result(result=result, status=STATUS_FAIL, snapshot=snapshot)

    def _record_result(
        self,
        result: bool,
        status: str,
        message: Optional[Any] = None,
        snapshot: Optional[str] = None,
    ) -> bool:
        """Record results for an assertion."""
        p_name = self.session._get_policy_name()
        p_id = self.session._get_policy_id()
        p_ci_props = self.session._get_policy_ci_props()
        t_name = self.session._get_test_name()
        a_name = self.session._get_assert_name()
        if p_name is not None and p_id is not None and t_name is not None:
            self.session._add_assertion(
                policy_name=p_name,
                policy_id=p_id,
                policy_ci_props=p_ci_props,
                test_name=t_name,
                assert_name=self.DEFAULT_ASSERT_NAME if a_name is None else a_name,
                status=status,
                message=message if message else result,
                snapshot=snapshot,
            )
        # Clear current assertion name, since the assertion is now finished
        self.current_assertion = None
        return result

    def _record_error(self, e, snapshot):
        """Record results for an assertion which encountered an exception."""
        if isinstance(e, BatfishAssertException):
            return self._record_result(
                result=str(e), status=STATUS_FAIL, snapshot=snapshot
            )
        return self._record_result(
            result=str(e), status=STATUS_ERROR, snapshot=snapshot
        )


def _to_node_messages(nodes: Optional[List[str]]) -> Optional[List[NodeMessage]]:
    """Convert list of node names into list of NodeMessage objects for grpc calls."""
    if nodes is None:
        return None
    return [NodeMessage(name=n) for n in nodes]


def _to_interface_messages(
    ifaces: Optional[List[Interface]],
) -> Optional[List[InterfaceMessage]]:
    """Convert list of Interfaces into list of InterfaceMessage objects for grpc calls."""
    if ifaces is None:
        return None
    return [
        InterfaceMessage(node_name=i.hostname, interface_name=i.interface)
        for i in ifaces
    ]


class Session(BaseSession):
    """Session for connecting to a Batfish Enterprise service."""

    _BFE_SSL_CERT_ENV_VAR = "BFE_SSL_CERT"

    # Value of nonce value indicating no nonce was specified
    _UNSPECIFIED_NONCE = 0

    def __init__(
        self,
        *,
        host: str,
        port: int = 443,
        ssl: bool = True,
        api_key: str = CoordConsts.DEFAULT_API_KEY,
        load_questions: bool = True,
        access_token: Optional[str] = None,
        **kwargs: Dict[str, Any]
    ) -> None:
        if not host:
            raise ValueError("Missing value for 'host' parameter")

        self.host = host  # type: str
        self.port = port  # type: int
        self.ssl = ssl  # type: bool

        if "port_v1" in kwargs or "port_v2" in kwargs:
            warnings.warn(
                "port_v1 and port_v2 parameters are deprecated and ignored. Use 'port=' instead"
            )

        self.policies = {}  # type: Dict[Text, Dict[Text, LegacyPolicy]]

        # Session args
        self.access_token = access_token  # type: Optional[str]
        self.api_key = api_key  # type: str
        self.network = None  # type: Optional[str]
        self.snapshot = None  # type: Optional[str]

        # Objects to hold and manage questions and asserts
        self.q = Questions(self)  # type: Questions
        self.asserts = Asserts(self)  # type: Asserts

        # attempt to log all asked questions into a policy/test
        self.record_questions = True  # type: bool

        # Additional worker args
        self.additional_args = {}  # type: Dict[str, Any]

        self.elapsed_delay = 5  # type: int
        self.stale_timeout = 5  # type: int

        # Setup connection to API Gateway as well as its health check
        from intentionet.bfe.proto.api_gateway_pb2_grpc import ApiGatewayStub
        from intentionet.bfe.proto.health.health_pb2_grpc import HealthStub
        import grpc

        options = [
            # TODO: configurable max send/recv length
            ("grpc.max_send_message_length", 2147483647),
            ("grpc.max_receive_message_length", 2147483647),
        ]
        url = "{}:{}".format(self.host, self._get_api_gw_port())
        if self.ssl:
            channel_creds = grpc.ssl_channel_credentials(
                root_certificates=self._get_custom_certs()
            )
            call_creds = grpc.metadata_call_credentials(CallCredentialsPlugin(self))
            channel = grpc.secure_channel(
                url,
                grpc.composite_channel_credentials(channel_creds, call_creds),
                options=options,
            )
        else:
            channel = grpc.insecure_channel(url, options=options,)
        self._api_gw = ApiGatewayStub(channel)
        self._api_gw_health = HealthStub(channel)

        try:
            healthy = self._is_api_healthy()
        except Exception:
            # Assume health check exception means no gRPC end point is available
            raise Exception(
                "Can only establish a session with a Batfish Enterprise backend"
            )
        if not healthy:
            raise Exception("Batfish Enterprise is not healthy")
        if load_questions:
            self.q.load()

    def _get_dashboard_url(self, network: str, snapshot: str, resource: str) -> str:
        """Generate the encoded Dashboard url for the specified network, snapshot, and snapshot-resource."""
        protocol = "https" if self.ssl else "http"
        url = quote(
            "/dashboard/{net}/{snap}/{resource}".format(
                net=network, snap=snapshot, resource=resource,
            )
        )
        return "{protocol}://{host}:{post}{url}".format(
            protocol=protocol, host=self.host, post=self.port, url=url,
        )

    def _get_answer_dashboard_url(self, name: str) -> str:
        """Generate the encoded Dashboard url for the specified question name."""
        # network and snapshot should be set by the time we get to this point
        assert self.network is not None
        assert self.snapshot is not None
        resource = "explore/view-result/{name}".format(name=name)
        return self._get_dashboard_url(self.network, self.snapshot, resource=resource)

    def _get_adhoc_assertion_dashboard_url(
        self, adhoc_result: AdHocAssertionResult, network: str, snapshot: str
    ) -> str:
        """Generate the encoded Dashboard url for the specified adhoc assertion id."""
        uid = adhoc_result.id.uid
        resource = "assertions/adhoc/{uid}".format(uid=uid)
        return self._get_dashboard_url(network, snapshot, resource=resource)

    def _is_api_healthy(self, service: Optional[str] = None) -> bool:
        """
        Check if specified gRPC service is healthy.

        If no service is specified, the overall gateway health is checked.
        """
        from intentionet.bfe.proto.health.health_pb2 import (
            HealthCheckRequest,
            HealthCheckResponse,
        )

        healthy = HealthCheckResponse.SERVING_STATUS_SERVING
        resp = self._api_gw_health.Check(HealthCheckRequest(service=service))
        return bool(
            resp.status == healthy
        )  # mypy: __eq__ is not guaranteed to return a bool

    def _get_api_gw_port(self):
        """Return port number for API gateway."""
        return os.environ.get("pybfe_api_gateway_port", self.port)

    @property
    def _credentials(self) -> "Credentials":
        """Credentials for Batfish Enterprise connection."""
        from intentionet.bfe.proto.api_gateway_pb2 import Credentials

        return Credentials(api_key=self.api_key)

    def _get_nonce(self) -> int:
        """Generate 32-bit nonce value."""
        nonce = self._UNSPECIFIED_NONCE
        # Make sure generated nonce doesn't happen to overlap w/ unspecified
        while nonce == self._UNSPECIFIED_NONCE:
            nonce = rand_int()
        return nonce

    @classmethod
    def _get_custom_certs(cls) -> Optional[bytes]:
        """Returns the user-specified custom certificates if set."""

        # Environment variable
        try:
            cert_path = os.getenv(cls._BFE_SSL_CERT_ENV_VAR)
            if cert_path:
                with open(cert_path, "rb") as f:
                    return f.read()
        except (IOError, OSError):
            pass

        # Certifi
        try:
            import certifi

            with open(certifi.where(), "rb") as f:
                return f.read()
        except (IOError, ImportError, OSError):
            pass

        return None

    def _get_network_or_raise(self, network: Optional[str]) -> str:
        """
        Return network if given or set in session. Otherwise raise ValueError
        """
        net = network if network else self.network
        if not net:
            raise ValueError("Network is required")
        assert isinstance(net, str)
        return net

    def _get_snapshot_or_raise(self, snapshot: Optional[str]) -> str:
        """
        Return snapshot if given or set in session. Otherwise raise ValueError
        """
        snap = snapshot if snapshot else self.snapshot
        if not snap:
            raise ValueError("Snapshot is required")
        assert isinstance(snap, str)
        return snap

    @staticmethod
    def _get_pytest_env_match():
        """Attempt to extract policy/test name from pytest env var."""
        if Session._get_policy_id() is not None:
            var = os.environ.get(_PYTEST_CURRENT_TEST_VAR)
            if var is not None:
                return re.search(_PYTEST_TEST_PATTERN, var)
        return None

    @staticmethod
    def _get_policy_name() -> Optional[str]:
        """Get current policy name."""
        var = os.environ.get("bf_policy_name")
        if var is not None:
            return var
        match = Session._get_pytest_env_match()
        if match:
            # force type
            name = match.group("policy_name")  # type: str
            return name
        return None

    @staticmethod
    def _get_policy_id() -> Optional[Text]:
        """Get current policy id."""
        return os.environ.get("bf_policy_id")

    @staticmethod
    def _get_policy_ci_props():
        # type: () -> CiProperties
        """Get the CI properties."""
        return CiProperties(url=os.environ.get("bf_policy_ci_url"))

    @staticmethod
    def _get_test_name() -> Optional[Text]:
        """Get current test name."""
        var = os.environ.get("bf_test_name")
        if var is not None:
            return var
        match = Session._get_pytest_env_match()
        if match:
            # force type
            name = match.group("test_name")  # type: str
            return name
        return None

    def _get_assert_name(self):
        # type: () -> Optional[Text]
        """
        Get current assert name.

        Name in environment var takes precedence over internal name.
        """
        env_name = os.environ.get("bf_assert_name")
        if env_name:
            return env_name
        return self.asserts.current_assertion

    def _get_question_map_key(self, snapshot=None):
        # type: (Optional[Text]) -> Tuple
        """
        Return the current question mapping key.

        The key returned is a tuple of snapshot, policy name, policy id, test name, and assertion name, based on current policy metadata and snapshot.
        """
        snap = snapshot if snapshot is not None else self.snapshot
        return (
            snap,
            self._get_policy_name(),
            self._get_policy_id(),
            self._get_test_name(),
            self._get_assert_name(),
        )

    def _get_bfe_version(self) -> Optional[str]:
        """Get the BfE backend version."""
        v = restv2helper.get_component_versions(self).get("Batfish-Extension-Pack")
        if v is not None:
            return str(v)
        return None

    def _check_policy_exists_locally(self, policy_name, policy_id, snapshot):
        # type: (Text, Text, Text) -> bool
        """Check if the specified policy exists locally."""
        if snapshot in self.policies:
            if policy_name in self.policies[snapshot]:
                p = self.policies[snapshot][policy_name]
                if p.id == policy_id:
                    return True
        return False

    def _check_policy_exists_remotely(self, policy_name, policy_id, snapshot):
        # type: (Text, Text, Text) -> bool
        """
        Check if the specified policy exists on the remote service.

        If the policy exists remotely, it is loaded and saved locally.
        """
        remote_policy = load_policy(self, policy_name, policy_id, snapshot)
        if remote_policy is not None:
            if snapshot not in self.policies:
                self.policies[snapshot] = {}
            self.policies[snapshot][policy_name] = remote_policy
            return True
        return False

    def _check_policy_exists(self, policy_name, policy_id, snapshot):
        # type: (Text, Text, Text) -> bool
        """Check if the specified policy exists."""
        return self._check_policy_exists_locally(
            policy_name, policy_id, snapshot
        ) or self._check_policy_exists_remotely(policy_name, policy_id, snapshot)

    def _get_policy_by_name(self, policy_name, policy_id, snapshot=None):
        # type: (Text, Text, Optional[Text]) -> LegacyPolicy
        """Get policy object from the specified policy name and ID."""
        snap = self.get_snapshot(snapshot)
        # Check locally first
        if self._check_policy_exists_locally(policy_name, policy_id, snap):
            return self.policies[snap][policy_name]

        # Check backend
        if self._check_policy_exists_remotely(policy_name, policy_id, snap):
            policy = load_policy(self, policy_name, policy_id, snap)
            if policy is not None:
                self.policies.get(snap, {})[policy_name] = policy
                return policy

        raise ValueError(
            "Specified policy does not exist (name:{}, id:{}, snapshot:{}).".format(
                policy_name, policy_id, snap
            )
        )

    def _create_policy(self, policy_name, policy_id, policy_ci_props, snapshot):
        # type: (Text, Text, CiProperties, Text) -> LegacyPolicy
        """Create a new policy with the specified name and ID.

        This policy is created locally and not written to the remote service.
        """
        p = LegacyPolicy(policy_name, policy_id, policy_ci_props)
        if snapshot not in self.policies:
            self.policies[snapshot] = {}
        self.policies[snapshot][policy_name] = p
        return p

    def _get_or_create_policy_and_test(
        self, policy_name, policy_id, policy_ci_props, test_name, snap
    ):
        # type: (Text, Text, CiProperties, Text, Text) -> Tuple[LegacyPolicy, Test]
        """
        Get the specified policy and test from the provided names.

        Creates the policy and test if they don't exist already.
        """
        if self._check_policy_exists(policy_name, policy_id, snap):
            p = self._get_policy_by_name(policy_name, policy_id, snap)
        else:
            p = self._create_policy(policy_name, policy_id, policy_ci_props, snap)
        t = get_or_create_test(p, test_name)
        return p, t

    def _add_assertion(
        self,
        policy_name,
        policy_id,
        policy_ci_props,
        test_name,
        assert_name,
        status,
        message,
        expected=None,
        actual=None,
        key_present=None,
        write=True,
        snapshot=None,
    ):
        # type: (Text, Text, CiProperties, Text, Text, Text, Text, Optional[Any], Optional[Any], Optional[bool], bool, Optional[Text]) -> None
        """Add a new assertion to the specified test in the specified policy.

        Creates the policy and test if they don't exist already.  The assertion is only written to the remote service if `write=True`
        """
        snap = self.get_snapshot(snapshot)
        p, t = self._get_or_create_policy_and_test(
            policy_name, policy_id, policy_ci_props, test_name, snap
        )
        questions = self.asserts.question_mapping.pop(
            self._get_question_map_key(snapshot), None
        )
        t.add_assert(
            Assert(
                name=assert_name,
                status=status,
                message=message,
                expected=expected,
                actual=actual,
                key_present=key_present,
                questions=questions,
            )
        )
        if write is True:
            # Update the service
            write_policy(p, session=self, snapshot=snap)

    def validate_facts(self, expected_facts, snapshot=None):
        # type: (Text, Optional[Text]) -> Dict[Text, Any]
        """
        Return a dictionary of mismatched facts between the loaded expected facts and the actual facts.

        :param expected_facts: path to directory to read expected fact YAML files from
        :type expected_facts: Text
        :param snapshot: name of the snapshot to validate facts for, defaults to the current snapshot
        :type snapshot: Text
        :return: mismatched facts between expected and actual facts
        :rtype: dict
        """
        kwargs = dict()  # type: Dict[Text, Text]
        if snapshot is not None:
            kwargs.update(snapshot=snapshot)
        # Don't bother recording property questions into policy
        # during fact validation
        self.record_questions = False
        try:
            actual_facts = get_facts(self, **kwargs)
        finally:
            self.record_questions = True

        expected_facts_ = load_facts(expected_facts)
        return self._validate_facts(expected_facts_, actual_facts)

    def _validate_facts(self, expected_facts, actual_facts):
        # type: (Dict[Text, Any], Dict[Text, Any]) -> Dict[Text, Any]
        """
        Return a dictionary of mismatched facts between the provided expected and actual facts.

        :param expected_facts: expected fact dictionary
        :type expected_facts: dict
        :param actual_facts: actual fact dictionary
        :type actual_facts: dict
        :return: mismatched facts between provided fact dictionaries
        :rtype: dict
        """
        policy_name = self._get_policy_name()
        policy_id_org = self._get_policy_id()
        policy_ci_props = self._get_policy_ci_props()
        policy_id = get_uuid() if policy_id_org is None else policy_id_org

        all_fact_val_results = validate_facts(
            expected_facts, actual_facts, verbose=True
        )
        failing_fact_results = {}  # type: Dict[Text, Any]

        # Update a separate test per node
        for node in all_fact_val_results:
            test_name = self._get_fact_test_name(node)
            vals = all_fact_val_results[node]
            for val in vals:
                # Update a separate assert per property checked
                res = vals[val]
                expected = res.get("expected")
                actual = res.get("actual")
                status = (
                    STATUS_FAIL
                    if res.get("key_present") is False or expected != actual
                    else STATUS_PASS
                )
                match_msg = "matched" if status == STATUS_PASS else "did not match"
                msg = "Actual {key} ({act}) {match_msg} expected {key} ({exp})".format(
                    key=val, match_msg=match_msg, exp=expected, act=actual
                )
                if policy_name is not None:
                    self._add_assertion(
                        policy_name,
                        policy_id,
                        policy_ci_props,
                        test_name,
                        val,
                        status,
                        msg,
                        expected,
                        actual,
                        res.get("key_present"),
                        write=False,
                    )

                # Keep track of which facts are failing so those can be returned to user
                if status == STATUS_FAIL:
                    if node not in failing_fact_results:
                        failing_fact_results[node] = {}
                    failing_fact_results[node][val] = vals[val]
        if policy_name is not None:
            # Update the backend only after we've finished processing all asserts
            write_policy(self._get_policy_by_name(policy_name, policy_id), session=self)

        # Only return mismatched facts
        return failing_fact_results

    def _get_fact_test_name(self, node):
        # type: (Text) -> Text
        """Get fact validation test name for a given node name."""
        return "Validate facts for node {}".format(node)

    def generate_dataplane(
        self,
        snapshot: Optional[str] = None,
        extra_args: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generates the data plane for the supplied snapshot. If no snapshot is specified, uses the last snapshot initialized.

        :param snapshot: name of the snapshot to generate dataplane for
        :type snapshot: str
        :param extra_args: extra arguments to be passed to Batfish
        :type extra_args: dict
        """
        snapshot = self.get_snapshot(snapshot)
        work_item = workhelper.get_workitem_generate_dataplane(self, snapshot)
        answer_dict = workhelper.execute(work_item, self, extra_args=extra_args)
        return str(answer_dict["status"].value)

    def get_answer(
        self, question: str, snapshot: str, reference_snapshot: Optional[str] = None
    ) -> Answer:
        """
        Get the answer for a previously asked question.

        :param question: the unique identifier of the previously asked question
        :type question: str
        :param snapshot: name of the snapshot the question was run on
        :type snapshot: str
        :param reference_snapshot: if present, gets the answer for a differential question asked against the specified reference snapshot
        :type reference_snapshot: str
        :return: answer to the specified question
        :rtype: :py:class:`Answer`
        """
        ans = self._get_answer(
            question, snapshot, reference_snapshot=reference_snapshot
        )
        p_name = self._get_policy_name()
        p_id = self._get_policy_id()
        p_ci_props = self._get_policy_ci_props()
        t_name = self._get_test_name()
        a_name = self._get_assert_name()
        if (
            p_name is not None
            and p_id is not None
            and t_name is not None
            and self.record_questions
        ):
            # We're in a test, so we should associate this question with a test or assertion

            q = Question(question)
            if a_name is not None:
                # Attach the question to current assertion, if one exists
                # Note: at this point, the assertion has not been created,
                # so we cannot directly add the question to it
                q_map_key = self._get_question_map_key(snapshot)
                qs = self.asserts.question_mapping.get(q_map_key, [])
                qs.append(q)
                self.asserts.question_mapping[q_map_key] = qs
                # Assume the assertion will handle writing the updated policy once it completes
            else:
                # Otherwise, just attach the question to the test
                p, t = self._get_or_create_policy_and_test(
                    p_name, p_id, p_ci_props, t_name, snapshot
                )
                t.add_question(q)
                write_policy(p, session=self, snapshot=snapshot)
        return ans

    def delete_network_object(self, key: str) -> None:
        """
        Delete the network object with specified key.

        :param key: key identifying the resource to delete
        :type key: str
        """
        restv2helper.delete_network_object(self, key)

    def get_network_object_stream(self, key: str) -> Any:
        raise NotImplementedError("Not implemented for pybfe")

    def get_network_object_text(self, key: str) -> str:
        """
        Return the text content of the network object with specified key.

        :param key: key identifying the resource to get
        :type key: str
        :return specified resource's text
        :rtype: str
        """
        return restv2helper.get_network_object(self, key)

    def delete_snapshot_object(self, key: str, snapshot: Optional[str] = None) -> None:
        """
        Delete the snapshot object with specified key.

        :param key: key identifying the resource to delete
        :type key: str
        :param snapshot: name of the snapshot under which the resource is stored
        :type snapshot: str
        """
        restv2helper.delete_snapshot_object(self, key, snapshot)

    def get_snapshot_object_stream(
        self, key: str, snapshot: Optional[str] = None
    ) -> Any:
        raise NotImplementedError("Not implemented for pybfe")

    def get_snapshot_object_text(self, key: str, snapshot: Optional[str] = None) -> str:
        """Return the text content of the snapshot object with specified key.

        :param key: key identifying the resource to get
        :type key: str
        :param snapshot: name of the snapshot under which the resource is stored, uses current snapshot by default
        :type snapshot: str
        :return: specified resource's text
        :rtype: str
        """
        return restv2helper.get_snapshot_object(self, key, snapshot)

    def put_snapshot_object(
        self, key: str, data: str, snapshot: Optional[str] = None
    ) -> None:
        """Put data as the snapshot object with specified key.

        :param key: key identifying the resource to upload
        :type key: str
        :param snapshot: name of the snapshot under which the resource is stored, uses current snapshot by default
        :type snapshot: str
        """
        restv2helper.put_snapshot_object(self, key, data, snapshot)

    def get_snapshot_input_object_stream(
        self, key: str, snapshot: Optional[str] = None
    ) -> BytesIO:
        """Return a binary stream of the content of an input object (part of the original snapshot data) with specified key.

        :param key: key identifying the resource to get
        :type key: str
        :param snapshot: name of the snapshot under which the resource is stored, uses current snapshot by default
        :type snapshot: str
        :return: stream containing the resource
        :rtype: BytesIO
        """
        return restv2helper.get_snapshot_input_object(self, key, snapshot)

    def get_snapshot_input_object_text(self, key, encoding="utf-8", snapshot=None):
        # type: (Text, Text, Optional[Text]) -> Text
        """Return the text content of an input object (part of the original snapshot data) with specified key.

        :param key: key identifying the resource to get
        :type key: str
        :param encoding: name of the encoding used to decode the snapshot input object
        :type key: str
        :param snapshot: name of the snapshot under which the resource is stored, uses current snapshot by default
        :type snapshot: str
        :return: specified resource's text
        :rtype: str
        """
        with self.get_snapshot_input_object_stream(key, snapshot) as stream:
            text = stream.read().decode(encoding)
        return str(text)

    def put_network_object(self, key: str, data: str) -> None:
        """
        Put data as the network object with specified key.

        :param key: key identifying the resource to upload
        :type key: str
        :param data: data to upload
        :type data: Any
        """
        restv2helper.put_network_object(self, key, data)

    def get_snapshot_input(self, zip_file_name, snapshot=None, overwrite=False):
        # type: (Text, Optional[Text], bool) -> None
        """
        Gets the data that was used to initialize the snapshot and writes that as a zip to file
        :param zip_file_name: the path to the zip file where to write the snapshot content
        :type zip_file_name: Text
        :param snapshot: name of the snapshot, uses current snapshot by default
        :type snapshot: Text
        :param overwrite: if the file already exists, whether it should be overwritten
        :type overwrite: bool
        """
        input_stream = self.get_snapshot_input_object_stream("", snapshot)
        if not overwrite and os.path.exists(zip_file_name):
            raise ValueError(
                "File '{}' already exists. Use overwrite=True if you want to overwrite it."
            )
        if zip_file_name is not None:
            with open(zip_file_name, "wb") as f:
                f.write(input_stream.read())

    def delete_topology_roots(self) -> None:
        """
        Deletes the list of topology roots.
        """
        self.delete_network_object(_NETWORK_OBJECT_TOPOLOGY_ROOTS)

    def get_topology_roots(self) -> List[str]:
        """
        Gets the list of topology roots.
        :return: returns the topology root nodes
        :rtype: List[str]
        """
        roots = json.loads(
            self.get_network_object_text(_NETWORK_OBJECT_TOPOLOGY_ROOTS)
        )  # type: List[str]
        return roots

    def put_topology_roots(self, roots: List[str]) -> None:
        """
        Puts the list of topology roots.
        :param roots: A list of nodes to use spanning-tree roots to build the topology layout.
        :type roots: List[str]
        """
        self.put_network_object(_NETWORK_OBJECT_TOPOLOGY_ROOTS, json.dumps(roots))

    def delete_topology_aggregates(self) -> None:
        """
        Deletes the topology aggregate definitions.
        """
        self.delete_network_object(_NETWORK_OBJECT_TOPOLOGY_AGGREGATES)

    def get_topology_aggregates(self) -> TopologyAggregates:
        """
        Gets the topology aggregate definitions.
        :return: returns the aggregate topology
        :rtype: TopologyAggregates
        """
        # TODO: update pybf to have correct types
        agg = TopologyAggregates.from_dict(
            json.loads(
                self.get_network_object_text(_NETWORK_OBJECT_TOPOLOGY_AGGREGATES)
            )
        )  # type: TopologyAggregates
        return agg

    def put_topology_aggregates(self, aggregates: TopologyAggregates) -> None:
        """
        Puts the topology aggregate definitions.
        :param aggregates: A TopologyAggregates object defining aggregates (groups) in the
        network. An aggregate is defined by its ID, its children (a list of names) and an
        optional human-friendly display name. Aggregates can contain network, routers, subnets,
        or other aggregates. No name should be listed in the children list of more than one
        aggregate.
        :type aggregates: TopologyAggregates
        """
        restv2helper.put_network_object(
            self,
            _NETWORK_OBJECT_TOPOLOGY_AGGREGATES,
            json.dumps(attr.asdict(aggregates)),
        )

    def delete_topology_positions(self):
        # type: () -> None
        """
        Deletes the topology positions.
        """
        restv2helper.delete_network_object(self, _NETWORK_OBJECT_TOPOLOGY_POSITIONS)

    def get_topology_positions(self) -> Dict[str, Dict[str, float]]:
        """
        Gets the topology positions.
        :return: A dictionary defining the position of nodes in the
        topology. A position is a dictionary with x and y keys. Any node
        absent from the dictionary will be assigned a position automatically.
        :rtype: Dict[str, Dict[str, float]]
        """
        # force type
        pos = json.loads(
            self.get_network_object_text(_NETWORK_OBJECT_TOPOLOGY_POSITIONS)
        )  # type: Dict[str, Dict[str, float]]
        return pos

    def put_topology_positions(self, positions):
        # type: (Dict[str, Dict[str, float]]) -> None
        """
        Puts the topology positions.
        :param positions: A dictionary defining the position of nodes in the
        topology. A position is a dictionary with x and y keys. Any node
        absent from the dictionary will be assigned a position automatically.
        :type positions: Dict[str, Dict[str, float]]
        """
        self.put_network_object(
            _NETWORK_OBJECT_TOPOLOGY_POSITIONS, json.dumps(positions)
        )

    def get_configuration_diffs(self, snapshot: str, reference: str) -> str:
        """
        Return the differences in configurations between two snapshots as a `diff` patch.

        :param snapshot: current snapshot
        :param reference: reference snapshot
        :return: the diff patch, as a string
        """
        qs = _bf_get_question_templates(self, verbose=True)
        qname = "__configdiffdetail"
        if qname not in qs:
            raise BatfishException("Configuration diff unavailable")
        name, q = _load_question_dict(json.loads(qs[qname]), self)
        fr = (
            q(context=3).answer(snapshot=snapshot, reference_snapshot=reference).frame()
        )
        return "".join(fr["Diff"])

    def set_network(
        self, name: Optional[str] = None, prefix: str = DEFAULT_NETWORK_PREFIX
    ) -> str:
        """
        Set current network.

        Creates the network if it does not already exist.

        :param name: name of the network to set. If `None`, a name will be generated
        :type name: str
        :param prefix: prefix to prepend to auto-generated network names if name is empty
        :type name: str

        :return: name of the configured network
        :rtype: str
        """
        if name is None:
            name = prefix + get_uuid()

        if name not in self.list_networks():
            self._create_network(name)

        self.network = name
        return name

    def list_network_metadata(self) -> List["NetworkMetadata"]:
        """Return list of network metadata for accessible networks."""
        from pybfe.datamodel.metadata import NetworkMetadata

        metadata = self._list_network_metadata()
        return [NetworkMetadata.from_message(m) for m in metadata]

    def list_networks(self, verbose: bool = False) -> List[str]:
        """Return list of ready, accessible networks."""
        from intentionet.bfe.proto.api_gateway_pb2 import NetworkStatus

        metadata = self._list_network_metadata()
        return [
            m.network_name
            for m in metadata
            if m.status == NetworkStatus.NETWORK_STATUS_READY
        ]

    def _list_network_metadata(self) -> "NetworkMetadataMessage":
        from intentionet.bfe.proto.api_gateway_pb2 import ListNetworkMetadataRequest

        req = ListNetworkMetadataRequest(credentials=self._credentials)
        return self._api_gw.ListNetworkMetadata(req).network_metadata

    def get_network_aggregates(self) -> Dict:
        """
        Get the network aggregates definition. This defines nested groups of devices in the network.
        """
        from intentionet.bfe.proto.api_gateway_pb2 import GetNetworkAggregatesRequest

        req = GetNetworkAggregatesRequest(
            credentials=self._credentials, network_name=self.network
        )
        resp = self._api_gw.GetNetworkAggregates(req)
        return MessageToDict(resp.aggregates)

    def put_network_aggregates(self, aggs_dict: Dict) -> None:
        """
        Put the network aggregates (groups) definition. This defines nested groups of devices in the network.

        The aggregates definition consists of a list of single-aggregate definitions. Each aggregate definition consists
        of:
        - A name.
        - A non-empty list of hostname patterns (similar to unix filesystem globs) that control which devices are to be
          included in the aggregate.
        - A possibly-empty list of sub-aggregates, or "children", of the aggregate.

        The order of aggregates in the top-level list and the children of an aggregate matters. If a hostname matches
        the patterns of more than one aggregate in the list, the device will be placed into the earliest one in the
        list.

        Example:

            session.put_network_aggregates([
                {
                    name: "site1",
                    patterns: ["site1*"],
                    children: [
                        {
                            name: "core",
                            patterns: ["*core*]
                        },
                        {
                            name: "border",
                            patterns: ["*border*", "*brdr*"]
                        }
                    ]
                },
                {
                    name: "site2",
                    patterns: ["site2*"],
                    children: [
                        {
                            name: "core",
                            patterns: ["*core*]
                        },
                        {
                            name: "border",
                            patterns: ["*border*", "*brdr*"]
                        }
                    ]
                }
            ])

        In this example, a device with hostname "site1-core1" will be placed in the "core" sub-aggregate of the "site1"
        aggregate. A device with hostname "site2-brdr3" will be placed in the "border" sub-aggregate of "site2". A
        device with hostname "site2-fwl3" will be placed in "site2" itself, not in any of its child sub-aggregates.
        A device with hostname "site3-core1" will not be placed in any aggregate, even though it matches the "core"
        sub-aggregates, because it does not match either "site1" or "site2".
        """
        from intentionet.bfe.proto.api_gateway_pb2 import PutNetworkAggregatesRequest
        from intentionet.bfe.proto.datamodel.aggregates_pb2 import NetworkAggregates

        req = PutNetworkAggregatesRequest(
            credentials=self._credentials,
            network_name=self.network,
            aggregates=ParseDict(aggs_dict, NetworkAggregates()),
        )
        self._api_gw.PutNetworkAggregates(req)

    def delete_network(self, name: str) -> None:
        """
        Delete network by name.

        :param name: name of the network to delete
        :type name: str
        """
        if name is None:
            raise ValueError("Must specify network to delete.")
        nets = self._list_network_metadata()  # type: List[NetworkMetadataMessage]
        if name not in [m.network_name for m in nets]:
            raise ValueError("Network {} was not found.".format(name))
        from intentionet.bfe.proto.api_gateway_pb2 import (
            DeleteNetworkRequest,
            NetworkStatus,
        )

        req = DeleteNetworkRequest(
            credentials=self._credentials, network_name=name, nonce=self._get_nonce()
        )
        self._api_gw.DeleteNetwork(req)
        self._wait_for_network(name, NetworkStatus.NETWORK_STATUS_NOT_FOUND)

    def _create_network(self, name: str) -> None:
        from intentionet.bfe.proto.api_gateway_pb2 import (
            CreateNetworkRequest,
            NetworkStatus,
        )

        req = CreateNetworkRequest(
            credentials=self._credentials, network_name=name, nonce=self._get_nonce()
        )
        self._api_gw.CreateNetwork(req)
        self._wait_for_network(name, NetworkStatus.NETWORK_STATUS_READY)

    def _wait_for_network(self, name: str, status: "NetworkStatus") -> None:
        """Wait for network to reach specified state."""
        from intentionet.bfe.proto.api_gateway_pb2 import (
            GetNetworkMetadataRequest,
            NetworkStatus,
        )

        done = False
        req = GetNetworkMetadataRequest(
            credentials=self._credentials, network_name=name
        )
        while not done:
            resp = self._api_gw.GetNetworkMetadata(req)
            current_status = resp.network_metadata.status
            if current_status == status:
                return
            if current_status == NetworkStatus.NETWORK_STATUS_NOT_FOUND:
                raise ValueError("Unknown network: {}".format(name))
            if current_status == NetworkStatus.NETWORK_STATUS_FAILED:
                raise Exception("Network failed")
            # TODO smarter sleeping
            time.sleep(1)  # seconds

    def _wait_for_snapshot(
        self, network: str, name: str, status: "SnapshotStatus"
    ) -> None:
        """Wait for snapshot to reach specified state."""
        from intentionet.bfe.proto.api_gateway_pb2 import (
            GetSnapshotMetadataRequest,
            SnapshotStatus,
        )

        done = False
        req = GetSnapshotMetadataRequest(
            credentials=self._credentials, network_name=network, snapshot_name=name
        )
        while not done:
            resp = self._api_gw.GetSnapshotMetadata(req)
            current_status = resp.snapshot_metadata.status
            if current_status == status:
                return
            if current_status == SnapshotStatus.SNAPSHOT_STATUS_NOT_FOUND:
                raise ValueError("Unknown snapshot: {}".format(name))
            if current_status == SnapshotStatus.SNAPSHOT_STATUS_FAILED:
                raise Exception("Snapshot failed")
            # TODO smarter sleeping
            time.sleep(1)  # seconds

    def fork_snapshot(
        self,
        base_name: str,
        name: Optional[str] = None,
        overwrite: bool = False,
        deactivate_interfaces: Optional[List[Interface]] = None,
        deactivate_nodes: Optional[List[str]] = None,
        restore_interfaces: Optional[List[Interface]] = None,
        restore_nodes: Optional[List[str]] = None,
        add_files: Optional[str] = None,
        extra_args: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Copy an existing snapshot and deactivate or reactivate specified interfaces and nodes.

        :param base_name: name of the snapshot to copy
        :type base_name: str
        :param name: name of the snapshot to initialize
        :type name: str
        :param overwrite: whether or not to overwrite an existing snapshot with the
            same name
        :type overwrite: bool
        :param deactivate_interfaces: list of interfaces to deactivate in new snapshot
        :type deactivate_interfaces: list[Interface]
        :param deactivate_nodes: list of names of nodes to deactivate in new snapshot
        :type deactivate_nodes: list[str]
        :param restore_interfaces: list of interfaces to reactivate
        :type restore_interfaces: list[Interface]
        :param restore_nodes: list of names of nodes to reactivate
        :type restore_nodes: list[str]
        :param add_files: path to zip file or directory containing files to add
        :type add_files: str
        :param extra_args: extra arguments to be passed to the parse command.
        :type extra_args: dict

        :return: name of initialized snapshot
        :rtype: str
        """
        self._check_network()
        assert self.network is not None  # guaranteed by check_network()
        network = self.network

        if name is None:
            name = DEFAULT_SNAPSHOT_PREFIX + get_uuid()
        assert name is not None

        if name in self._list_all_snapshots(network):
            if overwrite:
                self.delete_snapshot(name)
            else:
                raise ValueError(
                    "A snapshot named "
                    "{}"
                    " already exists in network "
                    "{}"
                    ". "
                    "Use overwrite = True if you want to overwrite the "
                    "existing snapshot".format(name, network)
                )

        if base_name not in self.list_snapshots():
            raise ValueError("Base snapshot is not ready.")

        self._api_gw.ForkSnapshot(
            ForkSnapshotRequest(
                credentials=self._credentials,
                network_name=network,
                snapshot_name=name,
                base_snapshot_name=base_name,
                zip_data=read_zip(add_files),
                nonce=self._get_nonce(),
                deactivate_nodes=_to_node_messages(deactivate_nodes),
                restore_nodes=_to_node_messages(restore_nodes),
                deactivate_interfaces=_to_interface_messages(deactivate_interfaces),
                restore_interfaces=_to_interface_messages(restore_interfaces),
            )
        )

        self._wait_for_snapshot(network, name, SnapshotStatus.SNAPSHOT_STATUS_READY)
        self.snapshot = name
        return name

    def init_snapshot(
        self,
        upload: str,
        name: Optional[str] = None,
        overwrite: bool = False,
        extra_args: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Initialize a new snapshot.

        :param upload: path to the snapshot zip or directory
        :type upload: str
        :param name: name of the snapshot to initialize
        :type name: str
        :param overwrite: whether or not to overwrite an existing snapshot with the
           same name
        :type overwrite: bool
        :param extra_args: extra arguments to be passed to the parse command
        :type extra_args: dict

        :return: name of initialized snapshot
        :rtype: str
        """
        return self._initialize_snapshot(
            upload, name=name, overwrite=overwrite, extra_args=extra_args
        )

    def init_snapshot_from_text(
        self,
        text: str,
        filename: Optional[str] = None,
        snapshot_name: Optional[str] = None,
        platform: Optional[str] = None,
        overwrite: bool = False,
        extra_args: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Initialize a snapshot of a single configuration file with given text.

        When `platform=None` the file contains the given text, unmodified. This
        means that the file text must indicate the platform of the vendor to
        Batfish, which is usually learned from headers that devices add in
        "show run"::

            boot nxos bootflash:nxos.7.0.3.I4.7.bin   (Cisco NX-OS)
            ! boot system flash:/vEOS-lab.swi         (Arista EOS)
            #TMSH-VERSION: 1.0                        (F5 Big-IP)
            !! IOS XR Configuration 5.2.4             (Cisco IOS XR)

        Alternately, you may supply the name of the platform in the `platform`
        argument.

        As usual, the hostname of the node will be parsed from the configuration
        text itself, and if not present Batfish will default to the provided
        filename.

        :param text: the contents of the file.
        :type text: str
        :param filename: name of the configuration file created, 'config' by
            default.
        :type filename: str
        :param snapshot_name: name of the snapshot to initialize
        :type snapshot_name: str
        :param platform: the RANCID router.db name for the device platform,
            i.e., "cisco-nx", "arista", "f5", or "cisco-xr" for above examples.
            See https://www.shrubbery.net/rancid/man/router.db.5.html
        :type platform: str
        :param overwrite: whether or not to overwrite an existing snapshot with
           the same name.
        :type overwrite: bool
        :param extra_args: extra arguments to be passed to the parse command
        :type extra_args: dict

        :return: name of initialized snapshot
        :rtype: str
        """
        if filename is None:
            filename = "config"

        contents = text_with_platform(text, platform)
        filepath = os.path.join("snapshot", "configs", filename)
        data = zip_from_file_text(contents, filepath)

        return self._initialize_snapshot(
            data, name=snapshot_name, overwrite=overwrite, extra_args=extra_args
        )

    def _experimental_init_partial_snapshot(
        self,
        path: Optional[str] = None,
        name: Optional[str] = None,
        add_files: Optional[Mapping[str, bytes]] = None,
        remove_dirs: Optional[Union[str, Iterable[str]]] = None,
        remove_files: Optional[Union[str, Iterable[str]]] = None,
    ) -> str:
        """
        Initialize a new snapshot by modifying the latest existing snapshot in a network.

        :param path: path to the snapshot zip or directory (to add/overwrite files)
        :param add_files: a mapping of file key to file contents, e.g., `{"configs/router1.cfg": b"hostname foo\n"}`
        :param remove_files: keys of files to delete from latest snapshot, e.g., `["configs/router1.cfg"]`
        :param remove_dirs: keys of directories to delete from latest snapshot, e.g., `["configs"]`
        :param name: name of the snapshot to initialize

        :return: name of initialized snapshot
        :rtype: str
        """
        if all(p is None for p in [path, add_files, remove_files, remove_dirs]):
            raise ValueError(
                "One of path, add_files, remove_files, or remove_dirs must be specified"
            )
        if self.network is None:
            network = self.set_network()
        else:
            network = self.network

        if name is None:
            name = DEFAULT_SNAPSHOT_PREFIX + get_uuid()
        assert name is not None

        if name in self._list_all_snapshots(network):
            raise ValueError(
                "A snapshot named {} already exists in network {}".format(
                    name, self.network
                )
            )

        from intentionet.bfe.proto.api_gateway_pb2 import (
            ForkFromMasterSnapshotRequest,
            UploadFile,
            RemoveFile,
        )

        request = ForkFromMasterSnapshotRequest(
            network_name=network,
            snapshot_name=name,
            credentials=self._credentials,
            nonce=self._get_nonce(),
        )
        if remove_files is not None:
            if isinstance(remove_files, str):
                # accept single key
                remove_files = [remove_files]
            request.remove_files.extend(RemoveFile(key=x) for x in remove_files)
        if remove_dirs is not None:
            if isinstance(remove_dirs, str):
                # accept single key
                remove_dirs = [remove_dirs]
            request.remove_dirs.extend(RemoveFile(key=x) for x in remove_dirs)

        if add_files is not None:
            request.files.extend(
                UploadFile(key=k, contents=v) for k, v in add_files.items()
            )

        if path is not None:
            if not isinstance(path, str):
                raise ValueError("Please pass a path to directory or zip file.")

            if os.path.isdir(path):
                # walk the dir
                for root, _dirs, files in os.walk(path):
                    for f in files:
                        filename = os.path.join(root, f)
                        key = os.path.relpath(filename, path)
                        with open(filename, "rb") as fio:
                            request.files.append(
                                UploadFile(key=key, contents=fio.read())
                            )
            elif os.path.isfile(path):
                # walk zip entries
                if not zipfile.is_zipfile(path):
                    raise ValueError("{} is not a valid zip file".format(path))
                with zipfile.ZipFile(
                    path, "r", zipfile.ZIP_DEFLATED, allowZip64=False
                ) as in_zip:
                    for entry in in_zip.infolist():

                        key = entry.filename.split("/")[1]
                        if not key:
                            continue
                        request.files.append(
                            UploadFile(key=key, value=in_zip.read(entry))
                        )
            else:
                raise ValueError("Supplied path does not exist: {}".format(path))

        self._api_gw.ForkFromMasterSnapshot(request)

        self._wait_for_snapshot(network, name, SnapshotStatus.SNAPSHOT_STATUS_READY)

        self.snapshot = name
        return name

    def _initialize_snapshot(
        self,
        upload: Union[str, IO],
        name: Optional[str] = None,
        overwrite: bool = False,
        extra_args: Optional[Dict[str, str]] = None,
    ) -> str:
        if self.network is None:
            network = self.set_network()
        else:
            network = self.network

        if name is None:
            name = DEFAULT_SNAPSHOT_PREFIX + get_uuid()
        assert name is not None

        if name in self._list_all_snapshots(network):
            if overwrite:
                self.delete_snapshot(name)
            else:
                raise ValueError(
                    "A snapshot named "
                    "{}"
                    " already exists in network "
                    "{}"
                    ". "
                    "Use overwrite = True if you want to overwrite the "
                    "existing snapshot".format(name, network)
                )

        if isinstance(upload, str):
            # Upload is file/directory path
            self._init_snapshot_from_file(name, upload)
        else:
            # Upload is IO
            if not zipfile.is_zipfile(upload):
                raise ValueError("The provided data is not a valid zip file")
            self._init_snapshot_from_io(name, upload)

        from intentionet.bfe.proto.api_gateway_pb2 import SnapshotStatus

        self._wait_for_snapshot(network, name, SnapshotStatus.SNAPSHOT_STATUS_READY)

        self.snapshot = name
        return name

    def _init_snapshot_from_file(self, name: str, file_to_send: str) -> None:
        if os.path.isdir(file_to_send):
            data = zip_from_dir(file_to_send)
            self._init_snapshot_from_io(name, data)
        elif os.path.isfile(file_to_send):
            if not zipfile.is_zipfile(file_to_send):
                raise ValueError("{} is not a valid zip file".format(file_to_send))
            with open(file_to_send, "rb") as fd:
                self._init_snapshot_from_io(name, fd)
        else:
            raise ValueError("Supplied path does not exist: {}".format(file_to_send))

    def _init_snapshot_from_io(self, name: str, fd: IO) -> None:
        from intentionet.bfe.proto.api_gateway_pb2 import InitSnapshotRequest

        # Seek to origin so the full zip data is read
        if fd.seekable():
            fd.seek(0)
        else:
            # Should not get here since IO is constructed internally
            raise ValueError("Cannot prepare snapshot input for upload")
        req = InitSnapshotRequest(
            credentials=self._credentials,
            network_name=self.network,
            snapshot_name=name,
            zip_data=fd.read(),
            nonce=self._get_nonce(),
        )
        self._api_gw.InitSnapshot(req)

    def list_snapshot_metadata(self) -> List["SnapshotMetadata"]:
        """List metadata for snapshots in the current network."""
        from pybfe.datamodel.metadata import SnapshotMetadata

        self._check_network()
        # Guaranteed by check_network
        assert self.network is not None
        metadata = self._list_snapshot_metadata(network=self.network)
        return [SnapshotMetadata.from_message(m) for m in metadata]

    def list_snapshots(
        self, verbose: bool = False
    ) -> Union[List[str], List[Dict[str, "SnapshotMetadata"]]]:
        """
        List snapshots for the current network.

        :param verbose: If true, return the full output of Batfish Enterprise, including
            snapshot metadata.
        :type verbose: bool

        :return: snapshot names or the full response containing snapshots and metadata (if `verbose=True`)
        :rtype: List
        """
        from intentionet.bfe.proto.api_gateway_pb2 import SnapshotStatus
        from pybfe.datamodel.metadata import SnapshotMetadata

        self._check_network()
        # Guaranteed by check_network
        assert self.network is not None
        metadata = self._list_snapshot_metadata(network=self.network)
        if verbose:
            # TODO remove verbose flag
            return [
                {m.snapshot_name: SnapshotMetadata.from_message(m)} for m in metadata
            ]
        return [
            s.snapshot_name
            for s in metadata
            if s.status == SnapshotStatus.SNAPSHOT_STATUS_READY
        ]

    def _list_all_snapshots(self, network: str) -> List[str]:
        """List all snapshots associated with specified network, even those that are pending/failed."""
        return [s.snapshot_name for s in self._list_snapshot_metadata(network)]

    def _list_snapshot_metadata(self, network: str) -> List["SnapshotMetadataMessage"]:
        from intentionet.bfe.proto.api_gateway_pb2 import ListSnapshotMetadataRequest

        req = ListSnapshotMetadataRequest(
            credentials=self._credentials, network_name=network
        )
        # list copy is needed if we want this to be a list. Proto repeated messages are *not* lists.
        return list(self._api_gw.ListSnapshotMetadata(req).snapshot_metadata)

    def delete_snapshot(self, name: str) -> None:
        """
        Delete specified snapshot from current network.

        :param name: name of the snapshot to delete
        :type name: str
        """
        self._check_network()
        if self.network not in self.list_networks():
            raise ValueError("Network {} was not found.".format(self.network))

        if name not in self._list_all_snapshots(self.network):
            raise ValueError("Snapshot {} was not found.".format(name))

        from intentionet.bfe.proto.api_gateway_pb2 import (
            DeleteSnapshotRequest,
            SnapshotStatus,
        )

        req = DeleteSnapshotRequest(
            credentials=self._credentials,
            snapshot_name=name,
            network_name=self.network,
            nonce=self._get_nonce(),
        )
        self._api_gw.DeleteSnapshot(req)
        self._wait_for_snapshot(
            network=self.network,
            name=name,
            status=SnapshotStatus.SNAPSHOT_STATUS_NOT_FOUND,
        )

    def get_data_retention_policy(self) -> DataRetentionPolicy:
        """Returns the active Batfish Enterprise data retention policy"""
        return self._api_gw.GetDataRetentionPolicy(
            GetDataRetentionPolicyRequest()
        ).policy

    def update_data_retention_policy(
        self, policy: Union[Dict, DataRetentionPolicy]
    ) -> None:
        """Updates the active Batfish Enterprise data retention policy

        A data retention policy contains:
        - max_age: the maximum snapshot age in seconds of a snapshot before it is removed
            automatically. A value of 0 or absent value indicates that snapshots should be kept
            forever.
        - enforcement_interval: how often in seconds automatic removal of snapshots older than the
            maximum age occurs. A value of 0 or absent value is interpreted to mean 1 second.

        :param policy: The new data retention policy to enforce
        :type policy: Union[Dict, DataRetentionPolicy]"""

        # Validate input
        if isinstance(policy, Dict):
            new_policy = ParseDict(policy, DataRetentionPolicy())
        elif isinstance(policy, DataRetentionPolicy):
            new_policy = policy
        else:
            raise ValueError(
                "Unknown data retention policy type ({}).".format(type(policy))
            )

        self._update_data_retention_policy(new_policy)

    def _update_data_retention_policy(self, policy: DataRetentionPolicy) -> None:
        self._api_gw.UpdateDataRetentionPolicy(
            UpdateDataRetentionPolicyRequest(policy=policy)
        )

    def _experimental_create_policy(
        self, assertion: Union[Dict, AssertionInput], network: Optional[str] = None,
    ) -> PolicyId:
        """
        Create a managed policy on the specified network, from the specified assertion input.
        Newly created policies will not run on previously initialized snapshots, but will run on new snapshots initialized in this network.

        Example:

            session.create_policy(
                assertion={
                    "title": "Check Core NTP Servers",
                    "description": "Check that all core nodes have exactly the set of expected NTP servers",
                    "devices_have_servers": {
                        "devices": {"hostname": {"regex": ".*core.*",}},
                        "servers": {"ntp": {"set": {"equals": {"items": ["10.10.10.10", "10.10.10.110"]},}},},
                    }
                },
                network="network_name",
            )

        :param assertion: assertion definition for the new, managed policy
        :type assertion: Union[Dict, AssertionInput]
        :param network: name of the network to add the policy to, if not specified, the session's current network will be used
        :type network: Optional[str]
        :return: Identifier for the new managed policy
        :rtype PolicyId:
        """
        network = self._get_network_or_raise(network)
        assertion_input = Asserts._to_assertion_input(assertion)

        # Create & run the assertion
        req = CreatePolicyRequest(
            credentials=self._credentials,
            network_name=network,
            policy=Policy(
                # Omit uid, so one is provided by backend
                input=assertion_input,
            ),
        )
        res = self._api_gw.CreatePolicy(request=req)
        return res.policy_id

    def _experimental_list_policies(
        self, network: Optional[str] = None,
    ) -> Iterable[Policy]:
        """
        List managed policies for the specified network.

        :return: List of managed policies associated with this network
        :rtype Iterable[Policy]:
        """
        network = self._get_network_or_raise(network)

        req = ListPoliciesRequest(credentials=self._credentials, network_name=network,)
        res = self._api_gw.ListPolicies(request=req)
        policies = res.policies  # type: Iterable[Policy]
        return policies

    def delete_node_role_dimension(self, dimension: str) -> None:
        """
        Deletes the definition of the given role dimension for the active network.

        :param dimension: name of the dimension to delete
        :type dimension: str
        """
        restv2helper.delete_node_role_dimension(self, dimension)

    def delete_reference_book(self, name: str) -> None:
        """
        Deletes the reference book with the specified name for the active network.

        :param name: name of the reference book to delete
        :type name: str
        """
        restv2helper.delete_reference_book(self, name)

    def _get_answer(
        self, question: str, snapshot: str, reference_snapshot: Optional[str] = None
    ) -> Answer:
        """
        Get the answer for a previously asked question.

        :param question: the unique identifier of the previously asked question
        :type question: str
        :param snapshot: name of the snapshot the question was run on
        :type snapshot: str
        :param reference_snapshot: if present, gets the answer for a differential question asked against the specified reference snapshot
        :type reference_snapshot: str
        :return: answer to the specified question
        :rtype: :py:class:`Answer`
        """
        params = {"snapshot": snapshot, "referenceSnapshot": reference_snapshot}
        ans = restv2helper.get_answer(self, question, params)
        if is_table_ans(ans):
            return TableAnswer(ans)
        else:
            return Answer(ans)

    def get_node_role_dimension(
        self, dimension: str, inferred: bool = False
    ) -> NodeRoleDimension:
        """
        Returns the definition of the given node role dimension for the active network or inferred definition for the active snapshot.

        :param dimension: name of the node role dimension to fetch
        :type dimension: str
        :param inferred: whether or not to fetch active snapshot's inferred node role dimension
        :type inferred: bool

        :return: the definition of the given node role dimension for the active network, or inferred definition for the active snapshot if inferred=True.
        :rtype: :class:`~pybatfish.datamodel.referencelibrary.NodeRoleDimension`
        """
        if inferred:
            self._check_snapshot()
            return NodeRoleDimension.from_dict(
                restv2helper.get_snapshot_inferred_node_role_dimension(self, dimension)
            )
        return NodeRoleDimension.from_dict(
            restv2helper.get_node_role_dimension(self, dimension)
        )

    def get_node_roles(self, inferred: bool = False) -> NodeRolesData:
        """
        Returns the definitions of node roles for the active network or inferred roles for the active snapshot.

        :param inferred: whether or not to fetch the active snapshot's inferred node roles
        :type inferred: bool

        :return: the definitions of node roles for the active network, or inferred definitions for the active snapshot if inferred=True.
        :rtype: :class:`~pybatfish.datamodel.referencelibrary.NodeRolesData`
        """
        if inferred:
            self._check_snapshot()
            return NodeRolesData.from_dict(
                restv2helper.get_snapshot_inferred_node_roles(self)
            )
        return NodeRolesData.from_dict(restv2helper.get_node_roles(self))

    def get_reference_book(self, name: str) -> ReferenceBook:
        """
        Returns the specified reference book for the active network.

        :param name: name of the reference book to fetch
        :type name: str
        """
        return ReferenceBook.from_dict(restv2helper.get_reference_book(self, name))

    def get_reference_library(self) -> ReferenceLibrary:
        """Returns the reference library for the active network."""
        return ReferenceLibrary.from_dict(restv2helper.get_reference_library(self))

    def get_snapshot(self, snapshot: Optional[str] = None) -> str:
        """
        Get the specified or active snapshot name.

        :param snapshot: if specified, this name is returned instead of active snapshot
        :type snapshot: str

        :return: name of the active snapshot, or the specified snapshot if applicable
        :rtype: str

        :raises ValueError: if there is no active snapshot and no snapshot was specified
        """
        if snapshot is not None:
            return str(snapshot)
        elif self.snapshot is not None:
            return self.snapshot
        else:
            raise ValueError(
                "snapshot must be either provided or set using "
                "Session.set_snapshot (e.g. session.set_snapshot('NAME'))"
            )

    def list_incomplete_works(self) -> Dict[str, Any]:
        """
        Get pending work that is incomplete.

        :return: JSON dictionary of question name to question object
        :rtype: dict
        """
        json_data = workhelper.get_data_list_incomplete_work(self)
        response = resthelper.get_json_response(
            self, CoordConsts.SVC_RSC_LIST_INCOMPLETE_WORK, json_data
        )
        return response

    def put_reference_book(self, book: ReferenceBook) -> None:
        """
        Put a reference book in the active network.

        If a book with the same name exists, it is overwritten.

        :param book: The ReferenceBook object to add
        :type book: :class:`~pybatfish.datamodel.referencelibrary.ReferenceBook`
        """
        restv2helper.put_reference_book(self, book)

    def put_node_role_dimension(self, dimension: NodeRoleDimension) -> None:
        """
        Put a role dimension in the active network.

        Overwrites the old dimension if one of the same name already exists.

        Individual role dimension mappings within the dimension must have a valid (java) regex.

        :param dimension: The NodeRoleDimension object for the dimension to add
        :type dimension: :class:`~pybatfish.datamodel.referencelibrary.NodeRoleDimension`
        """
        restv2helper.put_node_role_dimension(self, dimension)

    def put_node_roles(self, node_roles_data: NodeRolesData) -> None:
        """
        Writes the definitions of node roles for the active network. Completely replaces any existing definitions.

        :param node_roles_data: node roles definitions to add to the active network
        :type node_roles_data: :class:`~pybatfish.datamodel.referencelibrary.NodeRolesData`
        """
        restv2helper.put_node_roles(self, node_roles_data)

    def upload_diagnostics(
        self,
        dry_run: bool = True,
        netconan_config: Optional[str] = None,
        contact_info: Optional[str] = None,
        proxy: Optional[str] = None,
    ) -> str:
        raise NotImplementedError("Not implemented for pybfe")


class GRPCSession(Session):
    pass
