from typing import Optional, Any

from kubragen.kresource import KRPersistentVolumeProfile, KResourceDatabase, KRPersistentVolumeProfile_CSI
from kubragen.merger import Merger
from kubragen.object import ObjectItem
from kubragen.provider import Provider


class KRPersistentVolumeProfile_GCEPersistentDisk(KRPersistentVolumeProfile):
    """
    A PersisteVolume builder for Google Compute Engine Persistent Disk using the in-source Kubernetes driver.

    .. seealso:: `gcePersistentDisk <https://kubernetes.io/docs/concepts/storage/volumes/#gcepersistentdisk>`_.
    """
    def build(self, provider: Provider, resources: KResourceDatabase, name: str,
              config: Optional[Any], merge_config: Optional[Any]) -> ObjectItem:
        pvdata = {
            'apiVersion': 'v1',
            'kind': 'PersistentVolume',
            'metadata': {
                'name': name,
            },
            'spec': {
                'gcePersistentDisk': {},
            },
        }
        if config is not None:
            if 'name' in config:
                pvdata['metadata']['name'] = config['name']
            if 'csi' in config:
                if 'volumeHandle' in config['csi']:
                    pvdata['spec']['gcePersistentDisk']['pdName'] = config['csi']['volumeHandle']
                if 'fsType' in config['csi']:
                    pvdata['spec']['gcePersistentDisk']['fsType'] = config['csi']['fsType']
                if 'readOnly' in config['csi']:
                    pvdata['spec']['gcePersistentDisk']['readOnly'] = config['csi']['readOnly']

        return Merger.merge(pvdata, merge_config if merge_config is not None else {})


class KRPersistentVolumeProfile_CSI_GCEPD(KRPersistentVolumeProfile_CSI):
    """
    A PersisteVolume builder for Google Compute Engine Persistent Disk using the CSI driver.

    .. seealso:: `Using the Compute Engine persistent disk CSI Driver <https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/gce-pd-csi-driver>`_.
    """
    def build(self, provider: Provider, resources: KResourceDatabase, name: str,
              config: Optional[Any], merge_config: Optional[Any]) -> ObjectItem:
        ret = super().build(provider, resources, name, config, merge_config)
        ret['spec']['csi']['driver'] = 'pd.csi.storage.gke.io'
        if config is not None:
            if 'nodriver' in config and config['nodriver'] is True:
                del ret['spec']['csi']['driver']
        return ret
