from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: keycloak_client_roles

short_description: An extension to Ansible's keycloak_client specific to Client Roles

description:
    - The keycloak_client module does not allow for specifying client roles. This module extends
    that module with the ability to add client roles and client service account roles.

    - This module also extends Ansible's KeycloakAPI class to re-use its token and general client
    functionality.

    - See
    https://github.com/ansible-collections/community.general/blob/1.3.1/plugins/modules/identity/keycloak/keycloak_client.py
    and
    https://github.com/ansible-collections/community.general/blob/1.3.1/plugins/module_utils/identity/keycloak/keycloak.py

options:
    realm:
        description:
            - The realm to create the client in.
        type: str
        default: master
    client_id:
        description:
            - Client id of client to be worked on. This is usually an alphanumeric name chosen by
              you. Either this or I(id) is required. If you specify both, I(id) takes precedence.
              This is 'clientId' in the Keycloak REST API.
        aliases:
            - clientId
        type: str
    roles:
        description:
            - list of roles for this client. If the client roles referenced do not exist
              yet, they will be created.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - the name of the role to be created.
                type: str
    serviceAccountRoles:
        description:
            - the client's service account roles configuration.
        type: dict
        suboptions:
            clientRoles:
                description:
                    - the desired client's service account client roles
                    - the dict keys are the desired client role's clientId and the value is a list of dicts
                    that must have a 'name' key the desired client role name.
                type: dict
