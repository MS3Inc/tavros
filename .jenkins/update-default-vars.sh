#!/bin/bash
# Generate custom tavros yaml

# Exit if no argumetns were passed
if [ -z $1 ]; then
    exit
fi

i=1
for argument in "$@";  do
    key=${argument%=*}
    value=${argument#*=}
    if [ "$i" -eq 1 ]; then
        query="(.all.vars.$key = \"$value\")"
    else
        query="$query | (.all.vars.$key = \"$value\")"
    fi
    ((i++))
done

# Update default variables
yq e "$query" -i playbooks/provision_playbook/default_vars.yaml

