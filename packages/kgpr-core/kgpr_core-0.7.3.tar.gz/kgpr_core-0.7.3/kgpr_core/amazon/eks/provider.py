from kubragen.consts import PROVIDER_AMAZON, PROVIDERSVC_AMAZON_EKS
from kubragen.provider import Provider


class ProviderAmazonEKS(Provider):
    """
    Provider for Amazon EKS.
    """
    def __init__(self):
        super().__init__(PROVIDER_AMAZON, PROVIDERSVC_AMAZON_EKS)
