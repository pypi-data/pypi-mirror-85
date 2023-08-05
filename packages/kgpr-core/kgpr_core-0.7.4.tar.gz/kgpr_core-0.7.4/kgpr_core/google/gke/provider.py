from kubragen.consts import PROVIDER_GOOGLE, PROVIDERSVC_GOOGLE_GKE
from kubragen.provider import Provider


class ProviderGoogleGKE(Provider):
    """
    Provider for Google GKE.
    """
    def __init__(self):
        super().__init__(PROVIDER_GOOGLE, PROVIDERSVC_GOOGLE_GKE)
