k8sgen_data = {
    "api_resources_data": {
        "DaemonSet": {
            "description": "DaemonSet represents the configuration of a daemon set.",
            "json": {
                "apiVersion": "apps/v1",
                "kind": "DaemonSet",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "minReadySeconds": "<integer>",
                    "revisionHistoryLimit": "<integer>",
                    "selector": "<COMPONENT.Selector>",
                    "template": {
                        "metadata": "<COMPONENT.Metadata>",
                        "spec": "<COMPONENT.ContainerSpec>"
                    },
                    "updateStrategy": {
                        "rollingUpdate": {
                            "maxUnavailable": "<string>"
                        },
                        "type": "<string>"
                    }
                }
            }
        },
        "ReplicationController": {
            "description": "ReplicationController represents the configuration of a replication controller.",
            "json": {
                "apiVersion": "v1",
                "kind": "ReplicationController",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "minReadySeconds": "<integer>",
                    "replicas": "<integer>",
                    "selector": "<map[string]string>",
                    "template": {
                        "metadata": "<COMPONENT.Metadata>",
                        "spec": {
                            "activeDeadlineSeconds": "<integer>",
                            "affinity": {
                                "nodeAffinity": "<COMPONENT.NodeAffinity>",
                                "podAffinity": "<COMPONENT.PodAffinity>",
                                "podAntiAffinity": "<COMPONENT.PodAntiAffinity>"
                            },
                            "automountServiceAccountToken": "<boolean>",
                            "containers": "<[]COMPONENT.Container>",
                            "dnsConfig": "<COMPONENT.DNSConfig>",
                            "dnsPolicy": "<string>",
                            "enableServiceLinks": "<boolean>",
                            "ephemeralContainers": [
                                {
                                    "args": "<[]string>",
                                    "command": "<[]string>",
                                    "env": [
                                        {
                                            "name": "<string>",
                                            "value": "<string>",
                                            "valueFrom": {
                                                "configMapKeyRef": {
                                                    "key": "<string>",
                                                    "name": "<string>",
                                                    "optional": "<boolean>"
                                                },
                                                "fieldRef": {
                                                    "apiVersion": "<string>",
                                                    "fieldPath": "<string>"
                                                },
                                                "resourceFieldRef": {
                                                    "containerName": "<string>",
                                                    "divisor": "<string>",
                                                    "resource": "<string>"
                                                },
                                                "secretKeyRef": {
                                                    "key": "<string>",
                                                    "name": "<string>",
                                                    "optional": "<boolean>"
                                                }
                                            }
                                        }
                                    ],
                                    "envFrom": [
                                        {
                                            "configMapRef": {
                                                "name": "<string>",
                                                "optional": "<boolean>"
                                            },
                                            "prefix": "<string>",
                                            "secretRef": {
                                                "name": "<string>",
                                                "optional": "<boolean>"
                                            }
                                        }
                                    ],
                                    "image": "<string>",
                                    "imagePullPolicy": "<string>",
                                    "lifecycle": {
                                        "postStart": {
                                            "exec": {
                                                "command": "<[]string>"
                                            },
                                            "httpGet": {
                                                "host": "<string>",
                                                "httpHeaders": [
                                                    {
                                                        "name": "<string>",
                                                        "value": "<string>"
                                                    }
                                                ],
                                                "path": "<string>",
                                                "port": "<string>",
                                                "scheme": "<string>"
                                            },
                                            "tcpSocket": {
                                                "host": "<string>",
                                                "port": "<string>"
                                            }
                                        },
                                        "preStop": {
                                            "exec": {
                                                "command": "<[]string>"
                                            },
                                            "httpGet": {
                                                "host": "<string>",
                                                "httpHeaders": [
                                                    {
                                                        "name": "<string>",
                                                        "value": "<string>"
                                                    }
                                                ],
                                                "path": "<string>",
                                                "port": "<string>",
                                                "scheme": "<string>"
                                            },
                                            "tcpSocket": {
                                                "host": "<string>",
                                                "port": "<string>"
                                            }
                                        }
                                    },
                                    "livenessProbe": {
                                        "exec": {
                                            "command": "<[]string>"
                                        },
                                        "failureThreshold": "<integer>",
                                        "httpGet": {
                                            "host": "<string>",
                                            "httpHeaders": [
                                                {
                                                    "name": "<string>",
                                                    "value": "<string>"
                                                }
                                            ],
                                            "path": "<string>",
                                            "port": "<string>",
                                            "scheme": "<string>"
                                        },
                                        "initialDelaySeconds": "<integer>",
                                        "periodSeconds": "<integer>",
                                        "successThreshold": "<integer>",
                                        "tcpSocket": {
                                            "host": "<string>",
                                            "port": "<string>"
                                        },
                                        "timeoutSeconds": "<integer>"
                                    },
                                    "name": "<string>",
                                    "ports": [
                                        {
                                            "containerPort": "<integer>",
                                            "hostIP": "<string>",
                                            "hostPort": "<integer>",
                                            "name": "<string>",
                                            "protocol": "<string>"
                                        }
                                    ],
                                    "readinessProbe": {
                                        "exec": {
                                            "command": "<[]string>"
                                        },
                                        "failureThreshold": "<integer>",
                                        "httpGet": {
                                            "host": "<string>",
                                            "httpHeaders": [
                                                {
                                                    "name": "<string>",
                                                    "value": "<string>"
                                                }
                                            ],
                                            "path": "<string>",
                                            "port": "<string>",
                                            "scheme": "<string>"
                                        },
                                        "initialDelaySeconds": "<integer>",
                                        "periodSeconds": "<integer>",
                                        "successThreshold": "<integer>",
                                        "tcpSocket": {
                                            "host": "<string>",
                                            "port": "<string>"
                                        },
                                        "timeoutSeconds": "<integer>"
                                    },
                                    "resources": {
                                        "limits": "<map[string]string>",
                                        "requests": "<map[string]string>"
                                    },
                                    "securityContext": {
                                        "allowPrivilegeEscalation": "<boolean>",
                                        "capabilities": {
                                            "add": "<[]string>",
                                            "drop": "<[]string>"
                                        },
                                        "privileged": "<boolean>",
                                        "procMount": "<string>",
                                        "readOnlyRootFilesystem": "<boolean>",
                                        "runAsGroup": "<integer>",
                                        "runAsNonRoot": "<boolean>",
                                        "runAsUser": "<integer>",
                                        "seLinuxOptions": {
                                            "level": "<string>",
                                            "role": "<string>",
                                            "type": "<string>",
                                            "user": "<string>"
                                        },
                                        "windowsOptions": {
                                            "gmsaCredentialSpec": "<string>",
                                            "gmsaCredentialSpecName": "<string>",
                                            "runAsUserName": "<string>"
                                        }
                                    },
                                    "startupProbe": {
                                        "exec": {
                                            "command": "<[]string>"
                                        },
                                        "failureThreshold": "<integer>",
                                        "httpGet": {
                                            "host": "<string>",
                                            "httpHeaders": [
                                                {
                                                    "name": "<string>",
                                                    "value": "<string>"
                                                }
                                            ],
                                            "path": "<string>",
                                            "port": "<string>",
                                            "scheme": "<string>"
                                        },
                                        "initialDelaySeconds": "<integer>",
                                        "periodSeconds": "<integer>",
                                        "successThreshold": "<integer>",
                                        "tcpSocket": {
                                            "host": "<string>",
                                            "port": "<string>"
                                        },
                                        "timeoutSeconds": "<integer>"
                                    },
                                    "stdin": "<boolean>",
                                    "stdinOnce": "<boolean>",
                                    "targetContainerName": "<string>",
                                    "terminationMessagePath": "<string>",
                                    "terminationMessagePolicy": "<string>",
                                    "tty": "<boolean>",
                                    "volumeDevices": [
                                        {
                                            "devicePath": "<string>",
                                            "name": "<string>"
                                        }
                                    ],
                                    "volumeMounts": [
                                        {
                                            "mountPath": "<string>",
                                            "mountPropagation": "<string>",
                                            "name": "<string>",
                                            "readOnly": "<boolean>",
                                            "subPath": "<string>",
                                            "subPathExpr": "<string>"
                                        }
                                    ],
                                    "workingDir": "<string>"
                                }
                            ],
                            "hostAliases": "<[]COMPONENT.HostAlias>",
                            "hostIPC": "<boolean>",
                            "hostNetwork": "<boolean>",
                            "hostPID": "<boolean>",
                            "hostname": "<string>",
                            "imagePullSecrets": "<[]COMPONENT.ImagePullSecret>",
                            "initContainers": "<[]COMPONENT.Container>",
                            "nodeName": "<string>",
                            "nodeSelector": "<map[string]string>",
                            "overhead": "<map[string]string>",
                            "preemptionPolicy": "<string>",
                            "priority": "<integer>",
                            "priorityClassName": "<string>",
                            "readinessGates": "<[]COMPONENT.ReadinessGate>",
                            "restartPolicy": "<string>",
                            "runtimeClassName": "<string>",
                            "schedulerName": "<string>",
                            "securityContext": "<COMPONENT.SecurityContext>",
                            "serviceAccount": "<string>",
                            "serviceAccountName": "<string>",
                            "shareProcessNamespace": "<boolean>",
                            "subdomain": "<string>",
                            "terminationGracePeriodSeconds": "<integer>",
                            "tolerations": "<[]COMPONENT.Tolerations>",
                            "topologySpreadConstraints": [
                                {
                                    "labelSelector": {
                                        "matchExpressions": [
                                            {
                                                "key": "<string>",
                                                "operator": "<string>",
                                                "values": "<[]string>"
                                            }
                                        ],
                                        "matchLabels": "<map[string]string>"
                                    },
                                    "maxSkew": "<integer>",
                                    "topologyKey": "<string>",
                                    "whenUnsatisfiable": "<string>"
                                }
                            ],
                            "volumes": "<[]COMPONENT.Volume>"
                        }
                    }
                }
            }
        },
        "TokenReview": {
            "description": "TokenReview attempts to authenticate a token to a known user. Note: TokenReview requests may be cached by the webhook token authenticator plugin in the kube-apiserver.",
            "json": {
                "apiVersion": "authentication.k8s.io/v1",
                "kind": "TokenReview",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "audiences": "<[]string>",
                    "token": "<string>"
                }
            }
        },
        "StorageClass": {
            "description": "StorageClass describes the parameters for a class of storage for which PersistentVolumes can be dynamically provisioned. StorageClasses are non-namespaced; the name of the storage class according to etcd is in ObjectMeta.Name.",
            "json": {
                "allowVolumeExpansion": "<boolean>",
                "allowedTopologies": "<[]COMPONENT.AllowedTopology>",
                "apiVersion": "storage.k8s.io/v1",
                "kind": "StorageClass",
                "metadata": "<COMPONENT.Metadata>",
                "mountOptions": "<[]string>",
                "parameters": "<map[string]string>",
                "provisioner": "<string>",
                "reclaimPolicy": "<string>",
                "volumeBindingMode": "<string>"
            }
        },
        "CustomResourceDefinition": {
            "description": "CustomResourceDefinition represents a resource that should be exposed on the API server. Its name MUST be in the format <.spec.name>.<.spec.group>.",
            "json": {
                "apiVersion": "apiextensions.k8s.io/v1",
                "kind": "CustomResourceDefinition",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "conversion": {
                        "strategy": "<string>",
                        "webhook": {
                            "clientConfig": {
                                "caBundle": "<string>",
                                "service": {
                                    "name": "<string>",
                                    "namespace": "<string>",
                                    "path": "<string>",
                                    "port": "<integer>"
                                },
                                "url": "<string>"
                            },
                            "conversionReviewVersions": "<[]string>"
                        }
                    },
                    "group": "<string>",
                    "names": {
                        "categories": "<[]string>",
                        "kind": "<string>",
                        "listKind": "<string>",
                        "plural": "<string>",
                        "shortNames": "<[]string>",
                        "singular": "<string>"
                    },
                    "preserveUnknownFields": "<boolean>",
                    "scope": "<string>",
                    "versions": "<[]COMPONENT.ResourceDefinitionVersion>"
                }
            }
        },
        "CSIDriver": {
            "description": "CSIDriver captures information about a Container Storage Interface (CSI) volume driver deployed on the cluster. Kubernetes attach detach controller uses this object to determine whether attach is required. Kubelet uses this object to determine whether pod information needs to be passed on mount. CSIDriver objects are non-namespaced.",
            "json": {
                "apiVersion": "storage.k8s.io/v1",
                "kind": "CSIDriver",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "attachRequired": "<boolean>",
                    "podInfoOnMount": "<boolean>",
                    "volumeLifecycleModes": "<[]string>"
                }
            }
        },
        "Binding": {
            "description": "Binding ties one object to another; for example, a pod is bound to a node by a scheduler. Deprecated in 1.7, please use the bindings subresource of pods instead.",
            "json": {
                "apiVersion": "v1",
                "kind": "Binding",
                "metadata": "<COMPONENT.Metadata>",
                "target": {
                    "apiVersion": "<string>",
                    "fieldPath": "<string>",
                    "kind": "<string>",
                    "name": "<string>",
                    "namespace": "<string>",
                    "resourceVersion": "<string>",
                    "uid": "<string>"
                }
            }
        },
        "SelfSubjectRulesReview": {
            "description": "SelfSubjectRulesReview enumerates the set of actions the current user can perform within a namespace. The returned list of actions may be incomplete depending on the server's authorization mode, and any errors experienced during the evaluation. SelfSubjectRulesReview should be used by UIs to show/hide actions, or to quickly let an end user reason about their permissions. It should NOT Be used by external systems to drive authorization decisions as this raises confused deputy, cache lifetime/revocation, and correctness concerns. SubjectAccessReview, and LocalAccessReview are the correct way to defer authorization decisions to the API server.",
            "json": {
                "apiVersion": "authorization.k8s.io/v1",
                "kind": "SelfSubjectRulesReview",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "namespace": "<string>"
                }
            }
        },
        "Role": {
            "description": "Role is a namespaced, logical grouping of PolicyRules that can be referenced as a unit by a RoleBinding.",
            "json": {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "Role",
                "metadata": "<COMPONENT.Metadata>",
                "rules": "<[]COMPONENT.RoleRule"
            }
        },
        "Deployment": {
            "description": "Deployment enables declarative updates for Pods and ReplicaSets.",
            "json": {
                "apiVersion": "apps/v1",
                "kind": "Deployment",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "minReadySeconds": "<integer>",
                    "paused": "<boolean>",
                    "progressDeadlineSeconds": "<integer>",
                    "replicas": "<integer>",
                    "revisionHistoryLimit": "<integer>",
                    "selector": "<COMPONENT.Selector>",
                    "strategy": {
                        "rollingUpdate": {
                            "maxSurge": "<string>",
                            "maxUnavailable": "<string>"
                        },
                        "type": "<string>"
                    },
                    "template": {
                        "metadata": "<COMPONENT.Metadata>",
                        "spec": "<COMPONENT.ContainerSpec>"
                    }
                }
            }
        },
        "ValidatingWebhookConfiguration": {
            "description": "ValidatingWebhookConfiguration describes the configuration of and admission webhook that accept or reject and object without changing it.",
            "json": {
                "apiVersion": "admissionregistration.k8s.io/v1",
                "kind": "ValidatingWebhookConfiguration",
                "metadata": "<COMPONENT.Metadata>",
                "webhooks": "<[]COMPONENT.Webhook>"
            }
        },
        "PodSecurityPolicy": {
            "description": "PodSecurityPolicy governs the ability to make requests that affect the Security Context that will be applied to a pod and container.",
            "json": {
                "apiVersion": "policy/v1beta1",
                "kind": "PodSecurityPolicy",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "allowPrivilegeEscalation": "<boolean>",
                    "allowedCSIDrivers": "<[]COMPONENT.AllowedCSIDriver>",
                    "allowedCapabilities": "<[]string>",
                    "allowedFlexVolumes": "<[]COMPONENT.AllowedFlexVolume>",
                    "allowedHostPaths": "<[]COMPONENT.AllowedHostPath>",
                    "allowedProcMountTypes": "<[]string>",
                    "allowedUnsafeSysctls": "<[]string>",
                    "defaultAddCapabilities": "<[]string>",
                    "defaultAllowPrivilegeEscalation": "<boolean>",
                    "forbiddenSysctls": "<[]string>",
                    "fsGroup": "<COMPONENT.UserGroup>",
                    "hostIPC": "<boolean>",
                    "hostNetwork": "<boolean>",
                    "hostPID": "<boolean>",
                    "hostPorts": "<[]COMPONENT.Range>",
                    "privileged": "<boolean>",
                    "readOnlyRootFilesystem": "<boolean>",
                    "requiredDropCapabilities": "<[]string>",
                    "runAsGroup": "<COMPONENT.UserGroup>",
                    "runAsUser": "<COMPONENT.UserGroup>",
                    "runtimeClass": {
                        "allowedRuntimeClassNames": "<[]string>",
                        "defaultRuntimeClassName": "<string>"
                    },
                    "seLinux": {
                        "rule": "<string>",
                        "seLinuxOptions": {
                            "level": "<string>",
                            "role": "<string>",
                            "type": "<string>",
                            "user": "<string>"
                        }
                    },
                    "supplementalGroups": "<COMPONENT.UserGroup>",
                    "volumes": "<[]COMPONENT.Volume>"
                }
            }
        },
        "CronJob": {
            "description": "CronJob represents the configuration of a single cron job.",
            "json": {
                "apiVersion": "batch/v1beta1",
                "kind": "CronJob",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "concurrencyPolicy": "<string>",
                    "failedJobsHistoryLimit": "<integer>",
                    "jobTemplate": {
                        "metadata": "<COMPONENT.Metadata>",
                        "spec": {
                            "activeDeadlineSeconds": "<integer>",
                            "backoffLimit": "<integer>",
                            "completions": "<integer>",
                            "manualSelector": "<boolean>",
                            "parallelism": "<integer>",
                            "selector": "<COMPONENT.Selector>",
                            "template": {
                                "metadata": "<COMPONENT.Metadata>",
                                "spec": "<COMPONENT.ContainerSpec>"
                            },
                            "ttlSecondsAfterFinished": "<integer>"
                        }
                    },
                    "schedule": "<string>",
                    "startingDeadlineSeconds": "<integer>",
                    "successfulJobsHistoryLimit": "<integer>",
                    "suspend": "<boolean>"
                }
            }
        },
        "RuntimeClass": {
            "description": "RuntimeClass defines a class of container runtime supported in the cluster. The RuntimeClass is used to determine which container runtime is used to run all containers in a pod. RuntimeClasses are (currently) manually defined by a user or cluster provisioner, and referenced in the PodSpec. The Kubelet is responsible for resolving the RuntimeClassName reference before running the pod. For more details, see https://git.k8s.io/enhancements/keps/sig-node/runtime-class.md",
            "json": {
                "apiVersion": "node.k8s.io/v1beta1",
                "handler": "<string>",
                "kind": "RuntimeClass",
                "metadata": "<COMPONENT.Metadata>",
                "overhead": {
                    "podFixed": "<map[string]string>"
                },
                "scheduling": {
                    "nodeSelector": "<map[string]string>",
                    "tolerations": [
                        {
                            "effect": "<string>",
                            "key": "<string>",
                            "operator": "<string>",
                            "tolerationSeconds": "<integer>",
                            "value": "<string>"
                        }
                    ]
                }
            }
        },
        "ClusterRole": {
            "description": "ClusterRole is a cluster level, logical grouping of PolicyRules that can be referenced as a unit by a RoleBinding or ClusterRoleBinding.",
            "json": {
                "aggregationRule": {
                    "clusterRoleSelectors": "<[]COMPONENT.ClusterRoleSelector>"
                },
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "ClusterRole",
                "metadata": "<COMPONENT.Metadata>",
                "rules": "<[]COMPONENT.ClusterRule>"
            }
        },
        "Service": {
            "description": "Service is a named abstraction of software service (for example, mysql) consisting of local port (for example 3306) that the proxy listens on, and the selector that determines which pods will answer requests sent through the proxy.",
            "json": {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "clusterIP": "<string>",
                    "externalIPs": "<[]string>",
                    "externalName": "<string>",
                    "externalTrafficPolicy": "<string>",
                    "healthCheckNodePort": "<integer>",
                    "ipFamily": "<string>",
                    "loadBalancerIP": "<string>",
                    "loadBalancerSourceRanges": "<[]string>",
                    "ports": "<[]COMPONENT.ServicePort>",
                    "publishNotReadyAddresses": "<boolean>",
                    "selector": "<map[string]string>",
                    "sessionAffinity": "<string>",
                    "sessionAffinityConfig": {
                        "clientIP": {
                            "timeoutSeconds": "<integer>"
                        }
                    },
                    "topologyKeys": "<[]string>",
                    "type": "<string>"
                }
            }
        },
        "IngressClass": {
            "description": "IngressClass represents the class of the Ingress, referenced by the Ingress Spec. The `ingressclass.kubernetes.io/is-default-class` annotation can be used to indicate that an IngressClass should be considered default. When a single IngressClass resource has this annotation set to true, new Ingress resources without a class specified will be assigned this default class.",
            "json": {
                "apiVersion": "networking.k8s.io/v1beta1",
                "kind": "IngressClass",
                "metadata": {
                    "annotations": "<map[string]string>",
                    "clusterName": "<string>",
                    "creationTimestamp": "<string>",
                    "deletionGracePeriodSeconds": "<integer>",
                    "deletionTimestamp": "<string>",
                    "finalizers": "<[]string>",
                    "generateName": "<string>",
                    "generation": "<integer>",
                    "labels": "<map[string]string>",
                    "managedFields": [
                        {
                            "apiVersion": "<string>",
                            "fieldsType": "<string>",
                            "fieldsV1": "<map[string]>",
                            "manager": "<string>",
                            "operation": "<string>",
                            "time": "<string>"
                        }
                    ],
                    "name": "<string>",
                    "namespace": "<string>",
                    "ownerReferences": [
                        {
                            "apiVersion": "<string>",
                            "blockOwnerDeletion": "<boolean>",
                            "controller": "<boolean>",
                            "kind": "<string>",
                            "name": "<string>",
                            "uid": "<string>"
                        }
                    ],
                    "resourceVersion": "<string>",
                    "selfLink": "<string>",
                    "uid": "<string>"
                },
                "spec": {
                    "controller": "<string>",
                    "parameters": {
                        "apiGroup": "<string>",
                        "kind": "<string>",
                        "name": "<string>"
                    }
                }
            }
        },
        "Ingress": {
            "description": "Ingress is a collection of rules that allow inbound connections to reach the endpoints defined by a backend. An Ingress can be configured to give services externally-reachable urls, load balance traffic, terminate SSL, offer name based virtual hosting etc. DEPRECATED - This group version of Ingress is deprecated by networking.k8s.io/v1beta1 Ingress. See the release notes for more information.",
            "json": {
                "apiVersion": "extensions/v1beta1",
                "kind": "Ingress",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "backend": {
                        "resource": {
                            "apiGroup": "<string>",
                            "kind": "<string>",
                            "name": "<string>"
                        },
                        "serviceName": "<string>",
                        "servicePort": "<string>"
                    },
                    "ingressClassName": "<string>",
                    "rules": "<[]COMPONENT.IngressRule>",
                    "tls": "<[]COMPONENT.IngressTLS>"
                }
            }
        },
        "PriorityClass": {
            "description": "PriorityClass defines mapping from a priority class name to the priority integer value. The value can be any valid integer.",
            "json": {
                "apiVersion": "scheduling.k8s.io/v1",
                "description": "<string>",
                "globalDefault": "<boolean>",
                "kind": "PriorityClass",
                "metadata": "<COMPONENT.Metadata>",
                "preemptionPolicy": "<string>",
                "value": "<integer>"
            }
        },
        "PersistentVolume": {
            "description": "PersistentVolume (PV) is a storage resource provisioned by an administrator. It is analogous to a node. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes",
            "json": {
                "apiVersion": "v1",
                "kind": "PersistentVolume",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "accessModes": "<[]string>",
                    "awsElasticBlockStore": {
                        "fsType": "<string>",
                        "partition": "<integer>",
                        "readOnly": "<boolean>",
                        "volumeID": "<string>"
                    },
                    "azureDisk": {
                        "cachingMode": "<string>",
                        "diskName": "<string>",
                        "diskURI": "<string>",
                        "fsType": "<string>",
                        "kind": "<string>",
                        "readOnly": "<boolean>"
                    },
                    "azureFile": {
                        "readOnly": "<boolean>",
                        "secretName": "<string>",
                        "secretNamespace": "<string>",
                        "shareName": "<string>"
                    },
                    "capacity": "<map[string]string>",
                    "cephfs": {
                        "monitors": "<[]string>",
                        "path": "<string>",
                        "readOnly": "<boolean>",
                        "secretFile": "<string>",
                        "secretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "user": "<string>"
                    },
                    "cinder": {
                        "fsType": "<string>",
                        "readOnly": "<boolean>",
                        "secretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "volumeID": "<string>"
                    },
                    "claimRef": {
                        "apiVersion": "<string>",
                        "fieldPath": "<string>",
                        "kind": "<string>",
                        "name": "<string>",
                        "namespace": "<string>",
                        "resourceVersion": "<string>",
                        "uid": "<string>"
                    },
                    "csi": {
                        "controllerExpandSecretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "controllerPublishSecretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "driver": "<string>",
                        "fsType": "<string>",
                        "nodePublishSecretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "nodeStageSecretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "readOnly": "<boolean>",
                        "volumeAttributes": "<map[string]string>",
                        "volumeHandle": "<string>"
                    },
                    "fc": {
                        "fsType": "<string>",
                        "lun": "<integer>",
                        "readOnly": "<boolean>",
                        "targetWWNs": "<[]string>",
                        "wwids": "<[]string>"
                    },
                    "flexVolume": {
                        "driver": "<string>",
                        "fsType": "<string>",
                        "options": "<map[string]string>",
                        "readOnly": "<boolean>",
                        "secretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        }
                    },
                    "flocker": {
                        "datasetName": "<string>",
                        "datasetUUID": "<string>"
                    },
                    "gcePersistentDisk": {
                        "fsType": "<string>",
                        "partition": "<integer>",
                        "pdName": "<string>",
                        "readOnly": "<boolean>"
                    },
                    "glusterfs": {
                        "endpoints": "<string>",
                        "endpointsNamespace": "<string>",
                        "path": "<string>",
                        "readOnly": "<boolean>"
                    },
                    "hostPath": {
                        "path": "<string>",
                        "type": "<string>"
                    },
                    "iscsi": {
                        "chapAuthDiscovery": "<boolean>",
                        "chapAuthSession": "<boolean>",
                        "fsType": "<string>",
                        "initiatorName": "<string>",
                        "iqn": "<string>",
                        "iscsiInterface": "<string>",
                        "lun": "<integer>",
                        "portals": "<[]string>",
                        "readOnly": "<boolean>",
                        "secretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "targetPortal": "<string>"
                    },
                    "local": {
                        "fsType": "<string>",
                        "path": "<string>"
                    },
                    "mountOptions": "<[]string>",
                    "nfs": {
                        "path": "<string>",
                        "readOnly": "<boolean>",
                        "server": "<string>"
                    },
                    "nodeAffinity": {
                        "required": {
                            "nodeSelectorTerms": "<[]COMPONENT.NodeSelectorTerm>"
                        }
                    },
                    "persistentVolumeReclaimPolicy": "<string>",
                    "photonPersistentDisk": {
                        "fsType": "<string>",
                        "pdID": "<string>"
                    },
                    "portworxVolume": {
                        "fsType": "<string>",
                        "readOnly": "<boolean>",
                        "volumeID": "<string>"
                    },
                    "quobyte": {
                        "group": "<string>",
                        "readOnly": "<boolean>",
                        "registry": "<string>",
                        "tenant": "<string>",
                        "user": "<string>",
                        "volume": "<string>"
                    },
                    "rbd": {
                        "fsType": "<string>",
                        "image": "<string>",
                        "keyring": "<string>",
                        "monitors": "<[]string>",
                        "pool": "<string>",
                        "readOnly": "<boolean>",
                        "secretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "user": "<string>"
                    },
                    "scaleIO": {
                        "fsType": "<string>",
                        "gateway": "<string>",
                        "protectionDomain": "<string>",
                        "readOnly": "<boolean>",
                        "secretRef": {
                            "name": "<string>",
                            "namespace": "<string>"
                        },
                        "sslEnabled": "<boolean>",
                        "storageMode": "<string>",
                        "storagePool": "<string>",
                        "system": "<string>",
                        "volumeName": "<string>"
                    },
                    "storageClassName": "<string>",
                    "storageos": {
                        "fsType": "<string>",
                        "readOnly": "<boolean>",
                        "secretRef": {
                            "apiVersion": "<string>",
                            "fieldPath": "<string>",
                            "kind": "<string>",
                            "name": "<string>",
                            "namespace": "<string>",
                            "resourceVersion": "<string>",
                            "uid": "<string>"
                        },
                        "volumeName": "<string>",
                        "volumeNamespace": "<string>"
                    },
                    "volumeMode": "<string>",
                    "vsphereVolume": {
                        "fsType": "<string>",
                        "storagePolicyID": "<string>",
                        "storagePolicyName": "<string>",
                        "volumePath": "<string>"
                    }
                }
            }
        },
        "Event": {
            "description": "Event is a report of an event somewhere in the cluster.",
            "json": {
                "action": "<string>",
                "apiVersion": "v1",
                "count": "<integer>",
                "eventTime": "<string>",
                "firstTimestamp": "<string>",
                "involvedObject": {
                    "apiVersion": "<string>",
                    "fieldPath": "<string>",
                    "kind": "<string>",
                    "name": "<string>",
                    "namespace": "<string>",
                    "resourceVersion": "<string>",
                    "uid": "<string>"
                },
                "kind": "Event",
                "lastTimestamp": "<string>",
                "message": "<string>",
                "metadata": "<COMPONENT.Metadata>",
                "reason": "<string>",
                "related": {
                    "apiVersion": "<string>",
                    "fieldPath": "<string>",
                    "kind": "<string>",
                    "name": "<string>",
                    "namespace": "<string>",
                    "resourceVersion": "<string>",
                    "uid": "<string>"
                },
                "reportingComponent": "<string>",
                "reportingInstance": "<string>",
                "series": {
                    "count": "<integer>",
                    "lastObservedTime": "<string>",
                    "state": "<string>"
                },
                "source": {
                    "component": "<string>",
                    "host": "<string>"
                },
                "type": "<string>"
            }
        },
        "CSINode": {
            "description": "CSINode holds information about all CSI drivers installed on a node. CSI drivers do not need to create the CSINode object directly. As long as they use the node-driver-registrar sidecar container, the kubelet will automatically populate the CSINode object for the CSI driver as part of kubelet plugin registration. CSINode has the same name as a node. If the object is missing, it means either there are no CSI Drivers available on the node, or the Kubelet version is low enough that it doesn't create this object. CSINode has an OwnerReference that points to the corresponding node object.",
            "json": {
                "apiVersion": "storage.k8s.io/v1",
                "kind": "CSINode",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "drivers": "<[]COMPONENT.CSINodeDriver>"
                }
            }
        },
        "ReplicaSet": {
            "description": "ReplicaSet ensures that a specified number of pod replicas are running at any given time.",
            "json": {
                "apiVersion": "apps/v1",
                "kind": "ReplicaSet",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "minReadySeconds": "<integer>",
                    "replicas": "<integer>",
                    "selector": "<COMPONENT.Selector>",
                    "template": {
                        "metadata": "<COMPONENT.Metadata>",
                        "spec": "<COMPONENT.ContainerSpec>"
                    }
                }
            }
        },
        "MutatingWebhookConfiguration": {
            "description": "MutatingWebhookConfiguration describes the configuration of and admission webhook that accept or reject and may change the object.",
            "json": {
                "apiVersion": "admissionregistration.k8s.io/v1",
                "kind": "MutatingWebhookConfiguration",
                "metadata": "<COMPONENT.Metadata>",
                "webhooks": "<[]COMPONENT.Webhook>"
            }
        },
        "ServiceAccount": {
            "description": "ServiceAccount binds together: * a name, understood by users, and perhaps by peripheral systems, for an identity * a principal that can be authenticated and authorized * a set of secrets",
            "json": {
                "apiVersion": "v1",
                "automountServiceAccountToken": "<boolean>",
                "imagePullSecrets": "<[]COMPONENT.ImagePullSecret>",
                "kind": "ServiceAccount",
                "metadata": "<COMPONENT.Metadata>",
                "secrets": "<[]COMPONENT.ServiceAccountSecret>"
            }
        },
        "CertificateSigningRequest": {
            "description": "Describes a certificate signing request",
            "json": {
                "apiVersion": "certificates.k8s.io/v1beta1",
                "kind": "CertificateSigningRequest",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "extra": "<map[string][]string>",
                    "groups": "<[]string>",
                    "request": "<string>",
                    "signerName": "<string>",
                    "uid": "<string>",
                    "usages": "<[]string>",
                    "username": "<string>"
                }
            }
        },
        "SubjectAccessReview": {
            "description": "SubjectAccessReview checks whether or not a user or group can perform an action.",
            "json": {
                "apiVersion": "authorization.k8s.io/v1",
                "kind": "SubjectAccessReview",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "extra": "<map[string][]string>",
                    "groups": "<[]string>",
                    "nonResourceAttributes": "<[]COMPONENT.NonResourceAttribute>",
                    "resourceAttributes": "<COMPONENT.ResourceAttribute>",
                    "uid": "<string>",
                    "user": "<string>"
                }
            }
        },
        "APIService": {
            "description": "APIService represents a server for a particular GroupVersion. Name must be \"version.group\".",
            "json": {
                "apiVersion": "apiregistration.k8s.io/v1",
                "kind": "APIService",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "caBundle": "<string>",
                    "group": "<string>",
                    "groupPriorityMinimum": "<integer>",
                    "insecureSkipTLSVerify": "<boolean>",
                    "service": {
                        "name": "<string>",
                        "namespace": "<string>",
                        "port": "<integer>"
                    },
                    "version": "<string>",
                    "versionPriority": "<integer>"
                }
            }
        },
        "ConfigMap": {
            "description": "ConfigMap holds configuration data for pods to consume.",
            "json": {
                "apiVersion": "v1",
                "binaryData": "<map[string]string>",
                "data": "<map[string]string>",
                "immutable": "<boolean>",
                "kind": "ConfigMap",
                "metadata": "<COMPONENT.Metadata>"
            }
        },
        "SelfSubjectAccessReview": {
            "description": "SelfSubjectAccessReview checks whether or the current user can perform an action. Not filling in a spec.namespace means \"in all namespaces\". Self is a special case, because users should always be able to check whether they can perform an action",
            "json": {
                "apiVersion": "authorization.k8s.io/v1",
                "kind": "SelfSubjectAccessReview",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "nonResourceAttributes": "<[]COMPONENT.NonResourceAttribute>",
                    "resourceAttributes": "<COMPONENT.ResourceAttribute>"
                }
            }
        },
        "Lease": {
            "description": "Lease defines a lease concept.",
            "json": {
                "apiVersion": "coordination.k8s.io/v1",
                "kind": "Lease",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "acquireTime": "<string>",
                    "holderIdentity": "<string>",
                    "leaseDurationSeconds": "<integer>",
                    "leaseTransitions": "<integer>",
                    "renewTime": "<string>"
                }
            }
        },
        "Job": {
            "description": "Job represents the configuration of a single job.",
            "json": {
                "apiVersion": "batch/v1",
                "kind": "Job",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "activeDeadlineSeconds": "<integer>",
                    "backoffLimit": "<integer>",
                    "completions": "<integer>",
                    "manualSelector": "<boolean>",
                    "parallelism": "<integer>",
                    "selector": "<COMPONENT.Selector>",
                    "template": {
                        "metadata": "<COMPONENT.Metadata>",
                        "spec": "<COMPONENT.ContainerSpec>"
                    },
                    "ttlSecondsAfterFinished": "<integer>"
                }
            }
        },
        "PodDisruptionBudget": {
            "description": "PodDisruptionBudget is an object to define the max disruption that can be caused to a collection of pods",
            "json": {
                "apiVersion": "policy/v1beta1",
                "kind": "PodDisruptionBudget",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "maxUnavailable": "<string>",
                    "minAvailable": "<string>",
                    "selector": "<COMPONENT.Selector>"
                }
            }
        },
        "Namespace": {
            "description": "Namespace provides a scope for Names. Use of multiple namespaces is optional.",
            "json": {
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "finalizers": "<[]string>"
                }
            }
        },
        "HorizontalPodAutoscaler": {
            "description": "configuration of a horizontal pod autoscaler.",
            "json": {
                "apiVersion": "autoscaling/v1",
                "kind": "HorizontalPodAutoscaler",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "maxReplicas": "<integer>",
                    "minReplicas": "<integer>",
                    "scaleTargetRef": {
                        "apiVersion": "<string>",
                        "kind": "<string>",
                        "name": "<string>"
                    },
                    "targetCPUUtilizationPercentage": "<integer>"
                }
            }
        },
        "Pod": {
            "description": "Pod is a collection of containers that can run on a host. This resource is created by clients and scheduled onto hosts.",
            "json": {
                "apiVersion": "v1",
                "kind": "Pod",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "activeDeadlineSeconds": "<integer>",
                    "affinity": {
                        "nodeAffinity": "<COMPONENT.NodeAffinity>",
                        "podAffinity": "<COMPONENT.PodAffinity>",
                        "podAntiAffinity": "<COMPONENT.PodAntiAffinity>"
                    },
                    "automountServiceAccountToken": "<boolean>",
                    "containers": "<[]COMPONENT.Container>",
                    "dnsConfig": "<COMPONENT.DNSConfig>",
                    "dnsPolicy": "<string>",
                    "enableServiceLinks": "<boolean>",
                    "ephemeralContainers": [
                        {
                            "args": "<[]string>",
                            "command": "<[]string>",
                            "env": [
                                {
                                    "name": "<string>",
                                    "value": "<string>",
                                    "valueFrom": {
                                        "configMapKeyRef": {
                                            "key": "<string>",
                                            "name": "<string>",
                                            "optional": "<boolean>"
                                        },
                                        "fieldRef": {
                                            "apiVersion": "<string>",
                                            "fieldPath": "<string>"
                                        },
                                        "resourceFieldRef": {
                                            "containerName": "<string>",
                                            "divisor": "<string>",
                                            "resource": "<string>"
                                        },
                                        "secretKeyRef": {
                                            "key": "<string>",
                                            "name": "<string>",
                                            "optional": "<boolean>"
                                        }
                                    }
                                }
                            ],
                            "envFrom": [
                                {
                                    "configMapRef": {
                                        "name": "<string>",
                                        "optional": "<boolean>"
                                    },
                                    "prefix": "<string>",
                                    "secretRef": {
                                        "name": "<string>",
                                        "optional": "<boolean>"
                                    }
                                }
                            ],
                            "image": "<string>",
                            "imagePullPolicy": "<string>",
                            "lifecycle": {
                                "postStart": {
                                    "exec": {
                                        "command": "<[]string>"
                                    },
                                    "httpGet": {
                                        "host": "<string>",
                                        "httpHeaders": [
                                            {
                                                "name": "<string>",
                                                "value": "<string>"
                                            }
                                        ],
                                        "path": "<string>",
                                        "port": "<string>",
                                        "scheme": "<string>"
                                    },
                                    "tcpSocket": {
                                        "host": "<string>",
                                        "port": "<string>"
                                    }
                                },
                                "preStop": {
                                    "exec": {
                                        "command": "<[]string>"
                                    },
                                    "httpGet": {
                                        "host": "<string>",
                                        "httpHeaders": [
                                            {
                                                "name": "<string>",
                                                "value": "<string>"
                                            }
                                        ],
                                        "path": "<string>",
                                        "port": "<string>",
                                        "scheme": "<string>"
                                    },
                                    "tcpSocket": {
                                        "host": "<string>",
                                        "port": "<string>"
                                    }
                                }
                            },
                            "livenessProbe": {
                                "exec": {
                                    "command": "<[]string>"
                                },
                                "failureThreshold": "<integer>",
                                "httpGet": {
                                    "host": "<string>",
                                    "httpHeaders": [
                                        {
                                            "name": "<string>",
                                            "value": "<string>"
                                        }
                                    ],
                                    "path": "<string>",
                                    "port": "<string>",
                                    "scheme": "<string>"
                                },
                                "initialDelaySeconds": "<integer>",
                                "periodSeconds": "<integer>",
                                "successThreshold": "<integer>",
                                "tcpSocket": {
                                    "host": "<string>",
                                    "port": "<string>"
                                },
                                "timeoutSeconds": "<integer>"
                            },
                            "name": "<string>",
                            "ports": [
                                {
                                    "containerPort": "<integer>",
                                    "hostIP": "<string>",
                                    "hostPort": "<integer>",
                                    "name": "<string>",
                                    "protocol": "<string>"
                                }
                            ],
                            "readinessProbe": {
                                "exec": {
                                    "command": "<[]string>"
                                },
                                "failureThreshold": "<integer>",
                                "httpGet": {
                                    "host": "<string>",
                                    "httpHeaders": [
                                        {
                                            "name": "<string>",
                                            "value": "<string>"
                                        }
                                    ],
                                    "path": "<string>",
                                    "port": "<string>",
                                    "scheme": "<string>"
                                },
                                "initialDelaySeconds": "<integer>",
                                "periodSeconds": "<integer>",
                                "successThreshold": "<integer>",
                                "tcpSocket": {
                                    "host": "<string>",
                                    "port": "<string>"
                                },
                                "timeoutSeconds": "<integer>"
                            },
                            "resources": {
                                "limits": "<map[string]string>",
                                "requests": "<map[string]string>"
                            },
                            "securityContext": {
                                "allowPrivilegeEscalation": "<boolean>",
                                "capabilities": {
                                    "add": "<[]string>",
                                    "drop": "<[]string>"
                                },
                                "privileged": "<boolean>",
                                "procMount": "<string>",
                                "readOnlyRootFilesystem": "<boolean>",
                                "runAsGroup": "<integer>",
                                "runAsNonRoot": "<boolean>",
                                "runAsUser": "<integer>",
                                "seLinuxOptions": {
                                    "level": "<string>",
                                    "role": "<string>",
                                    "type": "<string>",
                                    "user": "<string>"
                                },
                                "windowsOptions": {
                                    "gmsaCredentialSpec": "<string>",
                                    "gmsaCredentialSpecName": "<string>",
                                    "runAsUserName": "<string>"
                                }
                            },
                            "startupProbe": {
                                "exec": {
                                    "command": "<[]string>"
                                },
                                "failureThreshold": "<integer>",
                                "httpGet": {
                                    "host": "<string>",
                                    "httpHeaders": [
                                        {
                                            "name": "<string>",
                                            "value": "<string>"
                                        }
                                    ],
                                    "path": "<string>",
                                    "port": "<string>",
                                    "scheme": "<string>"
                                },
                                "initialDelaySeconds": "<integer>",
                                "periodSeconds": "<integer>",
                                "successThreshold": "<integer>",
                                "tcpSocket": {
                                    "host": "<string>",
                                    "port": "<string>"
                                },
                                "timeoutSeconds": "<integer>"
                            },
                            "stdin": "<boolean>",
                            "stdinOnce": "<boolean>",
                            "targetContainerName": "<string>",
                            "terminationMessagePath": "<string>",
                            "terminationMessagePolicy": "<string>",
                            "tty": "<boolean>",
                            "volumeDevices": [
                                {
                                    "devicePath": "<string>",
                                    "name": "<string>"
                                }
                            ],
                            "volumeMounts": [
                                {
                                    "mountPath": "<string>",
                                    "mountPropagation": "<string>",
                                    "name": "<string>",
                                    "readOnly": "<boolean>",
                                    "subPath": "<string>",
                                    "subPathExpr": "<string>"
                                }
                            ],
                            "workingDir": "<string>"
                        }
                    ],
                    "hostAliases": "<[]COMPONENT.HostAlias>",
                    "hostIPC": "<boolean>",
                    "hostNetwork": "<boolean>",
                    "hostPID": "<boolean>",
                    "hostname": "<string>",
                    "imagePullSecrets": "<[]COMPONENT.ImagePullSecret>",
                    "initContainers": "<[]COMPONENT.Container>",
                    "nodeName": "<string>",
                    "nodeSelector": "<map[string]string>",
                    "overhead": "<map[string]string>",
                    "preemptionPolicy": "<string>",
                    "priority": "<integer>",
                    "priorityClassName": "<string>",
                    "readinessGates": "<[]COMPONENT.ReadinessGate>",
                    "restartPolicy": "<string>",
                    "runtimeClassName": "<string>",
                    "schedulerName": "<string>",
                    "securityContext": "<COMPONENT.SecurityContext>",
                    "serviceAccount": "<string>",
                    "serviceAccountName": "<string>",
                    "shareProcessNamespace": "<boolean>",
                    "subdomain": "<string>",
                    "terminationGracePeriodSeconds": "<integer>",
                    "tolerations": "<[]COMPONENT.Tolerations>",
                    "topologySpreadConstraints": [
                        {
                            "labelSelector": {
                                "matchExpressions": [
                                    {
                                        "key": "<string>",
                                        "operator": "<string>",
                                        "values": "<[]string>"
                                    }
                                ],
                                "matchLabels": "<map[string]string>"
                            },
                            "maxSkew": "<integer>",
                            "topologyKey": "<string>",
                            "whenUnsatisfiable": "<string>"
                        }
                    ],
                    "volumes": "<[]COMPONENT.Volume>"
                }
            }
        },
        "PodTemplate": {
            "description": "PodTemplate describes a template for creating copies of a predefined pod.",
            "json": {
                "apiVersion": "v1",
                "kind": "PodTemplate",
                "metadata": "<COMPONENT.Metadata>",
                "template": {
                    "metadata": "<COMPONENT.Metadata>",
                    "spec": {
                        "activeDeadlineSeconds": "<integer>",
                        "affinity": {
                            "nodeAffinity": "<COMPONENT.NodeAffinity>",
                            "podAffinity": "<COMPONENT.PodAffinity>",
                            "podAntiAffinity": "<COMPONENT.PodAntiAffinity>"
                        },
                        "automountServiceAccountToken": "<boolean>",
                        "containers": "<[]COMPONENT.Container>",
                        "dnsConfig": "<COMPONENT.DNSConfig>",
                        "dnsPolicy": "<string>",
                        "enableServiceLinks": "<boolean>",
                        "ephemeralContainers": [
                            {
                                "args": "<[]string>",
                                "command": "<[]string>",
                                "env": [
                                    {
                                        "name": "<string>",
                                        "value": "<string>",
                                        "valueFrom": {
                                            "configMapKeyRef": {
                                                "key": "<string>",
                                                "name": "<string>",
                                                "optional": "<boolean>"
                                            },
                                            "fieldRef": {
                                                "apiVersion": "<string>",
                                                "fieldPath": "<string>"
                                            },
                                            "resourceFieldRef": {
                                                "containerName": "<string>",
                                                "divisor": "<string>",
                                                "resource": "<string>"
                                            },
                                            "secretKeyRef": {
                                                "key": "<string>",
                                                "name": "<string>",
                                                "optional": "<boolean>"
                                            }
                                        }
                                    }
                                ],
                                "envFrom": [
                                    {
                                        "configMapRef": {
                                            "name": "<string>",
                                            "optional": "<boolean>"
                                        },
                                        "prefix": "<string>",
                                        "secretRef": {
                                            "name": "<string>",
                                            "optional": "<boolean>"
                                        }
                                    }
                                ],
                                "image": "<string>",
                                "imagePullPolicy": "<string>",
                                "lifecycle": {
                                    "postStart": {
                                        "exec": {
                                            "command": "<[]string>"
                                        },
                                        "httpGet": {
                                            "host": "<string>",
                                            "httpHeaders": [
                                                {
                                                    "name": "<string>",
                                                    "value": "<string>"
                                                }
                                            ],
                                            "path": "<string>",
                                            "port": "<string>",
                                            "scheme": "<string>"
                                        },
                                        "tcpSocket": {
                                            "host": "<string>",
                                            "port": "<string>"
                                        }
                                    },
                                    "preStop": {
                                        "exec": {
                                            "command": "<[]string>"
                                        },
                                        "httpGet": {
                                            "host": "<string>",
                                            "httpHeaders": [
                                                {
                                                    "name": "<string>",
                                                    "value": "<string>"
                                                }
                                            ],
                                            "path": "<string>",
                                            "port": "<string>",
                                            "scheme": "<string>"
                                        },
                                        "tcpSocket": {
                                            "host": "<string>",
                                            "port": "<string>"
                                        }
                                    }
                                },
                                "livenessProbe": {
                                    "exec": {
                                        "command": "<[]string>"
                                    },
                                    "failureThreshold": "<integer>",
                                    "httpGet": {
                                        "host": "<string>",
                                        "httpHeaders": [
                                            {
                                                "name": "<string>",
                                                "value": "<string>"
                                            }
                                        ],
                                        "path": "<string>",
                                        "port": "<string>",
                                        "scheme": "<string>"
                                    },
                                    "initialDelaySeconds": "<integer>",
                                    "periodSeconds": "<integer>",
                                    "successThreshold": "<integer>",
                                    "tcpSocket": {
                                        "host": "<string>",
                                        "port": "<string>"
                                    },
                                    "timeoutSeconds": "<integer>"
                                },
                                "name": "<string>",
                                "ports": [
                                    {
                                        "containerPort": "<integer>",
                                        "hostIP": "<string>",
                                        "hostPort": "<integer>",
                                        "name": "<string>",
                                        "protocol": "<string>"
                                    }
                                ],
                                "readinessProbe": {
                                    "exec": {
                                        "command": "<[]string>"
                                    },
                                    "failureThreshold": "<integer>",
                                    "httpGet": {
                                        "host": "<string>",
                                        "httpHeaders": [
                                            {
                                                "name": "<string>",
                                                "value": "<string>"
                                            }
                                        ],
                                        "path": "<string>",
                                        "port": "<string>",
                                        "scheme": "<string>"
                                    },
                                    "initialDelaySeconds": "<integer>",
                                    "periodSeconds": "<integer>",
                                    "successThreshold": "<integer>",
                                    "tcpSocket": {
                                        "host": "<string>",
                                        "port": "<string>"
                                    },
                                    "timeoutSeconds": "<integer>"
                                },
                                "resources": {
                                    "limits": "<map[string]string>",
                                    "requests": "<map[string]string>"
                                },
                                "securityContext": {
                                    "allowPrivilegeEscalation": "<boolean>",
                                    "capabilities": {
                                        "add": "<[]string>",
                                        "drop": "<[]string>"
                                    },
                                    "privileged": "<boolean>",
                                    "procMount": "<string>",
                                    "readOnlyRootFilesystem": "<boolean>",
                                    "runAsGroup": "<integer>",
                                    "runAsNonRoot": "<boolean>",
                                    "runAsUser": "<integer>",
                                    "seLinuxOptions": {
                                        "level": "<string>",
                                        "role": "<string>",
                                        "type": "<string>",
                                        "user": "<string>"
                                    },
                                    "windowsOptions": {
                                        "gmsaCredentialSpec": "<string>",
                                        "gmsaCredentialSpecName": "<string>",
                                        "runAsUserName": "<string>"
                                    }
                                },
                                "startupProbe": {
                                    "exec": {
                                        "command": "<[]string>"
                                    },
                                    "failureThreshold": "<integer>",
                                    "httpGet": {
                                        "host": "<string>",
                                        "httpHeaders": [
                                            {
                                                "name": "<string>",
                                                "value": "<string>"
                                            }
                                        ],
                                        "path": "<string>",
                                        "port": "<string>",
                                        "scheme": "<string>"
                                    },
                                    "initialDelaySeconds": "<integer>",
                                    "periodSeconds": "<integer>",
                                    "successThreshold": "<integer>",
                                    "tcpSocket": {
                                        "host": "<string>",
                                        "port": "<string>"
                                    },
                                    "timeoutSeconds": "<integer>"
                                },
                                "stdin": "<boolean>",
                                "stdinOnce": "<boolean>",
                                "targetContainerName": "<string>",
                                "terminationMessagePath": "<string>",
                                "terminationMessagePolicy": "<string>",
                                "tty": "<boolean>",
                                "volumeDevices": [
                                    {
                                        "devicePath": "<string>",
                                        "name": "<string>"
                                    }
                                ],
                                "volumeMounts": [
                                    {
                                        "mountPath": "<string>",
                                        "mountPropagation": "<string>",
                                        "name": "<string>",
                                        "readOnly": "<boolean>",
                                        "subPath": "<string>",
                                        "subPathExpr": "<string>"
                                    }
                                ],
                                "workingDir": "<string>"
                            }
                        ],
                        "hostAliases": "<[]COMPONENT.HostAlias>",
                        "hostIPC": "<boolean>",
                        "hostNetwork": "<boolean>",
                        "hostPID": "<boolean>",
                        "hostname": "<string>",
                        "imagePullSecrets": "<[]COMPONENT.ImagePullSecret>",
                        "initContainers": "<[]COMPONENT.Container>",
                        "nodeName": "<string>",
                        "nodeSelector": "<map[string]string>",
                        "overhead": "<map[string]string>",
                        "preemptionPolicy": "<string>",
                        "priority": "<integer>",
                        "priorityClassName": "<string>",
                        "readinessGates": "<[]COMPONENT.ReadinessGate>",
                        "restartPolicy": "<string>",
                        "runtimeClassName": "<string>",
                        "schedulerName": "<string>",
                        "securityContext": "<COMPONENT.SecurityContext>",
                        "serviceAccount": "<string>",
                        "serviceAccountName": "<string>",
                        "shareProcessNamespace": "<boolean>",
                        "subdomain": "<string>",
                        "terminationGracePeriodSeconds": "<integer>",
                        "tolerations": "<[]COMPONENT.Tolerations>",
                        "topologySpreadConstraints": [
                            {
                                "labelSelector": {
                                    "matchExpressions": [
                                        {
                                            "key": "<string>",
                                            "operator": "<string>",
                                            "values": "<[]string>"
                                        }
                                    ],
                                    "matchLabels": "<map[string]string>"
                                },
                                "maxSkew": "<integer>",
                                "topologyKey": "<string>",
                                "whenUnsatisfiable": "<string>"
                            }
                        ],
                        "volumes": "<[]COMPONENT.Volume>"
                    }
                }
            }
        },
        "Secret": {
            "description": "Secret holds secret data of a certain type. The total bytes of the values in the Data field must be less than MaxSecretSize bytes.",
            "json": {
                "apiVersion": "v1",
                "data": "<map[string]string>",
                "immutable": "<boolean>",
                "kind": "Secret",
                "metadata": "<COMPONENT.Metadata>",
                "stringData": "<map[string]string>",
                "type": "<string>"
            }
        },
        "LimitRange": {
            "description": "LimitRange sets resource usage limits for each kind of resource in a Namespace.",
            "json": {
                "apiVersion": "v1",
                "kind": "LimitRange",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "limits": "<[]COMPONENT.Limit>"
                }
            }
        },
        "NetworkPolicy": {
            "description": "NetworkPolicy describes what network traffic is allowed for a set of Pods",
            "json": {
                "apiVersion": "networking.k8s.io/v1",
                "kind": "NetworkPolicy",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "egress": "<[]COMPONENT.NetworkPolicyEgress>",
                    "ingress": "<[]COMPONENT.NetworkPolicyIngress>",
                    "podSelector": "<COMPONENT.Selector>",
                    "policyTypes": "<[]string>"
                }
            }
        },
        "ResourceQuota": {
            "description": "ResourceQuota sets aggregate quota restrictions enforced per namespace",
            "json": {
                "apiVersion": "v1",
                "kind": "ResourceQuota",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "hard": "<map[string]string>",
                    "scopeSelector": {
                        "matchExpressions": "<[]COMPONENT.ScopeSelector>"
                    },
                    "scopes": "<[]string>"
                }
            }
        },
        "VolumeAttachment": {
            "description": "VolumeAttachment captures the intent to attach or detach the specified volume to/from the specified node. VolumeAttachment objects are non-namespaced.",
            "json": {
                "apiVersion": "storage.k8s.io/v1",
                "kind": "VolumeAttachment",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "attacher": "<string>",
                    "nodeName": "<string>",
                    "source": {
                        "inlineVolumeSpec": {
                            "accessModes": "<[]string>",
                            "awsElasticBlockStore": {
                                "fsType": "<string>",
                                "partition": "<integer>",
                                "readOnly": "<boolean>",
                                "volumeID": "<string>"
                            },
                            "azureDisk": {
                                "cachingMode": "<string>",
                                "diskName": "<string>",
                                "diskURI": "<string>",
                                "fsType": "<string>",
                                "kind": "<string>",
                                "readOnly": "<boolean>"
                            },
                            "azureFile": {
                                "readOnly": "<boolean>",
                                "secretName": "<string>",
                                "secretNamespace": "<string>",
                                "shareName": "<string>"
                            },
                            "capacity": "<map[string]string>",
                            "cephfs": {
                                "monitors": "<[]string>",
                                "path": "<string>",
                                "readOnly": "<boolean>",
                                "secretFile": "<string>",
                                "secretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "user": "<string>"
                            },
                            "cinder": {
                                "fsType": "<string>",
                                "readOnly": "<boolean>",
                                "secretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "volumeID": "<string>"
                            },
                            "claimRef": {
                                "apiVersion": "<string>",
                                "fieldPath": "<string>",
                                "kind": "<string>",
                                "name": "<string>",
                                "namespace": "<string>",
                                "resourceVersion": "<string>",
                                "uid": "<string>"
                            },
                            "csi": {
                                "controllerExpandSecretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "controllerPublishSecretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "driver": "<string>",
                                "fsType": "<string>",
                                "nodePublishSecretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "nodeStageSecretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "readOnly": "<boolean>",
                                "volumeAttributes": "<map[string]string>",
                                "volumeHandle": "<string>"
                            },
                            "fc": {
                                "fsType": "<string>",
                                "lun": "<integer>",
                                "readOnly": "<boolean>",
                                "targetWWNs": "<[]string>",
                                "wwids": "<[]string>"
                            },
                            "flexVolume": {
                                "driver": "<string>",
                                "fsType": "<string>",
                                "options": "<map[string]string>",
                                "readOnly": "<boolean>",
                                "secretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                }
                            },
                            "flocker": {
                                "datasetName": "<string>",
                                "datasetUUID": "<string>"
                            },
                            "gcePersistentDisk": {
                                "fsType": "<string>",
                                "partition": "<integer>",
                                "pdName": "<string>",
                                "readOnly": "<boolean>"
                            },
                            "glusterfs": {
                                "endpoints": "<string>",
                                "endpointsNamespace": "<string>",
                                "path": "<string>",
                                "readOnly": "<boolean>"
                            },
                            "hostPath": {
                                "path": "<string>",
                                "type": "<string>"
                            },
                            "iscsi": {
                                "chapAuthDiscovery": "<boolean>",
                                "chapAuthSession": "<boolean>",
                                "fsType": "<string>",
                                "initiatorName": "<string>",
                                "iqn": "<string>",
                                "iscsiInterface": "<string>",
                                "lun": "<integer>",
                                "portals": "<[]string>",
                                "readOnly": "<boolean>",
                                "secretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "targetPortal": "<string>"
                            },
                            "local": {
                                "fsType": "<string>",
                                "path": "<string>"
                            },
                            "mountOptions": "<[]string>",
                            "nfs": {
                                "path": "<string>",
                                "readOnly": "<boolean>",
                                "server": "<string>"
                            },
                            "nodeAffinity": {
                                "required": {
                                    "nodeSelectorTerms": "<[]COMPONENT.NodeSelectorTerm>"
                                }
                            },
                            "persistentVolumeReclaimPolicy": "<string>",
                            "photonPersistentDisk": {
                                "fsType": "<string>",
                                "pdID": "<string>"
                            },
                            "portworxVolume": {
                                "fsType": "<string>",
                                "readOnly": "<boolean>",
                                "volumeID": "<string>"
                            },
                            "quobyte": {
                                "group": "<string>",
                                "readOnly": "<boolean>",
                                "registry": "<string>",
                                "tenant": "<string>",
                                "user": "<string>",
                                "volume": "<string>"
                            },
                            "rbd": {
                                "fsType": "<string>",
                                "image": "<string>",
                                "keyring": "<string>",
                                "monitors": "<[]string>",
                                "pool": "<string>",
                                "readOnly": "<boolean>",
                                "secretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "user": "<string>"
                            },
                            "scaleIO": {
                                "fsType": "<string>",
                                "gateway": "<string>",
                                "protectionDomain": "<string>",
                                "readOnly": "<boolean>",
                                "secretRef": {
                                    "name": "<string>",
                                    "namespace": "<string>"
                                },
                                "sslEnabled": "<boolean>",
                                "storageMode": "<string>",
                                "storagePool": "<string>",
                                "system": "<string>",
                                "volumeName": "<string>"
                            },
                            "storageClassName": "<string>",
                            "storageos": {
                                "fsType": "<string>",
                                "readOnly": "<boolean>",
                                "secretRef": {
                                    "apiVersion": "<string>",
                                    "fieldPath": "<string>",
                                    "kind": "<string>",
                                    "name": "<string>",
                                    "namespace": "<string>",
                                    "resourceVersion": "<string>",
                                    "uid": "<string>"
                                },
                                "volumeName": "<string>",
                                "volumeNamespace": "<string>"
                            },
                            "volumeMode": "<string>",
                            "vsphereVolume": {
                                "fsType": "<string>",
                                "storagePolicyID": "<string>",
                                "storagePolicyName": "<string>",
                                "volumePath": "<string>"
                            }
                        },
                        "persistentVolumeName": "<string>"
                    }
                }
            }
        },
        "PersistentVolumeClaim": {
            "description": "PersistentVolumeClaim is a user's request for and claim to a persistent volume",
            "json": {
                "apiVersion": "v1",
                "kind": "PersistentVolumeClaim",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "accessModes": "<[]string>",
                    "dataSource": {
                        "apiGroup": "<string>",
                        "kind": "<string>",
                        "name": "<string>"
                    },
                    "resources": {
                        "limits": "<map[string]string>",
                        "requests": "<map[string]string>"
                    },
                    "selector": "<COMPONENT.Selector>",
                    "storageClassName": "<string>",
                    "volumeMode": "<string>",
                    "volumeName": "<string>"
                }
            }
        },
        "Node": {
            "description": "Node is a worker node in Kubernetes. Each node will have a unique identifier in the cache (i.e. in etcd).",
            "json": {
                "apiVersion": "v1",
                "kind": "Node",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "configSource": {
                        "configMap": {
                            "kubeletConfigKey": "<string>",
                            "name": "<string>",
                            "namespace": "<string>",
                            "resourceVersion": "<string>",
                            "uid": "<string>"
                        }
                    },
                    "externalID": "<string>",
                    "podCIDR": "<string>",
                    "podCIDRs": "<[]string>",
                    "providerID": "<string>",
                    "taints": "<[]COMPONENT.Taint>",
                    "unschedulable": "<boolean>"
                }
            }
        },
        "ComponentStatus": {
            "description": "ComponentStatus (and ComponentStatusList) holds the cluster validation info.",
            "json": {
                "apiVersion": "v1",
                "conditions": "<[]COMPONENT.ComponentStatusCondition>",
                "kind": "ComponentStatus",
                "metadata": "<COMPONENT.Metadata>"
            }
        },
        "StatefulSet": {
            "description": "StatefulSet represents a set of pods with consistent identities. Identities are defined as: - Network: A single stable DNS and hostname. - Storage: As many VolumeClaims as requested. The StatefulSet guarantees that a given network identity will always map to the same storage identity.",
            "json": {
                "apiVersion": "apps/v1",
                "kind": "StatefulSet",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "podManagementPolicy": "<string>",
                    "replicas": "<integer>",
                    "revisionHistoryLimit": "<integer>",
                    "selector": "<COMPONENT.Selector>",
                    "serviceName": "<string>",
                    "template": {
                        "metadata": "<COMPONENT.Metadata>",
                        "spec": {
                            "activeDeadlineSeconds": "<integer>",
                            "affinity": {
                                "nodeAffinity": "<COMPONENT.NodeAffinity>",
                                "podAffinity": "<COMPONENT.PodAffinity>",
                                "podAntiAffinity": "<COMPONENT.PodAntiAffinity>"
                            },
                            "automountServiceAccountToken": "<boolean>",
                            "containers": "<[]COMPONENT.Container>",
                            "dnsConfig": "<COMPONENT.DNSConfig>",
                            "dnsPolicy": "<string>",
                            "enableServiceLinks": "<boolean>",
                            "ephemeralContainers": [
                                {
                                    "args": "<[]string>",
                                    "command": "<[]string>",
                                    "env": [
                                        {
                                            "name": "<string>",
                                            "value": "<string>",
                                            "valueFrom": {
                                                "configMapKeyRef": {
                                                    "key": "<string>",
                                                    "name": "<string>",
                                                    "optional": "<boolean>"
                                                },
                                                "fieldRef": {
                                                    "apiVersion": "<string>",
                                                    "fieldPath": "<string>"
                                                },
                                                "resourceFieldRef": {
                                                    "containerName": "<string>",
                                                    "divisor": "<string>",
                                                    "resource": "<string>"
                                                },
                                                "secretKeyRef": {
                                                    "key": "<string>",
                                                    "name": "<string>",
                                                    "optional": "<boolean>"
                                                }
                                            }
                                        }
                                    ],
                                    "envFrom": [
                                        {
                                            "configMapRef": {
                                                "name": "<string>",
                                                "optional": "<boolean>"
                                            },
                                            "prefix": "<string>",
                                            "secretRef": {
                                                "name": "<string>",
                                                "optional": "<boolean>"
                                            }
                                        }
                                    ],
                                    "image": "<string>",
                                    "imagePullPolicy": "<string>",
                                    "lifecycle": {
                                        "postStart": {
                                            "exec": {
                                                "command": "<[]string>"
                                            },
                                            "httpGet": {
                                                "host": "<string>",
                                                "httpHeaders": [
                                                    {
                                                        "name": "<string>",
                                                        "value": "<string>"
                                                    }
                                                ],
                                                "path": "<string>",
                                                "port": "<string>",
                                                "scheme": "<string>"
                                            },
                                            "tcpSocket": {
                                                "host": "<string>",
                                                "port": "<string>"
                                            }
                                        },
                                        "preStop": {
                                            "exec": {
                                                "command": "<[]string>"
                                            },
                                            "httpGet": {
                                                "host": "<string>",
                                                "httpHeaders": [
                                                    {
                                                        "name": "<string>",
                                                        "value": "<string>"
                                                    }
                                                ],
                                                "path": "<string>",
                                                "port": "<string>",
                                                "scheme": "<string>"
                                            },
                                            "tcpSocket": {
                                                "host": "<string>",
                                                "port": "<string>"
                                            }
                                        }
                                    },
                                    "livenessProbe": {
                                        "exec": {
                                            "command": "<[]string>"
                                        },
                                        "failureThreshold": "<integer>",
                                        "httpGet": {
                                            "host": "<string>",
                                            "httpHeaders": [
                                                {
                                                    "name": "<string>",
                                                    "value": "<string>"
                                                }
                                            ],
                                            "path": "<string>",
                                            "port": "<string>",
                                            "scheme": "<string>"
                                        },
                                        "initialDelaySeconds": "<integer>",
                                        "periodSeconds": "<integer>",
                                        "successThreshold": "<integer>",
                                        "tcpSocket": {
                                            "host": "<string>",
                                            "port": "<string>"
                                        },
                                        "timeoutSeconds": "<integer>"
                                    },
                                    "name": "<string>",
                                    "ports": [
                                        {
                                            "containerPort": "<integer>",
                                            "hostIP": "<string>",
                                            "hostPort": "<integer>",
                                            "name": "<string>",
                                            "protocol": "<string>"
                                        }
                                    ],
                                    "readinessProbe": {
                                        "exec": {
                                            "command": "<[]string>"
                                        },
                                        "failureThreshold": "<integer>",
                                        "httpGet": {
                                            "host": "<string>",
                                            "httpHeaders": [
                                                {
                                                    "name": "<string>",
                                                    "value": "<string>"
                                                }
                                            ],
                                            "path": "<string>",
                                            "port": "<string>",
                                            "scheme": "<string>"
                                        },
                                        "initialDelaySeconds": "<integer>",
                                        "periodSeconds": "<integer>",
                                        "successThreshold": "<integer>",
                                        "tcpSocket": {
                                            "host": "<string>",
                                            "port": "<string>"
                                        },
                                        "timeoutSeconds": "<integer>"
                                    },
                                    "resources": {
                                        "limits": "<map[string]string>",
                                        "requests": "<map[string]string>"
                                    },
                                    "securityContext": {
                                        "allowPrivilegeEscalation": "<boolean>",
                                        "capabilities": {
                                            "add": "<[]string>",
                                            "drop": "<[]string>"
                                        },
                                        "privileged": "<boolean>",
                                        "procMount": "<string>",
                                        "readOnlyRootFilesystem": "<boolean>",
                                        "runAsGroup": "<integer>",
                                        "runAsNonRoot": "<boolean>",
                                        "runAsUser": "<integer>",
                                        "seLinuxOptions": {
                                            "level": "<string>",
                                            "role": "<string>",
                                            "type": "<string>",
                                            "user": "<string>"
                                        },
                                        "windowsOptions": {
                                            "gmsaCredentialSpec": "<string>",
                                            "gmsaCredentialSpecName": "<string>",
                                            "runAsUserName": "<string>"
                                        }
                                    },
                                    "startupProbe": {
                                        "exec": {
                                            "command": "<[]string>"
                                        },
                                        "failureThreshold": "<integer>",
                                        "httpGet": {
                                            "host": "<string>",
                                            "httpHeaders": [
                                                {
                                                    "name": "<string>",
                                                    "value": "<string>"
                                                }
                                            ],
                                            "path": "<string>",
                                            "port": "<string>",
                                            "scheme": "<string>"
                                        },
                                        "initialDelaySeconds": "<integer>",
                                        "periodSeconds": "<integer>",
                                        "successThreshold": "<integer>",
                                        "tcpSocket": {
                                            "host": "<string>",
                                            "port": "<string>"
                                        },
                                        "timeoutSeconds": "<integer>"
                                    },
                                    "stdin": "<boolean>",
                                    "stdinOnce": "<boolean>",
                                    "targetContainerName": "<string>",
                                    "terminationMessagePath": "<string>",
                                    "terminationMessagePolicy": "<string>",
                                    "tty": "<boolean>",
                                    "volumeDevices": [
                                        {
                                            "devicePath": "<string>",
                                            "name": "<string>"
                                        }
                                    ],
                                    "volumeMounts": [
                                        {
                                            "mountPath": "<string>",
                                            "mountPropagation": "<string>",
                                            "name": "<string>",
                                            "readOnly": "<boolean>",
                                            "subPath": "<string>",
                                            "subPathExpr": "<string>"
                                        }
                                    ],
                                    "workingDir": "<string>"
                                }
                            ],
                            "hostAliases": "<[]COMPONENT.HostAlias>",
                            "hostIPC": "<boolean>",
                            "hostNetwork": "<boolean>",
                            "hostPID": "<boolean>",
                            "hostname": "<string>",
                            "imagePullSecrets": "<[]COMPONENT.ImagePullSecret>",
                            "initContainers": "<[]COMPONENT.Container>",
                            "nodeName": "<string>",
                            "nodeSelector": "<map[string]string>",
                            "overhead": "<map[string]string>",
                            "preemptionPolicy": "<string>",
                            "priority": "<integer>",
                            "priorityClassName": "<string>",
                            "readinessGates": "<[]COMPONENT.ReadinessGate>",
                            "restartPolicy": "<string>",
                            "runtimeClassName": "<string>",
                            "schedulerName": "<string>",
                            "securityContext": "<COMPONENT.SecurityContext>",
                            "serviceAccount": "<string>",
                            "serviceAccountName": "<string>",
                            "shareProcessNamespace": "<boolean>",
                            "subdomain": "<string>",
                            "terminationGracePeriodSeconds": "<integer>",
                            "tolerations": "<[]COMPONENT.Tolerations>",
                            "topologySpreadConstraints": [
                                {
                                    "labelSelector": {
                                        "matchExpressions": [
                                            {
                                                "key": "<string>",
                                                "operator": "<string>",
                                                "values": "<[]string>"
                                            }
                                        ],
                                        "matchLabels": "<map[string]string>"
                                    },
                                    "maxSkew": "<integer>",
                                    "topologyKey": "<string>",
                                    "whenUnsatisfiable": "<string>"
                                }
                            ],
                            "volumes": "<[]COMPONENT.Volume>"
                        }
                    },
                    "updateStrategy": {
                        "rollingUpdate": {
                            "partition": "<integer>"
                        },
                        "type": "<string>"
                    },
                    "volumeClaimTemplates": "<[]COMPONENT.VolumeClaimTemplate>"
                }
            }
        },
        "RoleBinding": {
            "description": "RoleBinding references a role, but does not contain it. It can reference a Role in the same namespace or a ClusterRole in the global namespace. It adds who information via Subjects and namespace information by which namespace it exists in. RoleBindings in a given namespace only have effect in that namespace.",
            "json": {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "RoleBinding",
                "metadata": "<COMPONENT.Metadata>",
                "roleRef": {
                    "apiGroup": "<string>",
                    "kind": "<string>",
                    "name": "<string>"
                },
                "subjects": "<[]COMPONENT.ClusterRoleBindingSubject>"
            }
        },
        "ClusterRoleBinding": {
            "description": "ClusterRoleBinding references a ClusterRole, but not contain it. It can reference a ClusterRole in the global namespace, and adds who information via Subject.",
            "json": {
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "kind": "ClusterRoleBinding",
                "metadata": "<COMPONENT.Metadata>",
                "roleRef": {
                    "apiGroup": "<string>",
                    "kind": "<string>",
                    "name": "<string>"
                },
                "subjects": "<[]COMPONENT.ClusterRoleBindingSubject>"
            }
        },
        "Endpoints": {
            "description": "Endpoints is a collection of endpoints that implement the actual service. Example: Name: \"mysvc\", Subsets: [ { Addresses: [{\"ip\": \"10.10.1.1\"}, {\"ip\": \"10.10.2.2\"}], Ports: [{\"name\": \"a\", \"port\": 8675}, {\"name\": \"b\", \"port\": 309}] }, { Addresses: [{\"ip\": \"10.10.3.3\"}], Ports: [{\"name\": \"a\", \"port\": 93}, {\"name\": \"b\", \"port\": 76}] }, ]",
            "json": {
                "apiVersion": "v1",
                "kind": "Endpoints",
                "metadata": "<COMPONENT.Metadata>",
                "subsets": "<[]COMPONENT.subsets>"
            }
        },
        "LocalSubjectAccessReview": {
            "description": "LocalSubjectAccessReview checks whether or not a user or group can perform an action in a given namespace. Having a namespace scoped resource makes it much easier to grant namespace scoped policy that includes permissions checking.",
            "json": {
                "apiVersion": "authorization.k8s.io/v1",
                "kind": "LocalSubjectAccessReview",
                "metadata": "<COMPONENT.Metadata>",
                "spec": {
                    "extra": "<map[string][]string>",
                    "groups": "<[]string>",
                    "nonResourceAttributes": {
                        "path": "<string>",
                        "verb": "<string>"
                    },
                    "resourceAttributes": {
                        "group": "<string>",
                        "name": "<string>",
                        "namespace": "<string>",
                        "resource": "<string>",
                        "subresource": "<string>",
                        "verb": "<string>",
                        "version": "<string>"
                    },
                    "uid": "<string>",
                    "user": "<string>"
                }
            }
        },
        "EndpointSlice": {
            "description": "EndpointSlice represents a subset of the endpoints that implement a service. For a given service there may be multiple EndpointSlice objects, selected by labels, which must be joined to produce the full set of endpoints.",
            "json": {
                "addressType": "<string>",
                "apiVersion": "discovery.k8s.io/v1beta1",
                "endpoints": [
                    {
                        "addresses": "<[]string>",
                        "conditions": {
                            "ready": "<boolean>"
                        },
                        "hostname": "<string>",
                        "targetRef": {
                            "apiVersion": "<string>",
                            "fieldPath": "<string>",
                            "kind": "<string>",
                            "name": "<string>",
                            "namespace": "<string>",
                            "resourceVersion": "<string>",
                            "uid": "<string>"
                        },
                        "topology": "<map[string]string>"
                    }
                ],
                "kind": "EndpointSlice",
                "metadata": {
                    "annotations": "<map[string]string>",
                    "clusterName": "<string>",
                    "creationTimestamp": "<string>",
                    "deletionGracePeriodSeconds": "<integer>",
                    "deletionTimestamp": "<string>",
                    "finalizers": "<[]string>",
                    "generateName": "<string>",
                    "generation": "<integer>",
                    "labels": "<map[string]string>",
                    "managedFields": [
                        {
                            "apiVersion": "<string>",
                            "fieldsType": "<string>",
                            "fieldsV1": "<map[string]>",
                            "manager": "<string>",
                            "operation": "<string>",
                            "time": "<string>"
                        }
                    ],
                    "name": "<string>",
                    "namespace": "<string>",
                    "ownerReferences": [
                        {
                            "apiVersion": "<string>",
                            "blockOwnerDeletion": "<boolean>",
                            "controller": "<boolean>",
                            "kind": "<string>",
                            "name": "<string>",
                            "uid": "<string>"
                        }
                    ],
                    "resourceVersion": "<string>",
                    "selfLink": "<string>",
                    "uid": "<string>"
                },
                "ports": [
                    {
                        "appProtocol": "<string>",
                        "name": "<string>",
                        "port": "<integer>",
                        "protocol": "<string>"
                    }
                ]
            }
        },
        "ControllerRevision": {
            "description": "ControllerRevision implements an immutable snapshot of state data. Clients are responsible for serializing and deserializing the objects that contain their internal state. Once a ControllerRevision has been successfully created, it can not be updated. The API Server will fail validation of all requests that attempt to mutate the Data field. ControllerRevisions may, however, be deleted. Note that, due to its use by both the DaemonSet and StatefulSet controllers for update and rollback, this object is beta. However, it may be subject to name and representation changes in future releases, and clients should not depend on its stability. It is primarily for internal use by controllers.",
            "json": {
                "apiVersion": "apps/v1",
                "data": "<map[string]>",
                "kind": "ControllerRevision",
                "metadata": "<COMPONENT.Metadata>",
                "revision": "<integer>"
            }
        }
    },
    "api_resources": [
        "DaemonSet",
        "ReplicationController",
        "TokenReview",
        "StorageClass",
        "CustomResourceDefinition",
        "CSIDriver",
        "Binding",
        "SelfSubjectRulesReview",
        "Role",
        "Deployment",
        "ValidatingWebhookConfiguration",
        "PodSecurityPolicy",
        "CronJob",
        "RuntimeClass",
        "ClusterRole",
        "Service",
        "IngressClass",
        "Ingress",
        "PriorityClass",
        "PersistentVolume",
        "Event",
        "CSINode",
        "ReplicaSet",
        "MutatingWebhookConfiguration",
        "ServiceAccount",
        "CertificateSigningRequest",
        "SubjectAccessReview",
        "APIService",
        "ConfigMap",
        "SelfSubjectAccessReview",
        "Lease",
        "Job",
        "PodDisruptionBudget",
        "Namespace",
        "HorizontalPodAutoscaler",
        "Pod",
        "PodTemplate",
        "Secret",
        "LimitRange",
        "NetworkPolicy",
        "ResourceQuota",
        "VolumeAttachment",
        "PersistentVolumeClaim",
        "Node",
        "ComponentStatus",
        "StatefulSet",
        "RoleBinding",
        "ClusterRoleBinding",
        "Endpoints",
        "LocalSubjectAccessReview",
        "EndpointSlice",
        "ControllerRevision"
    ],
    "components_data": {
        "VolumeMount": {
            "mountPath": "<string>",
            "mountPropagation": "<string>",
            "name": "<string>",
            "readOnly": "<boolean>",
            "subPath": "<string>",
            "subPathExpr": "<string>"
        },
        "ManagedField": {
            "apiVersion": "<string>",
            "fieldsType": "<string>",
            "fieldsV1": "<map[string]>",
            "manager": "<string>",
            "operation": "<string>",
            "time": "<string>"
        },
        "HostAlias": {
            "hostnames": "<[]string>",
            "ip": "<string>"
        },
        "NetworkPolicyIngress": {
            "from": [
                {
                    "ipBlock": {
                        "cidr": "<string>",
                        "except": "<[]string>"
                    },
                    "namespaceSelector": {
                        "matchExpressions": [
                            {
                                "key": "<string>",
                                "operator": "<string>",
                                "values": "<[]string>"
                            }
                        ],
                        "matchLabels": "<map[string]string>"
                    },
                    "podSelector": {
                        "matchExpressions": [
                            {
                                "key": "<string>",
                                "operator": "<string>",
                                "values": "<[]string>"
                            }
                        ],
                        "matchLabels": "<map[string]string>"
                    }
                }
            ],
            "ports": [
                {
                    "port": "<string>",
                    "protocol": "<string>"
                }
            ]
        },
        "VolumeClaimTemplate": {
            "apiVersion": "<string>",
            "kind": "<string>",
            "metadata": "<COMPONENT.Metadata>",
            "spec": {
                "accessModes": "<[]string>",
                "dataSource": {
                    "apiGroup": "<string>",
                    "kind": "<string>",
                    "name": "<string>"
                },
                "resources": {
                    "limits": "<map[string]string>",
                    "requests": "<map[string]string>"
                },
                "selector": "<COMPONENT.Selector>",
                "storageClassName": "<string>",
                "volumeMode": "<string>",
                "volumeName": "<string>"
            }
        },
        "DownwardAPIItem": {
            "fieldRef": {
                "apiVersion": "<string>",
                "fieldPath": "<string>"
            },
            "mode": "<integer>",
            "path": "<string>",
            "resourceFieldRef": {
                "containerName": "<string>",
                "divisor": "<string>",
                "resource": "<string>"
            }
        },
        "NodePreferredAffinity": {
            "preference": "<COMPONENT.NodeSelectorTerm>",
            "weight": "<integer>"
        },
        "Volume": {
            "awsElasticBlockStore": {
                "fsType": "<string>",
                "partition": "<integer>",
                "readOnly": "<boolean>",
                "volumeID": "<string>"
            },
            "azureDisk": {
                "cachingMode": "<string>",
                "diskName": "<string>",
                "diskURI": "<string>",
                "fsType": "<string>",
                "kind": "<string>",
                "readOnly": "<boolean>"
            },
            "azureFile": {
                "readOnly": "<boolean>",
                "secretName": "<string>",
                "shareName": "<string>"
            },
            "cephfs": {
                "monitors": "<[]string>",
                "path": "<string>",
                "readOnly": "<boolean>",
                "secretFile": "<string>",
                "secretRef": {
                    "name": "<string>"
                },
                "user": "<string>"
            },
            "cinder": {
                "fsType": "<string>",
                "readOnly": "<boolean>",
                "secretRef": {
                    "name": "<string>"
                },
                "volumeID": "<string>"
            },
            "configMap": {
                "defaultMode": "<integer>",
                "items": "<[]COMPONENT.ConfigMapItem>",
                "name": "<string>",
                "optional": "<boolean>"
            },
            "csi": {
                "driver": "<string>",
                "fsType": "<string>",
                "nodePublishSecretRef": {
                    "name": "<string>"
                },
                "readOnly": "<boolean>",
                "volumeAttributes": "<map[string]string>"
            },
            "downwardAPI": {
                "defaultMode": "<integer>",
                "items": "<[]COMPONENT.DownwardAPIItem>"
            },
            "emptyDir": {
                "medium": "<string>",
                "sizeLimit": "<string>"
            },
            "fc": {
                "fsType": "<string>",
                "lun": "<integer>",
                "readOnly": "<boolean>",
                "targetWWNs": "<[]string>",
                "wwids": "<[]string>"
            },
            "flexVolume": {
                "driver": "<string>",
                "fsType": "<string>",
                "options": "<map[string]string>",
                "readOnly": "<boolean>",
                "secretRef": {
                    "name": "<string>"
                }
            },
            "flocker": {
                "datasetName": "<string>",
                "datasetUUID": "<string>"
            },
            "gcePersistentDisk": {
                "fsType": "<string>",
                "partition": "<integer>",
                "pdName": "<string>",
                "readOnly": "<boolean>"
            },
            "gitRepo": {
                "directory": "<string>",
                "repository": "<string>",
                "revision": "<string>"
            },
            "glusterfs": {
                "endpoints": "<string>",
                "path": "<string>",
                "readOnly": "<boolean>"
            },
            "hostPath": {
                "path": "<string>",
                "type": "<string>"
            },
            "iscsi": {
                "chapAuthDiscovery": "<boolean>",
                "chapAuthSession": "<boolean>",
                "fsType": "<string>",
                "initiatorName": "<string>",
                "iqn": "<string>",
                "iscsiInterface": "<string>",
                "lun": "<integer>",
                "portals": "<[]string>",
                "readOnly": "<boolean>",
                "secretRef": {
                    "name": "<string>"
                },
                "targetPortal": "<string>"
            },
            "name": "<string>",
            "nfs": {
                "path": "<string>",
                "readOnly": "<boolean>",
                "server": "<string>"
            },
            "persistentVolumeClaim": {
                "claimName": "<string>",
                "readOnly": "<boolean>"
            },
            "photonPersistentDisk": {
                "fsType": "<string>",
                "pdID": "<string>"
            },
            "portworxVolume": {
                "fsType": "<string>",
                "readOnly": "<boolean>",
                "volumeID": "<string>"
            },
            "projected": {
                "defaultMode": "<integer>",
                "sources": "<[]COMPONENT.ProjectedVolumeSources>"
            },
            "quobyte": {
                "group": "<string>",
                "readOnly": "<boolean>",
                "registry": "<string>",
                "tenant": "<string>",
                "user": "<string>",
                "volume": "<string>"
            },
            "rbd": {
                "fsType": "<string>",
                "image": "<string>",
                "keyring": "<string>",
                "monitors": "<[]string>",
                "pool": "<string>",
                "readOnly": "<boolean>",
                "secretRef": {
                    "name": "<string>"
                },
                "user": "<string>"
            },
            "scaleIO": {
                "fsType": "<string>",
                "gateway": "<string>",
                "protectionDomain": "<string>",
                "readOnly": "<boolean>",
                "secretRef": {
                    "name": "<string>"
                },
                "sslEnabled": "<boolean>",
                "storageMode": "<string>",
                "storagePool": "<string>",
                "system": "<string>",
                "volumeName": "<string>"
            },
            "secret": {
                "defaultMode": "<integer>",
                "items": "<[]COMPONENT.SecretItem>",
                "optional": "<boolean>",
                "secretName": "<string>"
            },
            "storageos": {
                "fsType": "<string>",
                "readOnly": "<boolean>",
                "secretRef": {
                    "name": "<string>"
                },
                "volumeName": "<string>",
                "volumeNamespace": "<string>"
            },
            "vsphereVolume": {
                "fsType": "<string>",
                "storagePolicyID": "<string>",
                "storagePolicyName": "<string>",
                "volumePath": "<string>"
            }
        },
        "IngressTLS": {
            "hosts": "<[]string>",
            "secretName": "<string>"
        },
        "IngressRulePath": {
            "backend": {
                "resource": {
                    "apiGroup": "<string>",
                    "kind": "<string>",
                    "name": "<string>"
                },
                "serviceName": "<string>",
                "servicePort": "<string>"
            },
            "path": "<string>",
            "pathType": "<string>"
        },
        "AllowedFlexVolume": {
            "driver": "<string>"
        },
        "ComponentStatusCondition": {
            "error": "<string>",
            "message": "<string>",
            "type": "<string>"
        },
        "NonResourceAttribute": {
            "path": "<string>",
            "verb": "<string>"
        },
        "EnvironmentVariable": {
            "name": "<string>",
            "value": "<string>",
            "valueFrom": {
                "configMapKeyRef": {
                    "key": "<string>",
                    "name": "<string>",
                    "optional": "<boolean>"
                },
                "fieldRef": {
                    "apiVersion": "<string>",
                    "fieldPath": "<string>"
                },
                "resourceFieldRef": {
                    "containerName": "<string>",
                    "divisor": "<string>",
                    "resource": "<string>"
                },
                "secretKeyRef": {
                    "key": "<string>",
                    "name": "<string>",
                    "optional": "<boolean>"
                }
            }
        },
        "Webhook": {
            "admissionReviewVersions": "<[]string>",
            "clientConfig": {
                "caBundle": "<string>",
                "service": {
                    "name": "<string>",
                    "namespace": "<string>",
                    "path": "<string>",
                    "port": "<integer>"
                },
                "url": "<string>"
            },
            "failurePolicy": "<string>",
            "matchPolicy": "<string>",
            "name": "<string>",
            "namespaceSelector": "<COMPONENT.Selector",
            "objectSelector": "<COMPONENT.Selector",
            "reinvocationPolicy": "<string>",
            "rules": "<[]COMPONENT.Rule>",
            "sideEffects": "<string>",
            "timeoutSeconds": "<integer>"
        },
        "ProjectedVolumeSource": {
            "configMap": {
                "items": "<[]COMPONENT.ConfigMapItem>",
                "name": "<string>",
                "optional": "<boolean>"
            },
            "downwardAPI": {
                "items": "<[]COMPONENT.DownwardAPIItem>"
            },
            "secret": {
                "items": "<[]COMPONENT.SecretItem>",
                "name": "<string>",
                "optional": "<boolean>"
            },
            "serviceAccountToken": {
                "audience": "<string>",
                "expirationSeconds": "<integer>",
                "path": "<string>"
            }
        },
        "AllowedHostPath": {
            "pathPrefix": "<string>",
            "readOnly": "<boolean>"
        },
        "ImagePullSecret": {
            "name": "<string>"
        },
        "SubsetPort": {
            "appProtocol": "<string>",
            "name": "<string>",
            "port": "<integer>",
            "protocol": "<string>"
        },
        "RoleRule": {
            "apiGroups": "<[]string>",
            "nonResourceURLs": "<[]string>",
            "resourceNames": "<[]string>",
            "resources": "<[]string>",
            "verbs": "<[]string>"
        },
        "ServicePort": {
            "appProtocol": "<string>",
            "name": "<string>",
            "nodePort": "<integer>",
            "port": "<integer>",
            "protocol": "<string>",
            "targetPort": "<string>"
        },
        "Selector": {
            "matchExpressions": "<[]COMPONENT.MatchExpression>",
            "matchLabels": "<map[string]string>"
        },
        "Range": {
            "max": "<integer>",
            "min": "<integer>"
        },
        "AllowedCSIDriver": {
            "name": "<string>"
        },
        "PrinterColumn": None,
        "ContainerPort": {
            "containerPort": "<integer>",
            "hostIP": "<string>",
            "hostPort": "<integer>",
            "name": "<string>",
            "protocol": "<string>"
        },
        "ConfigMapItem": {
            "key": "<string>",
            "mode": "<integer>",
            "path": "<string>"
        },
        "NodeSelectorTerm": {
            "matchExpressions": "<[]COMPONENT.MatchExpression>",
            "matchFields": "<[]COMPONENT.MatchExpression>"
        },
        "DNSConfigOptions": {
            "name": "<string>",
            "value": "<string>"
        },
        "Metadata": {
            "annotations": "<map[string]string>",
            "clusterName": "<string>",
            "creationTimestamp": "<string>",
            "deletionGracePeriodSeconds": "<integer>",
            "deletionTimestamp": "<string>",
            "finalizers": "<[]string>",
            "generateName": "<string>",
            "generation": "<integer>",
            "labels": "<map[string]string>",
            "managedFields": "<[]COMPONENT.ManagedField>",
            "name": "<string>",
            "namespace": "<string>",
            "ownerReferences": "<[]COMPONENT.OwnerReference>",
            "resourceVersion": "<string>",
            "selfLink": "<string>",
            "uid": "<string>"
        },
        "ClusterRule": {
            "apiGroups": "<[]string>",
            "apiVersions": "<[]string>",
            "operations": "<[]string>",
            "resources": "<[]string>",
            "scope": "<string>"
        },
        "PodPreferredAffinity": {
            "podAffinityTerm": {
                "labelSelector": {
                    "matchExpressions": "<[]COMPONENT.MatchExpression>",
                    "matchLabels": "<map[string]string>"
                },
                "namespaces": "<[]string>",
                "topologyKey": "<string>"
            },
            "weight": "<integer>"
        },
        "ResourceDefinitionVersion": {
            "additionalPrinterColumns": "<[]COMPONENT.PrinterColumn>",
            "name": "<string>",
            "schema": {
                "openAPIV3Schema": {
                    "$ref": "<string>",
                    "$schema": "<string>",
                    "additionalItems": "<>",
                    "additionalProperties": "<>",
                    "allOf": None,
                    "anyOf": None,
                    "default": "<>",
                    "definitions": None,
                    "dependencies": "<map[string]>",
                    "description": "<string>",
                    "enum": "<[]>",
                    "example": "<>",
                    "exclusiveMaximum": "<boolean>",
                    "exclusiveMinimum": "<boolean>",
                    "externalDocs": {
                        "description": "<string>",
                        "url": "<string>"
                    },
                    "format": "<string>",
                    "id": "<string>",
                    "items": "<>",
                    "maxItems": "<integer>",
                    "maxLength": "<integer>",
                    "maxProperties": "<integer>",
                    "maximum": "<number>",
                    "minItems": "<integer>",
                    "minLength": "<integer>",
                    "minProperties": "<integer>",
                    "minimum": "<number>",
                    "multipleOf": "<number>",
                    "not": None,
                    "nullable": "<boolean>",
                    "oneOf": None,
                    "pattern": "<string>",
                    "patternProperties": None,
                    "properties": None,
                    "required": "<[]string>",
                    "title": "<string>",
                    "type": "<string>",
                    "uniqueItems": "<boolean>",
                    "x-kubernetes-embedded-resource": "<boolean>",
                    "x-kubernetes-int-or-string": "<boolean>",
                    "x-kubernetes-list-map-keys": "<[]string>",
                    "x-kubernetes-list-type": "<string>",
                    "x-kubernetes-map-type": "<string>",
                    "x-kubernetes-preserve-unknown-fields": "<boolean>"
                }
            },
            "served": "<boolean>",
            "storage": "<boolean>",
            "subresources": {
                "scale": {
                    "labelSelectorPath": "<string>",
                    "specReplicasPath": "<string>",
                    "statusReplicasPath": "<string>"
                },
                "status": "<map[string]>"
            }
        },
        "AllowedTopology": {
            "matchLabelExpressions": "<[]COMPONENT.MatchLabelExpression>"
        },
        "SecurityContext": {
            "fsGroup": "<COMPONENT.UserGroup>",
            "fsGroupChangePolicy": "<string>",
            "runAsGroup": "<COMPONENT.UserGroup>",
            "runAsNonRoot": "<boolean>",
            "runAsUser": "<COMPONENT.UserGroup>",
            "seLinuxOptions": {
                "level": "<string>",
                "role": "<string>",
                "type": "<string>",
                "user": "<string>"
            },
            "supplementalGroups": "<COMPONENT.UserGroup>",
            "sysctls": "<[]COMPONENTS.Sysctl>",
            "windowsOptions": {
                "gmsaCredentialSpec": "<string>",
                "gmsaCredentialSpecName": "<string>",
                "runAsUserName": "<string>"
            }
        },
        "LifecycleDefinition": {
            "exec": {
                "command": "<[]string>"
            },
            "httpGet": {
                "host": "<string>",
                "httpHeaders": "<[]COMPONENT.HTTPHeader>",
                "path": "<string>",
                "port": "<string>",
                "scheme": "<string>"
            },
            "tcpSocket": {
                "host": "<string>",
                "port": "<string>"
            }
        },
        "OwnerReference": {
            "apiVersion": "<string>",
            "blockOwnerDeletion": "<boolean>",
            "controller": "<boolean>",
            "kind": "<string>",
            "name": "<string>",
            "uid": "<string>"
        },
        "SecretItem": {
            "key": "<string>",
            "mode": "<integer>",
            "path": "<string>"
        },
        "PodAntiAffinity": {
            "preferredDuringSchedulingIgnoredDuringExecution": "<[]COMPONENT.PodPreferredAntiAffinity>",
            "requiredDuringSchedulingIgnoredDuringExecution": "<[]COMPONENT.PodRequiredAntiAffinity>"
        },
        "Container": {
            "args": "<[]string>",
            "command": "<[]string>",
            "env": "<[]COMPONENT.EnvironmentVariable>",
            "envFrom": "<[]COMPONENT.EnvironmentVariableSource>",
            "image": "<string>",
            "imagePullPolicy": "<string>",
            "lifecycle": {
                "postStart": "<[]COMPONENT.LifecycleDefinition>",
                "preStop": "<[]COMPONENT.LifecycleDefinition>"
            },
            "livenessProbe": "<COMPONENT.Probe>",
            "name": "<string>",
            "ports": "<[]COMPONENT.ContainerPort>",
            "readinessProbe": "<COMPONENT.Probe>",
            "resources": {
                "limits": "<map[string]string>",
                "requests": "<map[string]string>"
            },
            "securityContext": "<COMPONENT.SecurityContext>",
            "startupProbe": {
                "exec": {
                    "command": "<[]string>"
                },
                "failureThreshold": "<integer>",
                "httpGet": {
                    "host": "<string>",
                    "httpHeaders": [
                        {
                            "name": "<string>",
                            "value": "<string>"
                        }
                    ],
                    "path": "<string>",
                    "port": "<string>",
                    "scheme": "<string>"
                },
                "initialDelaySeconds": "<integer>",
                "periodSeconds": "<integer>",
                "successThreshold": "<integer>",
                "tcpSocket": {
                    "host": "<string>",
                    "port": "<string>"
                },
                "timeoutSeconds": "<integer>"
            },
            "stdin": "<boolean>",
            "stdinOnce": "<boolean>",
            "terminationMessagePath": "<string>",
            "terminationMessagePolicy": "<string>",
            "tty": "<boolean>",
            "volumeDevices": "<[]COMPONENT.VolumeDevice>",
            "volumeMounts": "<[]COMPONENT.VolumeMount>",
            "workingDir": "<string>"
        },
        "Address": {
            "hostname": "<string>",
            "ip": "<string>",
            "nodeName": "<string>",
            "targetRef": {
                "apiVersion": "<string>",
                "fieldPath": "<string>",
                "kind": "<string>",
                "name": "<string>",
                "namespace": "<string>",
                "resourceVersion": "<string>",
                "uid": "<string>"
            }
        },
        "IngressRule": {
            "host": "<string>",
            "http": {
                "paths": "<[]COMPONENT.IngressRulePath>"
            }
        },
        "ScopeSelector": {
            "operator": "<string>",
            "scopeName": "<string>",
            "values": "<[]string>"
        },
        "UserGroup": {
            "ranges": "<[]COMPONENTS.Range>",
            "rule": "<string>"
        },
        "PodRequiredAntiAffinity": {
            "labelSelector": {
                "matchExpressions": "<[]COMPONENT.MatchExpression>",
                "matchLabels": "<map[string]string>"
            },
            "namespaces": "<[]string>",
            "topologyKey": "<string>"
        },
        "EnvironmentVariableSource": {
            "configMapRef": {
                "name": "<string>",
                "optional": "<boolean>"
            },
            "prefix": "<string>",
            "secretRef": {
                "name": "<string>",
                "optional": "<boolean>"
            }
        },
        "Limit": {
            "default": "<map[string]string>",
            "defaultRequest": "<map[string]string>",
            "max": "<map[string]string>",
            "maxLimitRequestRatio": "<map[string]string>",
            "min": "<map[string]string>",
            "type": "<string>"
        },
        "NodeAffinity": {
            "preferredDuringSchedulingIgnoredDuringExecution": "<[]COMPONENT.NodePreferredAffinity>",
            "requiredDuringSchedulingIgnoredDuringExecution": "<[]COMPONENT.NodeRequiredAffinity>"
        },
        "NetworkPolicyEgress": {
            "ports": [
                {
                    "port": "<string>",
                    "protocol": "<string>"
                }
            ],
            "to": [
                {
                    "ipBlock": {
                        "cidr": "<string>",
                        "except": "<[]string>"
                    },
                    "namespaceSelector": {
                        "matchExpressions": [
                            {
                                "key": "<string>",
                                "operator": "<string>",
                                "values": "<[]string>"
                            }
                        ],
                        "matchLabels": "<map[string]string>"
                    },
                    "podSelector": {
                        "matchExpressions": [
                            {
                                "key": "<string>",
                                "operator": "<string>",
                                "values": "<[]string>"
                            }
                        ],
                        "matchLabels": "<map[string]string>"
                    }
                }
            ]
        },
        "Subset": {
            "addresses": "<[]COMPONENT.Address>",
            "notReadyAddresses": "<[]COMPONENT.Address>",
            "ports": "<[]COMPONENT.SubsetPort>"
        },
        "DNSConfig": {
            "nameservers": "<[]string>",
            "options": "<[]COMPONENTS.DNSConfigOptions>",
            "searches": "<[]string>"
        },
        "PodAffinity": {
            "preferredDuringSchedulingIgnoredDuringExecution": "<[]COMPONENT.PodPreferredAffinity>",
            "requiredDuringSchedulingIgnoredDuringExecution": "<[]COMPONENT.PodRequiredAffinity>"
        },
        "MatchExpression": {
            "key": "<string>",
            "operator": "<string>",
            "values": "<[]string>"
        },
        "Probe": {
            "exec": {
                "command": "<[]string>"
            },
            "failureThreshold": "<integer>",
            "httpGet": {
                "host": "<string>",
                "httpHeaders": "<[]COMPONENT.HTTPHeader>",
                "path": "<string>",
                "port": "<string>",
                "scheme": "<string>"
            },
            "initialDelaySeconds": "<integer>",
            "periodSeconds": "<integer>",
            "successThreshold": "<integer>",
            "tcpSocket": {
                "host": "<string>",
                "port": "<string>"
            },
            "timeoutSeconds": "<integer>"
        },
        "ServiceAccountSecret": {
            "apiVersion": "<string>",
            "fieldPath": "<string>",
            "kind": "<string>",
            "name": "<string>",
            "namespace": "<string>",
            "resourceVersion": "<string>",
            "uid": "<string>"
        },
        "ReadinessGate": {
            "conditionType": "<string>"
        },
        "Toleration": {
            "effect": "<string>",
            "key": "<string>",
            "operator": "<string>",
            "tolerationSeconds": "<integer>",
            "value": "<string>"
        },
        "NodeRequiredAffinity": {
            "nodeSelectorTerms": "<[]COMPONENT.NodeSelectorTerm>"
        },
        "MatchLabelExpression": {
            "key": "<string>",
            "values": "<[]string>"
        },
        "Sysctl": {
            "name": "<string>",
            "value": "<string>"
        },
        "HTTPHeader": {
            "name": "<string>",
            "value": "<string>"
        },
        "ResourceAttribute": {
            "group": "<string>",
            "name": "<string>",
            "namespace": "<string>",
            "resource": "<string>",
            "subresource": "<string>",
            "verb": "<string>",
            "version": "<string>"
        },
        "ClientConfig": None,
        "VolumeDevice": {
            "devicePath": "<string>",
            "name": "<string>"
        },
        "PodPreferredAntiAffinity": {
            "podAffinityTerm": {
                "labelSelector": {
                    "matchExpressions": "<[]COMPONENT.MatchExpression>",
                    "matchLabels": "<map[string]string>"
                },
                "namespaces": "<[]string>",
                "topologyKey": "<string>"
            },
            "weight": "<integer>"
        },
        "PodRequiredAffinity": {
            "labelSelector": {
                "matchExpressions": "<[]COMPONENT.MatchExpression>",
                "matchLabels": "<map[string]string>"
            },
            "namespaces": "<[]string>",
            "topologyKey": "<string>"
        },
        "Taint": {
            "effect": "<string>",
            "key": "<string>",
            "timeAdded": "<string>",
            "value": "<string>"
        },
        "ContainerSpec": {
            "activeDeadlineSeconds": "<integer>",
            "affinity": {
                "nodeAffinity": "<COMPONENT.NodeAffinity>",
                "podAffinity": "<COMPONENT.PodAffinity>",
                "podAntiAffinity": "<COMPONENT.PodAntiAffinity>"
            },
            "automountServiceAccountToken": "<boolean>",
            "containers": "<[]COMPONENT.Container>",
            "dnsConfig": "<COMPONENT.DNSConfig>",
            "dnsPolicy": "<string>",
            "enableServiceLinks": "<boolean>",
            "ephemeralContainers": [
                {
                    "args": "<[]string>",
                    "command": "<[]string>",
                    "env": [
                        {
                            "name": "<string>",
                            "value": "<string>",
                            "valueFrom": {
                                "configMapKeyRef": {
                                    "key": "<string>",
                                    "name": "<string>",
                                    "optional": "<boolean>"
                                },
                                "fieldRef": {
                                    "apiVersion": "<string>",
                                    "fieldPath": "<string>"
                                },
                                "resourceFieldRef": {
                                    "containerName": "<string>",
                                    "divisor": "<string>",
                                    "resource": "<string>"
                                },
                                "secretKeyRef": {
                                    "key": "<string>",
                                    "name": "<string>",
                                    "optional": "<boolean>"
                                }
                            }
                        }
                    ],
                    "envFrom": [
                        {
                            "configMapRef": {
                                "name": "<string>",
                                "optional": "<boolean>"
                            },
                            "prefix": "<string>",
                            "secretRef": {
                                "name": "<string>",
                                "optional": "<boolean>"
                            }
                        }
                    ],
                    "image": "<string>",
                    "imagePullPolicy": "<string>",
                    "lifecycle": {
                        "postStart": {
                            "exec": {
                                "command": "<[]string>"
                            },
                            "httpGet": {
                                "host": "<string>",
                                "httpHeaders": [
                                    {
                                        "name": "<string>",
                                        "value": "<string>"
                                    }
                                ],
                                "path": "<string>",
                                "port": "<string>",
                                "scheme": "<string>"
                            },
                            "tcpSocket": {
                                "host": "<string>",
                                "port": "<string>"
                            }
                        },
                        "preStop": {
                            "exec": {
                                "command": "<[]string>"
                            },
                            "httpGet": {
                                "host": "<string>",
                                "httpHeaders": [
                                    {
                                        "name": "<string>",
                                        "value": "<string>"
                                    }
                                ],
                                "path": "<string>",
                                "port": "<string>",
                                "scheme": "<string>"
                            },
                            "tcpSocket": {
                                "host": "<string>",
                                "port": "<string>"
                            }
                        }
                    },
                    "livenessProbe": {
                        "exec": {
                            "command": "<[]string>"
                        },
                        "failureThreshold": "<integer>",
                        "httpGet": {
                            "host": "<string>",
                            "httpHeaders": [
                                {
                                    "name": "<string>",
                                    "value": "<string>"
                                }
                            ],
                            "path": "<string>",
                            "port": "<string>",
                            "scheme": "<string>"
                        },
                        "initialDelaySeconds": "<integer>",
                        "periodSeconds": "<integer>",
                        "successThreshold": "<integer>",
                        "tcpSocket": {
                            "host": "<string>",
                            "port": "<string>"
                        },
                        "timeoutSeconds": "<integer>"
                    },
                    "name": "<string>",
                    "ports": [
                        {
                            "containerPort": "<integer>",
                            "hostIP": "<string>",
                            "hostPort": "<integer>",
                            "name": "<string>",
                            "protocol": "<string>"
                        }
                    ],
                    "readinessProbe": {
                        "exec": {
                            "command": "<[]string>"
                        },
                        "failureThreshold": "<integer>",
                        "httpGet": {
                            "host": "<string>",
                            "httpHeaders": [
                                {
                                    "name": "<string>",
                                    "value": "<string>"
                                }
                            ],
                            "path": "<string>",
                            "port": "<string>",
                            "scheme": "<string>"
                        },
                        "initialDelaySeconds": "<integer>",
                        "periodSeconds": "<integer>",
                        "successThreshold": "<integer>",
                        "tcpSocket": {
                            "host": "<string>",
                            "port": "<string>"
                        },
                        "timeoutSeconds": "<integer>"
                    },
                    "resources": {
                        "limits": "<map[string]string>",
                        "requests": "<map[string]string>"
                    },
                    "securityContext": {
                        "allowPrivilegeEscalation": "<boolean>",
                        "capabilities": {
                            "add": "<[]string>",
                            "drop": "<[]string>"
                        },
                        "privileged": "<boolean>",
                        "procMount": "<string>",
                        "readOnlyRootFilesystem": "<boolean>",
                        "runAsGroup": "<integer>",
                        "runAsNonRoot": "<boolean>",
                        "runAsUser": "<integer>",
                        "seLinuxOptions": {
                            "level": "<string>",
                            "role": "<string>",
                            "type": "<string>",
                            "user": "<string>"
                        },
                        "windowsOptions": {
                            "gmsaCredentialSpec": "<string>",
                            "gmsaCredentialSpecName": "<string>",
                            "runAsUserName": "<string>"
                        }
                    },
                    "startupProbe": {
                        "exec": {
                            "command": "<[]string>"
                        },
                        "failureThreshold": "<integer>",
                        "httpGet": {
                            "host": "<string>",
                            "httpHeaders": [
                                {
                                    "name": "<string>",
                                    "value": "<string>"
                                }
                            ],
                            "path": "<string>",
                            "port": "<string>",
                            "scheme": "<string>"
                        },
                        "initialDelaySeconds": "<integer>",
                        "periodSeconds": "<integer>",
                        "successThreshold": "<integer>",
                        "tcpSocket": {
                            "host": "<string>",
                            "port": "<string>"
                        },
                        "timeoutSeconds": "<integer>"
                    },
                    "stdin": "<boolean>",
                    "stdinOnce": "<boolean>",
                    "targetContainerName": "<string>",
                    "terminationMessagePath": "<string>",
                    "terminationMessagePolicy": "<string>",
                    "tty": "<boolean>",
                    "volumeDevices": [
                        {
                            "devicePath": "<string>",
                            "name": "<string>"
                        }
                    ],
                    "volumeMounts": [
                        {
                            "mountPath": "<string>",
                            "mountPropagation": "<string>",
                            "name": "<string>",
                            "readOnly": "<boolean>",
                            "subPath": "<string>",
                            "subPathExpr": "<string>"
                        }
                    ],
                    "workingDir": "<string>"
                }
            ],
            "hostAliases": "<[]COMPONENT.HostAlias>",
            "hostIPC": "<boolean>",
            "hostNetwork": "<boolean>",
            "hostPID": "<boolean>",
            "hostname": "<string>",
            "imagePullSecrets": "<[]COMPONENT.ImagePullSecret>",
            "initContainers": "<[]COMPONENT.Container>",
            "nodeName": "<string>",
            "nodeSelector": "<map[string]string>",
            "overhead": "<map[string]string>",
            "preemptionPolicy": "<string>",
            "priority": "<integer>",
            "priorityClassName": "<string>",
            "readinessGates": "<[]COMPONENT.ReadinessGate>",
            "restartPolicy": "<string>",
            "runtimeClassName": "<string>",
            "schedulerName": "<string>",
            "securityContext": "<COMPONENT.SecurityContext>",
            "serviceAccount": "<string>",
            "serviceAccountName": "<string>",
            "shareProcessNamespace": "<boolean>",
            "subdomain": "<string>",
            "terminationGracePeriodSeconds": "<integer>",
            "tolerations": "<[]COMPONENT.Tolerations>",
            "topologySpreadConstraints": [
                {
                    "labelSelector": {
                        "matchExpressions": [
                            {
                                "key": "<string>",
                                "operator": "<string>",
                                "values": "<[]string>"
                            }
                        ],
                        "matchLabels": "<map[string]string>"
                    },
                    "maxSkew": "<integer>",
                    "topologyKey": "<string>",
                    "whenUnsatisfiable": "<string>"
                }
            ],
            "volumes": "<[]COMPONENT.Volume>"
        },
        "ClusterRoleBindingSubject": {
            "apiGroup": "<string>",
            "kind": "<string>",
            "name": "<string>",
            "namespace": "<string>"
        },
        "CSINodeDriver": {
            "allocatable": {
                "count": "<integer>"
            },
            "name": "<string>",
            "nodeID": "<string>",
            "topologyKeys": "<[]string>"
        }
    },
    "components": [
        "VolumeMount",
        "ManagedField",
        "HostAlias",
        "NetworkPolicyIngress",
        "VolumeClaimTemplate",
        "DownwardAPIItem",
        "NodePreferredAffinity",
        "Volume",
        "IngressTLS",
        "IngressRulePath",
        "AllowedFlexVolume",
        "ComponentStatusCondition",
        "NonResourceAttribute",
        "EnvironmentVariable",
        "Webhook",
        "ProjectedVolumeSource",
        "AllowedHostPath",
        "ImagePullSecret",
        "SubsetPort",
        "RoleRule",
        "ServicePort",
        "Selector",
        "Range",
        "AllowedCSIDriver",
        "PrinterColumn",
        "ContainerPort",
        "ConfigMapItem",
        "NodeSelectorTerm",
        "DNSConfigOptions",
        "Metadata",
        "ClusterRule",
        "PodPreferredAffinity",
        "ResourceDefinitionVersion",
        "AllowedTopology",
        "SecurityContext",
        "LifecycleDefinition",
        "OwnerReference",
        "SecretItem",
        "PodAntiAffinity",
        "Container",
        "Address",
        "IngressRule",
        "ScopeSelector",
        "UserGroup",
        "PodRequiredAntiAffinity",
        "EnvironmentVariableSource",
        "Limit",
        "NodeAffinity",
        "NetworkPolicyEgress",
        "Subset",
        "DNSConfig",
        "PodAffinity",
        "MatchExpression",
        "Probe",
        "ServiceAccountSecret",
        "ReadinessGate",
        "Toleration",
        "NodeRequiredAffinity",
        "MatchLabelExpression",
        "Sysctl",
        "HTTPHeader",
        "ResourceAttribute",
        "ClientConfig",
        "VolumeDevice",
        "PodPreferredAntiAffinity",
        "PodRequiredAffinity",
        "Taint",
        "ContainerSpec",
        "ClusterRoleBindingSubject",
        "CSINodeDriver"
    ]
}