'''

import json

from ansible.utils.display import Display
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.general.plugins.module_utils.identity.keycloak.keycloak import \
    KeycloakAPI, camel, keycloak_argument_spec, get_token, KeycloakError, URL_CLIENT_ROLES

URL_USER_BY_USERNAME = "{url}/admin/realms/{realm}/users?username={username}"
URL_USER_CLIENT_ROLE_MAPPINGS = "{url}/admin/realms/{realm}/users/{id}/role-mappings/clients/{cid}"

def main():

    argument_spec = keycloak_argument_spec()
    meta_args = dict(
        client_id=dict(type='str', aliases=['clientId'], required=True),
        realm=dict(type='str', default='master'),
        roles=dict(type='list', elements='dict'),
        serviceAccountRoles=dict(type='dict')
    )

    argument_spec.update(meta_args)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    # Obtain access token, initialize API
    try:
        connection_header = get_token(
            base_url=module.params.get('auth_keycloak_url'),
            validate_certs=module.params.get('validate_certs'),
            auth_realm=module.params.get('auth_realm'),
            client_id=module.params.get('auth_client_id'),
            auth_username=module.params.get('auth_username'),
            auth_password=module.params.get('auth_password'),
            client_secret=module.params.get('auth_client_secret')
        )
    except KeycloakError as e:
        module.fail_json(msg=str(e))

    kcx = KeycloakAPIX(module, connection_header)

    realm = module.params.get('realm')
    client_id = module.params.get('client_id')
    cid = None

    before_client = kcx.get_client_by_clientid(client_id, realm=realm)
    if before_client is not None:
        cid = before_client['id']
    else:
        module.fail_json(msg=str('Client %s not found' % module.params.get('client_id')))

    desiredRoles = module.params.get('roles')
    if desiredRoles:
        existingRoles = map(lambda exRole: exRole['name'], kcx.get_client_roles(cid, realm))
        absentRoles = [item for item in desiredRoles if item['name'] not in existingRoles]
        for role in absentRoles:
            kcx.create_client_role(cid, role, realm)

    saRoles = module.params.get('serviceAccountRoles')
    if saRoles and saRoles['clientRoles']:
        kcx.add_client_sa_roles(cid, client_id, saRoles['clientRoles'], realm)

    result = dict(changed=True, msg='', diff={}, proposed={}, existing={}, end_state={})
    module.exit_json(**result)

# See:
# https://github.com/ansible-collections/community.general/blob/1.3.1/plugins/module_utils/identity/keycloak/keycloak.py
class KeycloakAPIX(KeycloakAPI):
    def create_client_role(self, id, roleRep, realm="master"):
        """ Add roles to a Keycloak client
        :param id: id (not clientId) of client where the roles are to be created
        :param roleRep: a RoleRepresentation to be created. Must contain at minimum the field name
        :param realm: realm of client where the roles are to be created
        :return: HTTPResponse object on success
        """

        client_roles_url = URL_CLIENT_ROLES.format(url=self.baseurl, realm=realm, id=id)
        try:
            return open_url(client_roles_url, method='POST', headers=self.restheaders,
                            data=json.dumps(roleRep), validate_certs=self.validate_certs)
        except Exception as e:
            self.module.fail_json(msg="Could not create roles in client %s in realm %s: %s"
                                      % (id, realm, str(e)), data=e.read().decode())

    def add_client_sa_roles(self, id, clientId, clientRoleReps, realm="master"):
        """ Add roles to a Keycloak client's service account
        :param id: id (not clientId) of client where the roles are to be created
        :param clientRoleReps: a map of clientIds (not the client's id) and RoleRepresentation to be created. Must contain at minimum the field name
        :param realm: realm of client where the roles are to be created
        :return: HTTPResponse object on success
        """

        user = self.get_user_by_username(("service-account-%s" % clientId), realm)
        for clientId in clientRoleReps:
            client = self.get_client_by_clientid(clientId, realm)
            clientRoles = self.get_client_roles(client['id'], realm)
            for roleRep in clientRoleReps[clientId]:
                # todo: throw if client doesn't have specifed role
                roleRep['id'] = list(filter(lambda role: role['name'] == roleRep['name'], clientRoles))[0]['id']

            self.create_user_client_role_mapping(user['id'], client['id'], clientRoleReps[clientId], realm)

    def get_client_roles(self, id, realm="master"):
        """ Retrieve a Keycloak client's roles
        :param id: id (not clientId) of client where the roles are to be created
        :param realm: realm of client where the roles are to be created
        :return: HTTPResponse object on success
        """
        client_roles_url = URL_CLIENT_ROLES.format(url=self.baseurl, realm=realm, id=id)
        try:
            return json.loads(to_native(open_url(client_roles_url, method='GET', headers=self.restheaders,
                                     validate_certs=self.validate_certs).read()))
        except Exception as e:
            self.module.fail_json(msg="Could not retrieve roles from client %s in realm %s: %s"
                                      % (id, realm, str(e)))

    def get_user_by_username(self, username, realm="master"):
      """ Retrieve an user by their username
      :param username: username to query by
      :return: dict with an user representation or None if none matching exist
      """

      user_by_username_url = URL_USER_BY_USERNAME.format(url=self.baseurl, realm=realm, username=username)
      try:
        r = json.loads(to_native(open_url(user_by_username_url, method='GET', headers=self.restheaders,
                                 validate_certs=self.validate_certs).read()))
        if len(r) > 0:
            return r[0]
        else:
            return None

      except Exception as e:
          self.module.fail_json(msg="Could not retrieve client %s in realm %s: %s"
                                    % (id, realm, str(e)))

    def create_user_client_role_mapping(self, id, cid, roleReps, realm="master"):
        """ Create a client role mappings for a given Keycloak user
        :param id: user id
        :param cid: client's id (not clientId) of client owner of the roles
        :param roleReps: a list of RoleRepresentation to be created. Must contain at minimum the field name and id
        :param realm: realm of client where the role mapping is to be created
        :return: HTTPResponse object on success
        """
        user_client_role_mapping_url = URL_USER_CLIENT_ROLE_MAPPINGS.format(url=self.baseurl, realm=realm, id=id, cid=cid)
        try:
            return open_url(user_client_role_mapping_url, method='POST', headers=self.restheaders,
                            data=json.dumps(roleReps), validate_certs=self.validate_certs)
        except Exception as e:
            self.module.fail_json(msg="Could not create roles mappings for user %s in realm %s: %s"
                                      % (id, realm, str(e)))


if __name__ == '__main__':
    main()
