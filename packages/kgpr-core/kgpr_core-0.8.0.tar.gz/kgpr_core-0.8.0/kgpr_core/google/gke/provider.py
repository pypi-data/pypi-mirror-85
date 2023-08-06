from typing import Optional, Union

import semver
from kubragen.consts import PROVIDER_GOOGLE, PROVIDERSVC_GOOGLE_GKE
from kubragen.provider import Provider


class ProviderGoogleGKE(Provider):
    """
    Provider for Google GKE.
    """
    def __init__(self, kubernetes_version: Optional[Union[str, semver.VersionInfo]] = None):
        super().__init__(provider=PROVIDER_GOOGLE, service=PROVIDERSVC_GOOGLE_GKE,
                         kubernetes_version=kubernetes_version)
