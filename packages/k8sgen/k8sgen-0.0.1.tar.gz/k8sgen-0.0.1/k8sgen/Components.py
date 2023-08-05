from k8sgen import base
from k8sgen.base import K8sObject

'''
Kubernetes VolumeMount component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class VolumeMount(K8sObject):
    def __init__(self):
        super().__init__(name="VolumeMount", data_source='components_data')

'''
Kubernetes ManagedField component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ManagedField(K8sObject):
    def __init__(self):
        super().__init__(name="ManagedField", data_source='components_data')

'''
Kubernetes HostAlias component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class HostAlias(K8sObject):
    def __init__(self):
        super().__init__(name="HostAlias", data_source='components_data')

'''
Kubernetes NetworkPolicyIngress component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class NetworkPolicyIngress(K8sObject):
    def __init__(self):
        super().__init__(name="NetworkPolicyIngress", data_source='components_data')

'''
Kubernetes VolumeClaimTemplate component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class VolumeClaimTemplate(K8sObject):
    def __init__(self):
        super().__init__(name="VolumeClaimTemplate", data_source='components_data')

'''
Kubernetes DownwardAPIItem component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class DownwardAPIItem(K8sObject):
    def __init__(self):
        super().__init__(name="DownwardAPIItem", data_source='components_data')

'''
Kubernetes NodePreferredAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class NodePreferredAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="NodePreferredAffinity", data_source='components_data')

'''
Kubernetes Volume component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Volume(K8sObject):
    def __init__(self):
        super().__init__(name="Volume", data_source='components_data')

'''
Kubernetes IngressTLS component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class IngressTLS(K8sObject):
    def __init__(self):
        super().__init__(name="IngressTLS", data_source='components_data')

'''
Kubernetes IngressRulePath component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class IngressRulePath(K8sObject):
    def __init__(self):
        super().__init__(name="IngressRulePath", data_source='components_data')

'''
Kubernetes AllowedFlexVolume component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class AllowedFlexVolume(K8sObject):
    def __init__(self):
        super().__init__(name="AllowedFlexVolume", data_source='components_data')

'''
Kubernetes ComponentStatusCondition component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ComponentStatusCondition(K8sObject):
    def __init__(self):
        super().__init__(name="ComponentStatusCondition", data_source='components_data')

'''
Kubernetes NonResourceAttribute component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class NonResourceAttribute(K8sObject):
    def __init__(self):
        super().__init__(name="NonResourceAttribute", data_source='components_data')

'''
Kubernetes EnvironmentVariable component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class EnvironmentVariable(K8sObject):
    def __init__(self):
        super().__init__(name="EnvironmentVariable", data_source='components_data')

'''
Kubernetes Webhook component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Webhook(K8sObject):
    def __init__(self):
        super().__init__(name="Webhook", data_source='components_data')

'''
Kubernetes ProjectedVolumeSource component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ProjectedVolumeSource(K8sObject):
    def __init__(self):
        super().__init__(name="ProjectedVolumeSource", data_source='components_data')

'''
Kubernetes AllowedHostPath component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class AllowedHostPath(K8sObject):
    def __init__(self):
        super().__init__(name="AllowedHostPath", data_source='components_data')

'''
Kubernetes ImagePullSecret component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ImagePullSecret(K8sObject):
    def __init__(self):
        super().__init__(name="ImagePullSecret", data_source='components_data')

'''
Kubernetes SubsetPort component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class SubsetPort(K8sObject):
    def __init__(self):
        super().__init__(name="SubsetPort", data_source='components_data')

'''
Kubernetes RoleRule component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class RoleRule(K8sObject):
    def __init__(self):
        super().__init__(name="RoleRule", data_source='components_data')

'''
Kubernetes ServicePort component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ServicePort(K8sObject):
    def __init__(self):
        super().__init__(name="ServicePort", data_source='components_data')

'''
Kubernetes Selector component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Selector(K8sObject):
    def __init__(self):
        super().__init__(name="Selector", data_source='components_data')

