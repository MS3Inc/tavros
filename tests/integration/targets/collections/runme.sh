#!/usr/bin/env bash

set -eux

echo "--- validating docs"
# test documentation
ansible-doc ms3_inc.troubadour.kustomize

echo "--- validating default collection"
ansible-playbook $ANSIBLE_COLLECTIONS_PATH/ansible_collections/ms3_inc/troubadour/playbooks/default_playbook.yaml --tags all,dry-run
