# Use Ansible as Provisioning Engine

* Status: accepted
* Deciders: Mohammad Naeem, @jam01
* Date: 2020-11

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to three sentences. You may want to articulate the problem in form of a question.]

## Decision Drivers <!-- optional -->

* Flexibility
* Maintainability

## Considered Options

* Bash
* Ansible

## Decision Outcome

We'll use Ansible as the provisioning engine. Ansible modules, variable handling, Jinja 2 templating, and Kubernetes module make it easier to install and configure components. Helm Charts use the same templating language, and the Operator SDK has support for Ansible, if we decide to build an Operator.

### Positive Consequences <!-- optional -->

* Ansible being a desired-state engine enables idempotency
* Simpler setup

### Negative Consequences <!-- optional -->

* A learning curve to Ansible, playbooks, roles, etc

## Links <!-- optional -->

* [Ansible](https://www.ansible.com/)
* [Kubernetes Ansible](https://docs.ansible.com/ansible/latest/collections/community/kubernetes/k8s_module.html)
* [Ansible Operator SDK](https://sdk.operatorframework.io/docs/building-operators/ansible/tutorial/)
