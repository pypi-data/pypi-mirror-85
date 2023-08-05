import base64
from typing import TYPE_CHECKING

from grpc import AuthMetadataContext, AuthMetadataPlugin, AuthMetadataPluginCallback

from intentionet.bfe.proto.auth.credentials_pb2 import Credentials, WebAccessToken

if TYPE_CHECKING:
    from pybfe.client.session import Session


class CallCredentialsPlugin(AuthMetadataPlugin):
    """Plugin that adds BFE session credentials to every GRPC's call context"""

    def __init__(self, session: "Session") -> None:
        self._session = session

    def __call__(
        self, context: AuthMetadataContext, callback: AuthMetadataPluginCallback
    ) -> None:
        metadata = (
            []
            if self._session.access_token is None
            else list(
                {
                    "authorization": base64.b64encode(
                        Credentials(
                            web_access_token=WebAccessToken(
                                secret=base64.decodebytes(
                                    self._session.access_token.encode()
                                )
                            )
                        ).SerializeToString()
                    )
                }.items()
            )
        )
        callback(
            metadata, None,
        )