'''
Kubernetes Range component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Range(K8sObject):
    def __init__(self):
        super().__init__(name="Range", data_source='components_data')

'''
Kubernetes AllowedCSIDriver component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class AllowedCSIDriver(K8sObject):
    def __init__(self):
        super().__init__(name="AllowedCSIDriver", data_source='components_data')

'''
Kubernetes PrinterColumn component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PrinterColumn(K8sObject):
    def __init__(self):
        super().__init__(name="PrinterColumn", data_source='components_data')

'''
Kubernetes ContainerPort component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ContainerPort(K8sObject):
    def __init__(self):
        super().__init__(name="ContainerPort", data_source='components_data')

'''
Kubernetes ConfigMapItem component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ConfigMapItem(K8sObject):
    def __init__(self):
        super().__init__(name="ConfigMapItem", data_source='components_data')

'''
Kubernetes NodeSelectorTerm component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class NodeSelectorTerm(K8sObject):
    def __init__(self):
        super().__init__(name="NodeSelectorTerm", data_source='components_data')

'''
Kubernetes DNSConfigOptions component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class DNSConfigOptions(K8sObject):
    def __init__(self):
        super().__init__(name="DNSConfigOptions", data_source='components_data')

'''
Kubernetes Metadata component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Metadata(K8sObject):
    def __init__(self):
        super().__init__(name="Metadata", data_source='components_data')

'''
Kubernetes ClusterRule component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ClusterRule(K8sObject):
    def __init__(self):
        super().__init__(name="ClusterRule", data_source='components_data')

'''
Kubernetes PodPreferredAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodPreferredAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="PodPreferredAffinity", data_source='components_data')

'''
Kubernetes ResourceDefinitionVersion component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ResourceDefinitionVersion(K8sObject):
    def __init__(self):
        super().__init__(name="ResourceDefinitionVersion", data_source='components_data')

'''
Kubernetes AllowedTopology component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class AllowedTopology(K8sObject):
    def __init__(self):
        super().__init__(name="AllowedTopology", data_source='components_data')

'''
Kubernetes SecurityContext component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class SecurityContext(K8sObject):
    def __init__(self):
        super().__init__(name="SecurityContext", data_source='components_data')

'''
Kubernetes LifecycleDefinition component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class LifecycleDefinition(K8sObject):
    def __init__(self):
        super().__init__(name="LifecycleDefinition", data_source='components_data')

'''
Kubernetes OwnerReference component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class OwnerReference(K8sObject):
    def __init__(self):
        super().__init__(name="OwnerReference", data_source='components_data')

'''
Kubernetes SecretItem component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class SecretItem(K8sObject):
    def __init__(self):
        super().__init__(name="SecretItem", data_source='components_data')

'''
Kubernetes PodAntiAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodAntiAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="PodAntiAffinity", data_source='components_data')

'''
Kubernetes Container component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Container(K8sObject):
    def __init__(self):
        super().__init__(name="Container", data_source='components_data')

'''
Kubernetes Address component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Address(K8sObject):
    def __init__(self):
        super().__init__(name="Address", data_source='components_data')

'''
Kubernetes IngressRule component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class IngressRule(K8sObject):
    def __init__(self):
        super().__init__(name="IngressRule", data_source='components_data')

'''
Kubernetes ScopeSelector component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ScopeSelector(K8sObject):
    def __init__(self):
        super().__init__(name="ScopeSelector", data_source='components_data')

'''
Kubernetes UserGroup component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class UserGroup(K8sObject):
    def __init__(self):
        super().__init__(name="UserGroup", data_source='components_data')

'''
Kubernetes PodRequiredAntiAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodRequiredAntiAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="PodRequiredAntiAffinity", data_source='components_data')

'''
Kubernetes EnvironmentVariableSource component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class EnvironmentVariableSource(K8sObject):
    def __init__(self):
        super().__init__(name="EnvironmentVariableSource", data_source='components_data')

