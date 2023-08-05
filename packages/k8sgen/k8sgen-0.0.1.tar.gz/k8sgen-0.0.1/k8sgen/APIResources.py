from k8sgen import base
from k8sgen.base import K8sObject

'''
Kubernetes DaemonSet component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class DaemonSet(K8sObject):
    def __init__(self):
        super().__init__(name="DaemonSet", data_source='api_resources_data')

'''
Kubernetes ReplicationController component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ReplicationController(K8sObject):
    def __init__(self):
        super().__init__(name="ReplicationController", data_source='api_resources_data')

'''
Kubernetes TokenReview component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class TokenReview(K8sObject):
    def __init__(self):
        super().__init__(name="TokenReview", data_source='api_resources_data')

'''
Kubernetes StorageClass component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class StorageClass(K8sObject):
    def __init__(self):
        super().__init__(name="StorageClass", data_source='api_resources_data')

'''
Kubernetes CustomResourceDefinition component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class CustomResourceDefinition(K8sObject):
    def __init__(self):
        super().__init__(name="CustomResourceDefinition", data_source='api_resources_data')

'''
Kubernetes CSIDriver component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class CSIDriver(K8sObject):
    def __init__(self):
        super().__init__(name="CSIDriver", data_source='api_resources_data')

'''
Kubernetes Binding component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Binding(K8sObject):
    def __init__(self):
        super().__init__(name="Binding", data_source='api_resources_data')

'''
Kubernetes SelfSubjectRulesReview component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class SelfSubjectRulesReview(K8sObject):
    def __init__(self):
        super().__init__(name="SelfSubjectRulesReview", data_source='api_resources_data')

'''
Kubernetes Role component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Role(K8sObject):
    def __init__(self):
        super().__init__(name="Role", data_source='api_resources_data')

'''
Kubernetes Deployment component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Deployment(K8sObject):
    def __init__(self):
        super().__init__(name="Deployment", data_source='api_resources_data')

'''
Kubernetes ValidatingWebhookConfiguration component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ValidatingWebhookConfiguration(K8sObject):
    def __init__(self):
        super().__init__(name="ValidatingWebhookConfiguration", data_source='api_resources_data')

'''
Kubernetes PodSecurityPolicy component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodSecurityPolicy(K8sObject):
    def __init__(self):
        super().__init__(name="PodSecurityPolicy", data_source='api_resources_data')

'''
Kubernetes CronJob component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class CronJob(K8sObject):
    def __init__(self):
        super().__init__(name="CronJob", data_source='api_resources_data')

'''
Kubernetes RuntimeClass component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class RuntimeClass(K8sObject):
    def __init__(self):
        super().__init__(name="RuntimeClass", data_source='api_resources_data')

'''
Kubernetes ClusterRole component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ClusterRole(K8sObject):
    def __init__(self):
        super().__init__(name="ClusterRole", data_source='api_resources_data')

'''
Kubernetes Service component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Service(K8sObject):
    def __init__(self):
        super().__init__(name="Service", data_source='api_resources_data')

'''
Kubernetes IngressClass component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class IngressClass(K8sObject):
    def __init__(self):
        super().__init__(name="IngressClass", data_source='api_resources_data')

'''
Kubernetes Ingress component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Ingress(K8sObject):
    def __init__(self):
        super().__init__(name="Ingress", data_source='api_resources_data')

'''
Kubernetes PriorityClass component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PriorityClass(K8sObject):
    def __init__(self):
        super().__init__(name="PriorityClass", data_source='api_resources_data')

'''
Kubernetes PersistentVolume component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PersistentVolume(K8sObject):
    def __init__(self):
        super().__init__(name="PersistentVolume", data_source='api_resources_data')

'''
Kubernetes Event component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Event(K8sObject):
    def __init__(self):
        super().__init__(name="Event", data_source='api_resources_data')

'''
Kubernetes CSINode component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class CSINode(K8sObject):
    def __init__(self):
        super().__init__(name="CSINode", data_source='api_resources_data')

'''
Kubernetes ReplicaSet component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ReplicaSet(K8sObject):
    def __init__(self):
        super().__init__(name="ReplicaSet", data_source='api_resources_data')

'''
Kubernetes MutatingWebhookConfiguration component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class MutatingWebhookConfiguration(K8sObject):
    def __init__(self):
        super().__init__(name="MutatingWebhookConfiguration", data_source='api_resources_data')

'''
Kubernetes ServiceAccount component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ServiceAccount(K8sObject):
    def __init__(self):
        super().__init__(name="ServiceAccount", data_source='api_resources_data')

'''
Kubernetes CertificateSigningRequest component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class CertificateSigningRequest(K8sObject):
    def __init__(self):
        super().__init__(name="CertificateSigningRequest", data_source='api_resources_data')

