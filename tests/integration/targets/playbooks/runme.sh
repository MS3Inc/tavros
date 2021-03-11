#!/usr/bin/env bash

set -eux

echo "--- validating docs"
# test documentation
ansible-doc ms3_inc.tavros.kustomize

PLAYBOOKS_PATH=$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ms3_inc/tavros/playbooks

echo "--- validating provision playbook with default config"

rm -rf /tmp/tavros.example.com/*
ansible-playbook $PLAYBOOKS_PATH/provision_playbook.yaml --extra-vars '{"cluster_fqdn":"tavros.example.com","cluster_admin_email":"ops@example.com"}' --inventory "./provision_playbook/default_vars.yaml" --skip-tags requires_cluster
diff --recursive /tmp/tavros.example.com/ ./provision_playbook/example.com/

echo "--- validating provision playbook with kong ee config"

rm -rf /tmp/tavros.enterprise-example.com/*
ansible-playbook $PLAYBOOKS_PATH/provision_playbook.yaml --extra-vars '{"cluster_fqdn":"tavros.enterprise-example.com","cluster_admin_email":"ops@example.com"}' --inventory "./provision_playbook/kong_ee_vars.yaml" --skip-tags requires_cluster
diff --recursive --exclude='secret-ee-admin-gui-session.yaml' --exclude='*.gitkeep' /tmp/tavros.enterprise-example.com/ ./provision_playbook/enterprise-example.com/
