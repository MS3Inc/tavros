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
    def _fail(self, msg=None, **kwargs):
        raise AnsibleError(msg)

    def run(self, terms, variables=None, **kwargs):
        self._set_base_params(kwargs)

        kind = kwargs.get('kind')
        name = kwargs.get('resource_name')
        namespace = kwargs.get('namespace')
        api_version = kwargs.get('api_version', 'v1')
        label_selector = kwargs.get('label_selector')
        field_selector = kwargs.get('field_selector')

        if not kind:
            raise AnsibleError(
                "Error: no Kind specified. Use the 'kind' parameter, or provide an object YAML configuration "
                "using the 'resource_definition' parameter."
            )

        k8s_obj = self._get_resource(kind,
                        name=name,
                        api_version=api_version,
                        namespace=namespace,
                        label_selector=label_selector,
                        field_selector=field_selector)

        if k8s_obj is None:
            return None

        if name:
            return [k8s_obj]

        return k8s_obj.get('items')


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        return KubeLookup().run(terms, variables=variables, **kwargs)
