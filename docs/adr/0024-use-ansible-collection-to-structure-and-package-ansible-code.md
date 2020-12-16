# Use Ansible Collection to Structure and Package Ansible Code

* Status: accepted
* Deciders: @jam01
* Date: 2020-11

## Context and Problem Statement

How do we package multiple playbooks, plugins, and how do we distribute them when creating a customer's platform?

Designing pre-configured components and their extension points through Kustomizations is increasingly complex. Is there a way to simplify and make it more maintainable?

## Decision Drivers <!-- optional -->

* Maintainability of the code
* Easier to add customer configurability of components
* Support for distribution

## Considered Options

* Ansible Collection

## Decision Outcome

We'll use Ansible Collection structure and packaging for our Ansible code. We'll refactor the platform from multiple layers of Kustomizations to be entirely driven by an Ansible Collection. Ansible is migrating all their re-usable artifacts to be Collections so that seems to be where all support and tooling is to be found, including distribution from a git repository. Moving the component configuration and extension points to Ansible makes it much easier to structure and maintain, as well as add points of extension.

### Positive Consequences <!-- optional -->

* Higher maintainability as it's all Ansible
* Easier to add customer configurability as everything can be templated

### Negative Consequences <!-- optional -->

* A bit more complexity

## Links <!-- optional -->

* [Using Collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
* Blog [The Future of Ansible Content Delivery](https://www.ansible.com/blog/the-future-of-ansible-content-delivery)
* Blog [Hands on with Ansible collections](https://www.ansible.com/blog/hands-on-with-ansible-collections)
