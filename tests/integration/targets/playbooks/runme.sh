#!/usr/bin/env bash

set -eux

echo "--- validating docs"
# test documentation
ansible-doc ms3_inc.tavros.kustomize

PLAYBOOKS_PATH=$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ms3_inc/tavros/playbooks

echo "--- validating provision playbook with default config"

rm -rf /tmp/example.com/*
ansible-playbook $PLAYBOOKS_PATH/provision_playbook.yaml --extra-vars '{"cluster_name":"tavros","cluster_domain":"example.com","cluster_admin_email":"ops@example.com"}' --inventory "./provision_playbook/default_vars.yaml" --tags all,dry-run
diff --recursive --exclude='.DS_Store' /tmp/example.com/ ./provision_playbook/example.com/

echo "--- validating provision playbook with kong ee config"

rm -rf /tmp/enterprise-example.com/*
ansible-playbook $PLAYBOOKS_PATH/provision_playbook.yaml --extra-vars '{"cluster_name":"tavros","cluster_domain":"enterprise-example.com","cluster_admin_email":"ops@example.com"}' --inventory "./provision_playbook/kong_ee_vars.yaml" --tags all,dry-run
diff --recursive --exclude='.DS_Store' --exclude='ee-session-secret.yaml' --exclude='*.gitkeep' /tmp/enterprise-example.com/ ./provision_playbook/enterprise-example.com/
