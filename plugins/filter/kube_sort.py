# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#filter-plugins
# https://github.com/kubernetes-sigs/kustomize/blob/kustomize/v3.9.4/api/resid/gvk.go#L116
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class FilterModule(object):
    def filters(self):
        return {'kube_sort': self.kube_sort}

    def kube_sort(self, resources):
        orderFirst = [
            "Namespace",
            "CustomResourceDefinition",

            # RBAC
            "ServiceAccount",
            "Role",
            "RoleBinding",
            "ClusterRole",
            "ClusterRoleBinding",

            # Configuration
            "ConfigMap",
            "Secret",
            "SealedSecret",

            # Storage
            "StorageClass",
            "PersistentVolume",
            "PersistentVolumeClaim",

            # Other
            "ResourceQuota",
            "PodSecurityPolicy",
            "Endpoints",
            "LimitRange",
            "PriorityClass",
            "PodDisruptionBudget",

            # Flux
            "GitRepository"
            "HelmRepository",
            "HelmRelease",
            "Kustomization",

            # Workload
            "Deployment",
            "StatefulSet",
            "ReplicaSet",
            "Job",
            "CronJob",

            # Network
            "Service",
            "Ingress"
        ]

        orderLast = [
            # Other
            "MutatingWebhookConfiguration",
            "ValidatingWebhookConfiguration"
        ]

        order = {}

        for index, res in enumerate(orderFirst):
            order[res] = -len(orderFirst) + index

        for index, res in enumerate(orderLast):
            order[res] = index + 1

        return sorted(resources, key=lambda obj: order.get(obj["kind"], 0))
