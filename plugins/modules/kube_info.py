#!/usr/bin/python
# -*- coding: utf-8 -*-

# See: https://github.com/kubernetes-sigs/kubespray/blob/v2.15.1/library/kube.py
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
module: kube
short_description: Manage Kubernetes resources
description:
  - Manage Kubernetes resources
version_added: "0.6.0"
options:
  api_version:
    description:
    - Use to specify the API version. If I(resource definition) is provided, the I(apiVersion) from the
      I(resource_definition) will override this option.
    default: v1
  kind:
    description:
    - Use to specify an object model. If I(resource definition) is provided, the I(kind) from a
      I(resource_definition) will override this option.
    required: true
  resource_name:
    description:
    - Fetch a specific object by name. If I(resource definition) is provided, the I(metadata.name) value
      from the I(resource_definition) will override this option.
  namespace:
    description:
    - Limit the objects returned to a specific namespace. If I(resource definition) is provided, the
      I(metadata.namespace) value from the I(resource_definition) will override this option.
  label_selector:
    description:
    - Additional labels to include in the query. Ignored when I(resource_name) is provided.
  field_selector:
    description:
    - Specific fields on which to query. Ignored when I(resource_name) is provided.
  kubectl:
    required: false
    default: null
    description:
    - The path to the kubectl binary
  host:
    description:
    - Provide a URL for accessing the API. Can also be specified via K8S_AUTH_HOST environment variable.
  log_level:
    required: false
    default: 0
    description:
    - Indicates the level of verbosity of logging by kubectl.
  kubeconfig:
    description:
    - Path to an existing Kubernetes config file. If not provided, and no other connection
      options are provided, the openshift client will attempt to load the default
      configuration file from I(~/.kube/config.json). Can also be specified via K8S_AUTH_KUBECONFIG environment
      variable.
requirements:
  - kubectl
author:
  - "Kenny Jones (@kenjones-cisco)"
  - "Jose Montoya (@jam01)"
"""

EXAMPLES = """
- name: test nginx is present
  kube: name=nginx resource=rc state=present

- name: test nginx is absent
  kube: name=nginx resource=rc state=absent

- name: test nginx is present
  kube: src=/tmp/nginx.yml

- name: test ansible namespace is present
  kube:
    state: present
    resource_definition:
      apiVersion: v1
      kind: Namespace
      metadata:
        name: ansible
"""

import os
import yaml

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import  string_types

from ansible_collections.ms3_inc.tavros.plugins.module_utils.kube_common import KubeBase

class KubeInfo(KubeBase):
    def __init__(self, module):
        self.module = module
        self._set_base_params(module.params)

    def _execute_module(self):
        kind = self.module.params.get('kind')
        name = self.module.params.get('name')
        namespace = self.module.params.get('namespace')
        api_version = self.module.params.get('api_version', 'v1')
        label_selector = self.module.params.get('label_selector')
        field_selector = self.module.params.get('field_selector')
        wait_sleep = self.module.params.get('wait_sleep')
        wait_timeout = self.module.params.get('wait_timeout')
        wait_condition = self.module.params.get('wait_condition')

        k8s_obj = self._get_resource(kind,
                        name=name,
                        api_version=api_version,
                        namespace=namespace,
                        label_selector=label_selector,
                        field_selector=field_selector)

        if k8s_obj is None:
            return []

        if not self.wait:
            if 'items' in k8s_obj:
                return k8s_obj.get('items')
            return [k8s_obj]

        resources = []
        condition_met = []

        if 'items' in k8s_obj:
            resources = k8s_obj.get('items')
        else:
            resources = [k8s_obj]

        for definition in resources:
            if definition is None:
                continue

            success, res, duration = self._wait(definition, wait_sleep, wait_timeout, condition=wait_condition)
            if not success:
                module.fail_json(msg="Failed to gather information about %s(s) even"
                                      " after waiting for %s seconds" % (res.get('kind'), duration))

            condition_met.append(res)

        return condition_met

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(),
            kubectl=dict(),
            kubeconfig=dict(),
            wait=dict(default=False, type='bool'),
            log_level=dict(default=0, type='int'),
            kind=dict(),
            name=dict(),
            namespace=dict(),
            api_version=dict(
                default='v1',
                aliases=['api', 'version'],
            ),
            wait_sleep=dict(default=5, type='int'),
            wait_timeout=dict(default=120, type='int'),
            wait_condition=dict(type='dict')
        )
    )

    manager = KubeInfo(module)
    module.exit_json(changed=False, resources=manager._execute_module())

def _exit(resources=[]):
    self.module.exit_json(changed=False, resources=resources)

if __name__ == '__main__':
    main()
