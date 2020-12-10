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
            args = ['kustomize', 'build']

            if self.reorder is not None:
                args.extend(['--reorder', self.reorder])

            args.append(term)

            # https://docs.python.org/3/library/subprocess.html#subprocess.run
            # https://github.com/painless-software/kustomize-wrapper/blob/master/kustomize/helpers/binaries.py
            try:
                result = run(args,
                         check=True,
                         input=None,
                         stderr=PIPE,
                         stdout=PIPE,
                         universal_newlines=True)

                manifests = yaml.load_all(result.stdout)
                ret.extend(manifests)
            except CalledProcessError as err:
                raise AnsibleError(err.stderr)

        return ret
