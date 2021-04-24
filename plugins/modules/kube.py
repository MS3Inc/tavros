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
  kubectl:
    required: false
    default: null
    description:
      - The path to the kubectl binary
  host:
    required: false
    default: null
    description:
      - The url for the API server that commands are executed against.
  force:
    required: false
    default: false
    description:
      - A flag to indicate to force delete, or apply.
  wait:
    required: false
    default: false
    description:
      - A flag to indicate to wait for resources to be created before continuing to the next step
  log_level:
    required: false
    default: 0
    description:
      - Indicates the level of verbosity of logging by kubectl.
  state:
    required: false
    choices: ['present', 'absent', 'latest', 'reloaded', 'stopped']
    default: present
    description:
      - present handles checking existence or creating if definition file provided,
        absent handles deleting resource(s) based on other options,
        latest handles creating or updating based on existence,
        reloaded handles updating resource(s) definition using definition file,
        stopped handles stopping resource(s) based on other options.
  resource_definition:
    description:
    - "Provide a YAML configuration for an object. NOTE: I(kind), I(api_version), I(resource_name),
      and I(namespace) will be overwritten by corresponding values found in the provided I(resource_definition)."
  src:
    description:
    - "Provide a path to a file containing a valid YAML definition of an object dated. Mutually
      exclusive with I(resource_definition). NOTE: I(kind), I(api_version), I(resource_name), and I(namespace)
      will be overwritten by corresponding values found in the configuration read in from the I(src) file."
    - Reads from the local file system. To read from the Ansible controller's file system, use the file lookup
      plugin or template lookup plugin, combined with the from_yaml filter, and pass the result to
      I(resource_definition). See Examples below.
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

class KubeManager(KubeBase):

    def __init__(self, module):
        self.module = module
        self._set_base_params(module.params)
        self._set_resource_definitions(module)

    def _set_resource_definitions(self, module):
        resource_definition = module.params.get('resource_definition')

        self.resource_definitions = []

        if resource_definition:
            if isinstance(resource_definition, string_types):
                try:
                    self.resource_definitions = yaml.safe_load_all(resource_definition)
                except (IOError, yaml.YAMLError) as exc:
                    self.fail(msg="Error loading resource_definition: {0}".format(exc))
            elif isinstance(resource_definition, list):
                self.resource_definitions = resource_definition
            else:
                self.resource_definitions = [resource_definition]

        src = module.params.get('src')
        if src:
            self.resource_definitions = self._load_resource_definitions(src)
        try:
            self.resource_definitions = [item for item in self.resource_definitions if item]
        except AttributeError:
            pass

    def apply(self):
        cmd = ['apply']

        if self.force:
            cmd.append('--force')

        if self.wait:
            cmd.append('--wait')

        cmd.extend(['-f', '-'])

        results = []

        wait_sleep = self.module.params.get('wait_sleep')
        wait_timeout = self.module.params.get('wait_timeout')
        wait_condition = self.module.params.get('wait_condition')

        for definition in self.resource_definitions:
            if definition is None:
                continue

            result = self._execute(cmd, yaml.dump(definition)).splitlines()

            if self.wait:
                success, res, duration = self._wait(definition, wait_sleep, wait_timeout, condition=wait_condition)
                if not success:
                    self.module.fail_json(msg="Resource apply timed out")

            results.extend(result)

        return results

def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type='path'),
            resource_definition=dict(type='dict', aliases=['definition']),
            host=dict(),
            kubectl=dict(),
            kubeconfig=dict(),
            force=dict(default=False, type='bool'),
            wait=dict(default=False, type='bool'),
            log_level=dict(default=0, type='int'),
            state=dict(default='present', choices=['present', 'absent']),
            wait_sleep=dict(default=5, type='int'),
            wait_timeout=dict(default=120, type='int'),
            wait_condition=dict(type='dict')
        ),
        mutually_exclusive=[('src', 'resource_definition')]
    )

    changed = False
    manager = KubeManager(module)
    state = module.params.get('state')

    if state == 'present':
        result = manager.apply()

    else:
        module.fail_json(msg='Unrecognized state %s.' % state)

    module.exit_json(changed=changed,
                     msg='success: %s' % (' '.join(result))
                     )

if __name__ == '__main__':
    main()
