from typing import Optional, Any

from kubragen.kresource import KRPersistentVolumeProfile, KResourceDatabase, KRPersistentVolumeProfile_CSI
from kubragen.merger import Merger
from kubragen.object import ObjectItem
from kubragen.provider import Provider


class KRPersistentVolumeProfile_AWSElasticBlockStore(KRPersistentVolumeProfile):
    """
    A PersisteVolume builder for AWS Elastic Block Store using the in-source Kubernetes driver.

    .. seealso:: `awsElasticBlockStore <https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore>`_.
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
                'awsElasticBlockStore': {},
            },
        }
        if self.storageclass is not None:
            pvdata['spec']['storageClassName'] = self.storageclass
        is_static = False
        if config is not None:
            if 'name' in config:
                pvdata['metadata']['name'] = config['name']
            if 'csi' in config:
                if 'volumeHandle' in config['csi']:
                    is_static = True
                    pvdata['spec']['awsElasticBlockStore']['volumeID'] = config['csi']['volumeHandle']
                if 'fsType' in config['csi']:
                    pvdata['spec']['awsElasticBlockStore']['fsType'] = config['csi']['fsType']
                if 'readOnly' in config['csi']:
                    pvdata['spec']['awsElasticBlockStore']['readOnly'] = config['csi']['readOnly']

        ret = Merger.merge(pvdata, merge_config if merge_config is not None else {})

        if is_static:
            # Static storage must set class name as ''
            ret['spec']['storageClassName'] = ''

        return ret


class KRPersistentVolumeProfile_CSI_AWSEBS(KRPersistentVolumeProfile_CSI):
    """
    A PersisteVolume builder for AWS Elastic Block Store using the CSI driver.

    .. seealso:: `Amazon EBS CSI driver <https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html>`_.
    """
    def build(self, provider: Provider, resources: KResourceDatabase, name: str,
              config: Optional[Any], merge_config: Optional[Any]) -> ObjectItem:
        ret = super().build(provider, resources, name, config, merge_config)
        ret['spec']['csi']['driver'] = 'ebs.csi.aws.com'
        if config is not None:
            if 'nodriver' in config and config['nodriver'] is True:
                del ret['spec']['csi']['driver']
        return ret


class KRPersistentVolumeProfile_CSI_AWSEFS(KRPersistentVolumeProfile_CSI):
    """
    A PersisteVolume builder for AWS Elastic File Store using the CSI driver.

    .. seealso:: `Amazon EFS CSI driver <https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html>`_.
    """
    def build(self, provider: Provider, resources: KResourceDatabase, name: str,
              config: Optional[Any], merge_config: Optional[Any]) -> ObjectItem:
        ret = super().build(provider, resources, name, config, merge_config)
        ret['spec']['csi']['driver'] = 'efs.csi.aws.com'
        if config is not None:
            if 'nodriver' in config and config['nodriver'] is True:
                del ret['spec']['csi']['driver']
        return ret
