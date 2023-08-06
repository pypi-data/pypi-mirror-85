from typing import Optional, Union

import semver
from kubragen.consts import PROVIDER_K3D, PROVIDERSVC_GENERIC
from kubragen.provider import Provider


class ProviderK3DGeneric(Provider):
    """
    Provider for K3D.
    """
    def __init__(self, kubernetes_version: Optional[Union[str, semver.VersionInfo]] = None):
        super().__init__(provider=PROVIDER_K3D, service=PROVIDERSVC_GENERIC,
                         kubernetes_version=kubernetes_version)
