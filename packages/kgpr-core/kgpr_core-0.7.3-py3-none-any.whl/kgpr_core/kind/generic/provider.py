from kubragen.consts import PROVIDERSVC_GENERIC, PROVIDER_KIND
from kubragen.provider import Provider


class ProviderKINDGeneric(Provider):
    """
    Provider for KIND.
    """
    def __init__(self):
        super().__init__(PROVIDER_KIND, PROVIDERSVC_GENERIC)
