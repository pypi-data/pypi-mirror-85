from typing import Optional, Union

import semver
from kubragen.consts import PROVIDER_DIGITALOCEAN, \
    PROVIDERSVC_DIGITALOCEAN_KUBERNETES
from kubragen.provider import Provider


class ProviderDigitalOceanKubernetes(Provider):
    """
    Provider for DigitalOcean Kubernetes.
    """
    def __init__(self, kubernetes_version: Optional[Union[str, semver.VersionInfo]] = None):
        super().__init__(provider=PROVIDER_DIGITALOCEAN, service=PROVIDERSVC_DIGITALOCEAN_KUBERNETES,
                         kubernetes_version=kubernetes_version)
