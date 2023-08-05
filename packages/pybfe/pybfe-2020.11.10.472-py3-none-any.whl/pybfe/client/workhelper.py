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
"""A collection of functions that execute RPCs against a Batfish server."""

from __future__ import absolute_import, print_function

import datetime
import json
import logging
import string
import tempfile
import time
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Tuple, Union

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal
from pybatfish.client.consts import BfConsts, CoordConsts, WorkStatusCode
from pybatfish.client.workitem import WorkItem
from pybatfish.exception import BatfishException

from . import resthelper, restv2helper

if TYPE_CHECKING:
    from pybfe.client.session import Session

# Maximum log length to display on execution errors, so we don't overload user with a huge log string
MAX_LOG_LENGTH = 64 * 1024


def _batch_desc(json_batch: Dict) -> str:
    """Get a string representation of the Batfish job batch."""
    description = json_batch.get("description", "").strip()  # type: str
    if json_batch["size"] > 0:
        description = "{desc} {completed} / {size}".format(
            desc=description, completed=json_batch["completed"], size=json_batch["size"]
        )
    if not description.endswith(tuple(string.punctuation)):
        description += "."
    return description


def _parse_timestamp(timestamp_str: str) -> datetime.datetime:
    """Convert the given Batfish date string into a printable local time."""
    try:
        # Attempt to parse a Unix timestamp in milliseconds
        millis = int(timestamp_str)
        return datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=millis)
    except ValueError:
        # Parse a RFC 3339 timestamp
        return parse(timestamp_str)


def _print_timestamp(timestamp: datetime.datetime) -> str:
    # Print the timestamp in the appropriate locale
    return timestamp.astimezone(tzlocal()).isoformat(sep=" ")


