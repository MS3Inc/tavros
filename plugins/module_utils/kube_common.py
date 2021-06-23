from __future__ import absolute_import, division, print_function
__metaclass__ = type

from datetime import datetime
import time
import yaml
import os
from subprocess import PIPE, run, CalledProcessError

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems, string_types
from ansible.module_utils._text import to_native, to_bytes, to_text
from ansible.module_utils.common.dict_transformations import dict_merge
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.module_utils.common.process import get_bin_path

class KubeBase(object):
    def _set_base_params(self, params):
        self.kubectl = params.get('kubectl')
        if self.kubectl is None:
            self.kubectl =  get_bin_path('kubectl')
        self.base_cmd = [self.kubectl]

        if params.get('host'):
            self.base_cmd.append('--server=' + params.get('host'))

        if params.get('log_level'):
            self.base_cmd.append('--v=' + str(params.get('log_level')))

        self.force = params.get('force')
        self.wait = params.get('wait')

    def _fail(self, msg=None, **kwargs):
        self.module.fail_json(msg=msg, **kwargs)

    def _get_resource(self, kind, name=None, api_version=None, namespace=None, label_selector=[], field_selector=[]):
        cmd = ['get', kind]

        if name:
            cmd.append(name)

        if namespace:
            cmd.append('--namespace=' + namespace)

        cmd.append('--output=yaml')

        result = self._execute(cmd, fail=False)
        if result is None:
            return None

        return dict(yaml.safe_load(result))

    def _wait_for(self, kind, name, namespace, predicate, sleep, timeout, state):
        start = datetime.now()

        def _wait_for_elapsed():
            return (datetime.now() - start).seconds

        response = None
        while _wait_for_elapsed() < timeout:
            response = self._get_resource(kind, name=name, namespace=namespace)

            if predicate(attr_dict(response)):
                if response:
                    return True, response, _wait_for_elapsed()
                return True, {}, _wait_for_elapsed()
            time.sleep(sleep)

        return False, response, _wait_for_elapsed()

    def _wait(self, definition, sleep=5, timeout=120, state='present', condition=None):

        def _deployment_ready(deployment):
            # FIXME: frustratingly bool(deployment.status) is True even if status is empty
            # Furthermore deployment.status.availableReplicas == deployment.status.replicas == None if status is empty
            # deployment.status.replicas is None is perfectly ok if desired replicas == 0
            # Scaling up means that we also need to check that we're not in a
            # situation where status.replicas == status.availableReplicas
            # but spec.replicas != status.replicas
            return (deployment.status
                    and deployment.spec.replicas == (deployment.status.replicas or 0)
                    and deployment.status.availableReplicas == deployment.status.replicas
                    and deployment.status.observedGeneration == deployment.metadata.generation
                    and not deployment.status.unavailableReplicas)

        def _pod_ready(pod):
            return (pod.status and pod.status.containerStatuses is not None
                    and all([container.get('ready') for container in pod.status.containerStatuses]))

        def _daemonset_ready(daemonset):
            return (daemonset.status and daemonset.status.desiredNumberScheduled is not None
                    and daemonset.status.numberReady == daemonset.status.desiredNumberScheduled
                    and daemonset.status.observedGeneration == daemonset.metadata.generation
                    and not daemonset.status.unavailableReplicas)

        def _service_ready(service):
            if not service.status:
                return False

            if service.spec.type != 'LoadBalancer':
                return True

            return (service.status.loadBalancer.ingress
                and all(ing.get('hostname') is not None or ing.get('ip') is not None for ing in service.status.loadBalancer.ingress))

        def _custom_condition(resource):
            if not resource.status or not resource.status.conditions or not all('type' in x for x in resource.status.conditions):
                return False
            match = [x for x in resource.status.conditions if x.get('type') == condition['type']]
            if not match:
                return False
            # There should never be more than one condition of a specific type
            match = attr_dict(match[0])
            if match.status == 'Unknown':
                if match.status == condition['status']:
                    if 'reason' not in condition:
                        return True
                    if condition['reason']:
                        return match.reason == condition['reason']
                return False
            status = True if match.status == 'True' else False
            if status == boolean(condition['status'], strict=False):
                if condition.get('reason'):
                    return match.reason == condition['reason']
                return True
            return False

        def _resource_absent(resource):
            return not resource

        waiter = dict(
            Deployment=_deployment_ready,
            DaemonSet=_daemonset_ready,
            Pod=_pod_ready,
            Service=_service_ready
        )

        kind = definition['kind']
        if state == 'present' and not condition:
            predicate = waiter.get(kind, lambda x: x)
        elif state == 'present' and condition:
            predicate = _custom_condition
        else:
            predicate = _resource_absent
        return self._wait_for(kind, definition['metadata']['name'], definition['metadata'].get('namespace'), predicate, sleep, timeout, state)

    def _load_resource_definitions(self, src):
        """ Load the requested src path """
        result = None
        path = os.path.normpath(src)
        if not os.path.exists(path):
            self._fail(msg="Error accessing {0}. Does the file exist?".format(path))
        try:
            with open(path, 'r') as f:
                result = list(yaml.safe_load_all(f))
        except (IOError, yaml.YAMLError) as exc:
            self._fail(msg="Error loading resource_definition: {0}".format(exc))
        return result

    def _execute(self, cmd, data=None, fail=True):
        args = self.base_cmd + cmd
        retries = 3
        retriable = [
                    # webhook errors seen with Kuma and cert-manage
                    "Error from server (InternalError)",
                    # CRDs not stable
                    "error: unable to recognize"
                ]

        while True:
            try:
                result = run(args, check=True, input=data, stderr=PIPE, stdout=PIPE, text=True)
                return result.stdout

            except CalledProcessError as err:
                if retries == 0 or not err.stderr.startswith(tuple(retriable)):
                    if not fail:
                        return None
                    else:
                        self._fail(
                            msg='error running kubectl (%s) command' % ' '.join(args),
                            rc=err.returncode,
                            stdout=err.stdout,
                            stderr=err.stderr
                        )
                else:
                    time.sleep(retries)
                    retries = retries - 1

class attr_dict(dict):
    def __getattr__(self, key):
        val = self.get(key)
        if isinstance(val, dict):
            return attr_dict(val)
        return val
