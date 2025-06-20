# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#lookup-plugins
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
        lookup: kustomize
        author: Jose Montoya <jmontoya@ms3-inc.com>
        version_added: "0.1.0"
        short_description: build kustomization
        description:
            - This lookup returns the results of `kustomize build` on a given directory on the Ansible controller's file system.
        options:
          _terms:
            description: path(s) of directories to run kustomize on
            required: True
          reorder:
            description: Reorder the resources just before output. Use 'legacy' to apply a legacy reordering (Namespaces first, Webhooks last, etc). Use 'none' to suppress a final reordering. (default 'legacy')
            required: False
"""
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from subprocess import CalledProcessError, PIPE, run
import yaml

display = Display()

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        ret = []
        self.reorder = kwargs.get('reorder')

        for term in terms:
            display.debug("Kustomize lookup term: %s" % term)
            # See: https://github.com/fluxcd/flux2/discussions/1304#discussioncomment-638319
            args = ['kustomize', '--enable_kyaml=false', '--allow_id_changes=false', '--load_restrictor=LoadRestrictionsNone', 'build']

            if self.reorder is not None:
                args.extend(['--reorder', self.reorder])

            args.append(term)

            try:
                result = run(args, check=True, stderr=PIPE, stdout=PIPE)
                resources = yaml.safe_load_all(result.stdout)
                ret.extend(resources)

            except CalledProcessError as err:
                raise AnsibleError('error running kustomize (%s) command: %s' % (' '.join(args), err.stderr))

        return ret
