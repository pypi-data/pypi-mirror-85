from typing import Optional, Union

import semver
from kubragen.consts import PROVIDERSVC_GENERIC, PROVIDER_KIND
from kubragen.provider import Provider


class ProviderKINDGeneric(Provider):
    """
    Provider for KIND.
    """
    def __init__(self, kubernetes_version: Optional[Union[str, semver.VersionInfo]] = None):
        super().__init__(provider=PROVIDER_KIND, service=PROVIDERSVC_GENERIC,
                         kubernetes_version=kubernetes_version)
