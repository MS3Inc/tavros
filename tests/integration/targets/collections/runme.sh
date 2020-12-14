#!/usr/bin/env bash

set -eux

echo "--- validating docs"
# test documentation
ansible-doc ms3_inc.troubadour.kustomize

echo "--- validating provision playbook with default config"
PLAYBOOKS_PATH=$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ms3_inc/troubadour/playbooks

ansible-playbook $PLAYBOOKS_PATH/provision_playbook.yaml --extra-vars '{"cluster_name":"troubadour","cluster_domain":"example.com","cluster_admin_email":"ops@example.com"}' --extra-vars "@${PLAYBOOKS_PATH}/provision_playbook/default_vars.yaml" --tags all,dry-run