def execute(
    work_item: WorkItem,
    session: "Session",
    background: bool = False,
    extra_args: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Submit a work item to Batfish.

    :param work_item: work to submit
    :type work_item: :py:class:`~pybatfish.client.WorkItem`
    :param session: Batfish session to use.
    :type session: :py:class:`~pybatfish.client.session.Session`
    :param background: Whether to background the job. If `True`,
        this function only returns the result of submitting the job.
    :type background: bool
    :param extra_args: extra arguments to be passed to Batfish.
    :type extra_args: dict

    :return: If `background=True`, a dict containing a single key 'result' with
    a string description of the result. If `background=False`, a dict containing
    a single key 'status' with a string describing work status.
    """
    if extra_args is not None:
        work_item.requestParams.update(extra_args)

    snapshot = work_item.requestParams.get(BfConsts.ARG_TESTRIG)
    if snapshot is None:
        raise ValueError(
            "Work item {} does not include a snapshot name".format(work_item.to_json())
        )

    json_data = {
        CoordConsts.SVC_KEY_WORKITEM: work_item.to_json(),
        CoordConsts.SVC_KEY_API_KEY: session.api_key,
    }  # type: Dict[str, Optional[Union[str, Tuple[str,str]]]]

    # Submit the work item
    response = resthelper.get_json_response(
        session, CoordConsts.SVC_RSC_QUEUE_WORK, json_data
    )

    if background:
        # TODO: this is ugly and messes with return types: design and write async replacement
        # After we drop 2.7 support
        return {"result": str(response["result"])}

    answer = get_work_status(work_item.id, session)
    status = WorkStatusCode(answer[CoordConsts.SVC_KEY_WORKSTATUS])
    task_details = answer[CoordConsts.SVC_KEY_TASKSTATUS]

    cur_sleep = 0.1  # seconds
    while not WorkStatusCode.is_terminated(status):
        _print_work_status(session, status, task_details)
        time.sleep(cur_sleep)
        cur_sleep = min(1.0, cur_sleep * 1.5)
        answer = get_work_status(work_item.id, session)
        status = WorkStatusCode(answer[CoordConsts.SVC_KEY_WORKSTATUS])
        task_details = answer[CoordConsts.SVC_KEY_TASKSTATUS]

    _print_work_status(session, status, task_details)

    # Handle fail conditions not producing logs
    if status in [WorkStatusCode.ASSIGNMENTERROR, WorkStatusCode.REQUEUEFAILURE]:
        raise BatfishException(
            "Work finished with status {}\nwork_item: {}\ntask_details: {}".format(
                status, work_item.to_json(), json.loads(task_details)
            )
        )

    # Handle fail condition with logs
    if status == WorkStatusCode.TERMINATEDABNORMALLY:
        log = restv2helper.get_work_log(session, snapshot, work_item.id)
        log_file_msg = ""
        if len(log) > MAX_LOG_LENGTH:
            log_file = tempfile.NamedTemporaryFile().name
            with open(log_file, "w") as log_file_handle:
                log_file_handle.write(str(log))
            log_file_msg = "Full log written to {}\n".format(log_file)
        raise BatfishException(
            "Work terminated abnormally\nwork_item: {item}\n\n{msg}log: {prefix}{log}".format(
                item=work_item.to_json(),
                msg=log_file_msg,
                log=log[-MAX_LOG_LENGTH:],
                prefix="..." if log_file_msg else "",
            )
        )

    return {"status": status}


def _format_elapsed_time(delta):
    return "{years}{months}{days}{hours}:{minutes}:{seconds}".format(
        years="%dy" % delta.years if delta.years else "",
        months="%dm" % delta.months if delta.months else "",
        days="%dd" % delta.days if delta.days else "",
        hours="%02d" % delta.hours,
        minutes="%02d" % delta.minutes,
        seconds="%02d" % delta.seconds,
    )


def get_data_upload_question(
    session: "Session", question_name: str, question_json: str
) -> Dict[str, Optional[Union[str, Tuple[str, str]]]]:
    """Create the form parameters needed to upload the given question."""
    if not session.network:
        raise ValueError("Network must be set to upload question")
    return {
        CoordConsts.SVC_KEY_API_KEY: session.api_key,
        CoordConsts.SVC_KEY_NETWORK_NAME: session.network,
        CoordConsts.SVC_KEY_QUESTION_NAME: question_name,
        CoordConsts.SVC_KEY_FILE: ("question", question_json),
    }


def get_data_list_incomplete_work(session):
    json_data = {
        CoordConsts.SVC_KEY_API_KEY: session.api_key,
        CoordConsts.SVC_KEY_NETWORK_NAME: session.network,
    }
    return json_data


def get_workitem_answer(
    session: "Session",
    question_name: str,
    snapshot: str,
    reference_snapshot: Optional[str] = None,
) -> WorkItem:
    """Return the result of submitting a question as a WorkItem."""
    work_item = WorkItem(session)

    parameters = {
        BfConsts.COMMAND_ANSWER: "",
        BfConsts.ARG_QUESTION_NAME: question_name,
        BfConsts.ARG_TESTRIG: snapshot,
    }

    if reference_snapshot is not None:
        parameters[BfConsts.ARG_DELTA_TESTRIG] = reference_snapshot
        parameters[BfConsts.ARG_DIFFERENTIAL] = ""

    work_item.requestParams.update(parameters)

    return work_item


def get_workitem_generate_dataplane(session: "Session", snapshot: str) -> WorkItem:
    w_item = WorkItem(session)
    w_item.requestParams[BfConsts.COMMAND_DUMP_DP] = ""
    w_item.requestParams[BfConsts.ARG_TESTRIG] = snapshot
    return w_item


def get_work_status(w_item_id, session):
    json_data = {
        CoordConsts.SVC_KEY_API_KEY: session.api_key,
        CoordConsts.SVC_KEY_WORKID: w_item_id,
    }

    answer = resthelper.get_json_response(
        session, CoordConsts.SVC_RSC_GET_WORKSTATUS, json_data
    )

    if CoordConsts.SVC_KEY_WORKSTATUS in answer:
        return answer
    else:
        raise BatfishException(
            "Expected key (%s) not found in status check response: %s"
            % (CoordConsts.SVC_KEY_WORKSTATUS, answer)
        )


def _print_work_status(
    session: "Session", work_status: WorkStatusCode, task_details: str
) -> None:
    _print_work_status_helper(session, work_status, task_details, datetime.datetime.now)


def _print_work_status_helper(
    session: "Session",
    work_status: WorkStatusCode,
    task_details: str,
    now_function: Callable[[Any], datetime.datetime],
) -> None:
    # type of now_function first arg should be Optional[datetime.tzinfo] instead of Any, but mypy complains for some reason
    logger = logging.getLogger(__name__)
    if (
        logger.getEffectiveLevel() == logging.INFO
        or logger.getEffectiveLevel() == logging.DEBUG
    ):
        logger.info("status: {}".format(work_status))

        json_task = json.loads(task_details)
        if not json_task:
            logger.info(".... no task information")
            return

        batches = json_task["batches"] if "batches" in json_task else []
        if not batches:
            return

        # Compute when the task started.
        task_start_time = _parse_timestamp(json_task["obtained"])
        task_start_time_str = _print_timestamp(task_start_time)

        # Compute how much time has elapsed in this task.
        now = now_function(task_start_time.tzinfo)

        # If true, print the elapsed time since the task started.
        print_elapsed = (now - task_start_time).total_seconds() > session.elapsed_delay

        # Only print info about finished batches in debug mode
        if logger.isEnabledFor(logging.DEBUG):
            for batch in batches[:-1]:
                logger.debug(
                    ".... {start} {batch}".format(
                        start=task_start_time_str, batch=_batch_desc(batch)
                    )
                )

        lastbatch = batches[-1]
        total_time_str = ""
        if print_elapsed:
            total_time = relativedelta(now, task_start_time)
            total_time_str = " ({total} elapsed)".format(
                total=_format_elapsed_time(total_time)
            )

        logger.info(
            ".... {start} {batch}{total}".format(
                start=task_start_time_str,
                batch=_batch_desc(lastbatch),
                total=total_time_str,
            )
        )
