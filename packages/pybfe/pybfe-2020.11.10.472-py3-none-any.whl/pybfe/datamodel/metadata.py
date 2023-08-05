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
import attr


@attr.s(frozen=True)
class NetworkMetadata(object):
    """Metadata for a network."""

    from intentionet.bfe.proto.api_gateway_pb2 import (
        NetworkMetadata as NetworkMetadataMessage,
    )

    network_name = attr.ib(type=str)
    status = attr.ib(type=str)

    @classmethod
    def from_message(cls, message: NetworkMetadataMessage) -> "NetworkMetadata":
        from intentionet.bfe.proto.api_gateway_pb2 import NetworkStatus

        return NetworkMetadata(
            network_name=message.network_name, status=NetworkStatus.Name(message.status)
        )


@attr.s(frozen=True)
class SnapshotMetadata(object):
    """Metadata for a snapshot."""

    from intentionet.bfe.proto.api_gateway_pb2 import (
        SnapshotMetadata as SnapshotMetadataMessage,
    )

    snapshot_name = attr.ib(type=str)
    status = attr.ib(type=str)

    @classmethod
    def from_message(cls, message: SnapshotMetadataMessage) -> "SnapshotMetadata":
        from intentionet.bfe.proto.api_gateway_pb2 import SnapshotStatus

        return SnapshotMetadata(
            snapshot_name=message.snapshot_name,
            status=SnapshotStatus.Name(message.status),
        )