'''
Kubernetes SubjectAccessReview component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class SubjectAccessReview(K8sObject):
    def __init__(self):
        super().__init__(name="SubjectAccessReview", data_source='api_resources_data')

'''
Kubernetes APIService component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class APIService(K8sObject):
    def __init__(self):
        super().__init__(name="APIService", data_source='api_resources_data')

'''
Kubernetes ConfigMap component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ConfigMap(K8sObject):
    def __init__(self):
        super().__init__(name="ConfigMap", data_source='api_resources_data')

'''
Kubernetes SelfSubjectAccessReview component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class SelfSubjectAccessReview(K8sObject):
    def __init__(self):
        super().__init__(name="SelfSubjectAccessReview", data_source='api_resources_data')

'''
Kubernetes Lease component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Lease(K8sObject):
    def __init__(self):
        super().__init__(name="Lease", data_source='api_resources_data')

'''
Kubernetes Job component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Job(K8sObject):
    def __init__(self):
        super().__init__(name="Job", data_source='api_resources_data')

'''
Kubernetes PodDisruptionBudget component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodDisruptionBudget(K8sObject):
    def __init__(self):
        super().__init__(name="PodDisruptionBudget", data_source='api_resources_data')

'''
Kubernetes Namespace component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Namespace(K8sObject):
    def __init__(self):
        super().__init__(name="Namespace", data_source='api_resources_data')

'''
Kubernetes HorizontalPodAutoscaler component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class HorizontalPodAutoscaler(K8sObject):
    def __init__(self):
        super().__init__(name="HorizontalPodAutoscaler", data_source='api_resources_data')

'''
Kubernetes Pod component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Pod(K8sObject):
    def __init__(self):
        super().__init__(name="Pod", data_source='api_resources_data')

'''
Kubernetes PodTemplate component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodTemplate(K8sObject):
    def __init__(self):
        super().__init__(name="PodTemplate", data_source='api_resources_data')

'''
Kubernetes Secret component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Secret(K8sObject):
    def __init__(self):
        super().__init__(name="Secret", data_source='api_resources_data')

'''
Kubernetes LimitRange component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class LimitRange(K8sObject):
    def __init__(self):
        super().__init__(name="LimitRange", data_source='api_resources_data')

'''
Kubernetes NetworkPolicy component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class NetworkPolicy(K8sObject):
    def __init__(self):
        super().__init__(name="NetworkPolicy", data_source='api_resources_data')

'''
Kubernetes ResourceQuota component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ResourceQuota(K8sObject):
    def __init__(self):
        super().__init__(name="ResourceQuota", data_source='api_resources_data')

'''
Kubernetes VolumeAttachment component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class VolumeAttachment(K8sObject):
    def __init__(self):
        super().__init__(name="VolumeAttachment", data_source='api_resources_data')

'''
Kubernetes PersistentVolumeClaim component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PersistentVolumeClaim(K8sObject):
    def __init__(self):
        super().__init__(name="PersistentVolumeClaim", data_source='api_resources_data')

'''
Kubernetes Node component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Node(K8sObject):
    def __init__(self):
        super().__init__(name="Node", data_source='api_resources_data')

'''
Kubernetes ComponentStatus component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ComponentStatus(K8sObject):
    def __init__(self):
        super().__init__(name="ComponentStatus", data_source='api_resources_data')

'''
Kubernetes StatefulSet component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class StatefulSet(K8sObject):
    def __init__(self):
        super().__init__(name="StatefulSet", data_source='api_resources_data')

'''
Kubernetes RoleBinding component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class RoleBinding(K8sObject):
    def __init__(self):
        super().__init__(name="RoleBinding", data_source='api_resources_data')

'''
Kubernetes ClusterRoleBinding component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ClusterRoleBinding(K8sObject):
    def __init__(self):
        super().__init__(name="ClusterRoleBinding", data_source='api_resources_data')

'''
Kubernetes Endpoints component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Endpoints(K8sObject):
    def __init__(self):
        super().__init__(name="Endpoints", data_source='api_resources_data')

'''
Kubernetes LocalSubjectAccessReview component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class LocalSubjectAccessReview(K8sObject):
    def __init__(self):
        super().__init__(name="LocalSubjectAccessReview", data_source='api_resources_data')

'''
Kubernetes EndpointSlice component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class EndpointSlice(K8sObject):
    def __init__(self):
        super().__init__(name="EndpointSlice", data_source='api_resources_data')

'''
Kubernetes ControllerRevision component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ControllerRevision(K8sObject):
    def __init__(self):
        super().__init__(name="ControllerRevision", data_source='api_resources_data')