'''
Kubernetes Limit component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Limit(K8sObject):
    def __init__(self):
        super().__init__(name="Limit", data_source='components_data')

'''
Kubernetes NodeAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class NodeAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="NodeAffinity", data_source='components_data')

'''
Kubernetes NetworkPolicyEgress component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class NetworkPolicyEgress(K8sObject):
    def __init__(self):
        super().__init__(name="NetworkPolicyEgress", data_source='components_data')

'''
Kubernetes Subset component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Subset(K8sObject):
    def __init__(self):
        super().__init__(name="Subset", data_source='components_data')

'''
Kubernetes DNSConfig component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class DNSConfig(K8sObject):
    def __init__(self):
        super().__init__(name="DNSConfig", data_source='components_data')

'''
Kubernetes PodAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="PodAffinity", data_source='components_data')

'''
Kubernetes MatchExpression component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class MatchExpression(K8sObject):
    def __init__(self):
        super().__init__(name="MatchExpression", data_source='components_data')

'''
Kubernetes Probe component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Probe(K8sObject):
    def __init__(self):
        super().__init__(name="Probe", data_source='components_data')

'''
Kubernetes ServiceAccountSecret component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ServiceAccountSecret(K8sObject):
    def __init__(self):
        super().__init__(name="ServiceAccountSecret", data_source='components_data')

'''
Kubernetes ReadinessGate component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ReadinessGate(K8sObject):
    def __init__(self):
        super().__init__(name="ReadinessGate", data_source='components_data')

'''
Kubernetes Toleration component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Toleration(K8sObject):
    def __init__(self):
        super().__init__(name="Toleration", data_source='components_data')

'''
Kubernetes NodeRequiredAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class NodeRequiredAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="NodeRequiredAffinity", data_source='components_data')

'''
Kubernetes MatchLabelExpression component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class MatchLabelExpression(K8sObject):
    def __init__(self):
        super().__init__(name="MatchLabelExpression", data_source='components_data')

'''
Kubernetes Sysctl component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Sysctl(K8sObject):
    def __init__(self):
        super().__init__(name="Sysctl", data_source='components_data')

'''
Kubernetes HTTPHeader component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class HTTPHeader(K8sObject):
    def __init__(self):
        super().__init__(name="HTTPHeader", data_source='components_data')

'''
Kubernetes ResourceAttribute component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ResourceAttribute(K8sObject):
    def __init__(self):
        super().__init__(name="ResourceAttribute", data_source='components_data')

'''
Kubernetes ClientConfig component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ClientConfig(K8sObject):
    def __init__(self):
        super().__init__(name="ClientConfig", data_source='components_data')

'''
Kubernetes VolumeDevice component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class VolumeDevice(K8sObject):
    def __init__(self):
        super().__init__(name="VolumeDevice", data_source='components_data')

'''
Kubernetes PodPreferredAntiAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodPreferredAntiAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="PodPreferredAntiAffinity", data_source='components_data')

'''
Kubernetes PodRequiredAffinity component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class PodRequiredAffinity(K8sObject):
    def __init__(self):
        super().__init__(name="PodRequiredAffinity", data_source='components_data')

'''
Kubernetes Taint component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class Taint(K8sObject):
    def __init__(self):
        super().__init__(name="Taint", data_source='components_data')

'''
Kubernetes ContainerSpec component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ContainerSpec(K8sObject):
    def __init__(self):
        super().__init__(name="ContainerSpec", data_source='components_data')

'''
Kubernetes ClusterRoleBindingSubject component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class ClusterRoleBindingSubject(K8sObject):
    def __init__(self):
        super().__init__(name="ClusterRoleBindingSubject", data_source='components_data')

'''
Kubernetes CSINodeDriver component for use in API resources

Available manifest keys are:
    (( MANIFEST_KEYS ))
'''
class CSINodeDriver(K8sObject):
    def __init__(self):
        super().__init__(name="CSINodeDriver", data_source='components_data')

