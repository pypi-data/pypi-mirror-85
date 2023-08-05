from typing import Optional, Any

from kubragen.helper import QuotedStr
from kubragen.kresource import KRPersistentVolumeProfile_CSI, KResourceDatabase
from kubragen.merger import Merger
from kubragen.object import ObjectItem
from kubragen.provider import Provider


class KRPersistentVolumeProfile_CSI_DOBS(KRPersistentVolumeProfile_CSI):
    """
    A PersisteVolume builder for DigitalOcean Kubernetes Storage using the CSI driver.

    .. seealso:: `How to Add Block Storage Volumes to Kubernetes Clusters <https://www.digitalocean.com/docs/kubernetes/how-to/add-volumes/>`_.
    """
    noformat: Optional[bool]

    def __init__(self, storageclass: Optional[str] = None, noformat: Optional[bool] = True):
        super().__init__(storageclass)
        self.noformat = noformat

    def build(self, provider: Provider, resources: KResourceDatabase, name: str,
              config: Optional[Any], merge_config: Optional[Any]) -> ObjectItem:
        ret = super().build(provider, resources, name, config, merge_config)
        ret['spec']['csi']['driver'] = 'dobs.csi.digitalocean.com'
        if config is not None:
            if 'nodriver' in config and config['nodriver'] is True:
                del ret['spec']['csi']['driver']

        if self.noformat is not None:
            if 'volumeAttributes' not in ret['spec']['csi']:
                ret['spec']['csi']['volumeAttributes'] = {}
            if 'com.digitalocean.csi/noformat' not in ret['spec']['csi']['volumeAttributes']:
                ret['spec']['csi']['volumeAttributes']['com.digitalocean.csi/noformat'] = QuotedStr(
                    'false' if self.noformat is False else 'true')

        if 'volumeHandle' in ret['spec']['csi'] and ret['spec']['csi']['volumeHandle'] is not None:
            # https://github.com/digitalocean/csi-digitalocean/blob/master/examples/kubernetes/pod-single-existing-volume/README.md
            Merger.merge(ret, {
                'metadata': {
                    'annotations': {
                        'pv.kubernetes.io/provisioned-by': 'dobs.csi.digitalocean.com',
                    }
                }
            })

        if 'storageClassName' not in ret['spec']:
            ret['spec']['storageClassName'] = 'do-block-storage'

        return ret
