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
from typing import List

import attr


@attr.s()
class Aggregate(object):
    """An element in the aggregate topology"""

    id = attr.ib()  # type: str
    children = attr.ib()  # type: List[str]
    human_name = attr.ib(default=None)  # type: str

    def __attrs_post_init__(self):
        if self.human_name is None:
            self.human_name = self.id


@attr.s
class TopologyAggregates(object):
    "Represents the aggregate topology"

    aggregates = attr.ib()  # type: List[Aggregate]

    @classmethod
    def from_dict(cls, json_dict):
        return TopologyAggregates(
            aggregates=[Aggregate(**a) for a in json_dict.get("aggregates", [])]
        )
