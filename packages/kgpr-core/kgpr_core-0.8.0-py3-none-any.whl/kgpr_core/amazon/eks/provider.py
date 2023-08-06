from typing import Optional, Union

import semver
from kubragen.consts import PROVIDER_AMAZON, PROVIDERSVC_AMAZON_EKS
from kubragen.provider import Provider


class ProviderAmazonEKS(Provider):
    """
    Provider for Amazon EKS.
    """
    def __init__(self, kubernetes_version: Optional[Union[str, semver.VersionInfo]] = None):
        super().__init__(provider=PROVIDER_AMAZON, service=PROVIDERSVC_AMAZON_EKS,
                         kubernetes_version=kubernetes_version)
