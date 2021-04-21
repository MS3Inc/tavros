# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#lookup-plugins
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: kube
    author: Jose Montoya <jmontoya@ms3-inc.com>
    version_added: "0.6.0"
    short_description: Lookup kubernetes resources
    description:
        - Lookup kubernetes resources
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
      host:
        description:
        - Provide a URL for accessing the API. Can also be specified via K8S_AUTH_HOST environment variable.
      kubeconfig:
        description:
        - Path to an existing Kubernetes config file. If not provided, and no other connection
          options are provided, the openshift client will attempt to load the default
          configuration file from I(~/.kube/config.json). Can also be specified via K8S_AUTH_KUBECONFIG environment
          variable.
"""
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ansible_collections.ms3_inc.tavros.plugins.module_utils.kube_common import KubeBase

import yaml

display = Display()

class KubeLookup(KubeBase):
    def __init__(self):
        self.kind = None
        self.name = None
        self.namespace = None
        self.api_version = None
        self.label_selector = None
        self.field_selector = None
        self.resource_definition = None

    def _fail(self, msg=None, **kwargs):
        raise AnsibleError(msg)

    def run(self, terms, variables=None, **kwargs):
        self._set_base_params(kwargs)

        self.kind = kwargs.get('kind')
        self.name = kwargs.get('resource_name')
        self.namespace = kwargs.get('namespace')
        self.api_version = kwargs.get('api_version', 'v1')
        self.label_selector = kwargs.get('label_selector')
        self.field_selector = kwargs.get('field_selector')

        resource_definition = kwargs.get('resource_definition')
        src = kwargs.get('src')
        if src:
            resource_definition = self.load_resource_definitions(src)[0]
        if resource_definition:
            self.kind = resource_definition.get('kind', self.kind)
            self.api_version = resource_definition.get('apiVersion', self.api_version)
            self.name = resource_definition.get('metadata', {}).get('name', self.name)
            self.namespace = resource_definition.get('metadata', {}).get('namespace', self.namespace)

        if not self.kind:
            raise AnsibleError(
                "Error: no Kind specified. Use the 'kind' parameter, or provide an object YAML configuration "
                "using the 'resource_definition' parameter."
            )

        k8s_obj = self._get_resource(self.kind,
                        name=self.name,
                        api_version=self.api_version,
                        namespace=self.namespace,
                        label_selector=self.label_selector,
                        field_selector=self.field_selector)

        if self.name:
            return [k8s_obj]

        return k8s_obj.get('items')


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        return KubeLookup().run(terms, variables=variables, **kwargs)
