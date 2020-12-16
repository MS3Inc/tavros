# Setup Sandbox and Production Keycloak Realms

* Status: accepted
* Deciders: @jam01, @rmccright-ms3
* Date: 2020-11

## Context and Problem Statement

Keycloak enables separation of sets of users, groups, roles, etc. through Realms. Should we create separate realms by default, which ones?

## Decision Drivers <!-- optional -->

* Must reflect best practice configuration
* Segregate production from non-production workloads as much as possible
* Satisfy 'common' enterprise requirements

## Considered Options

* Leave single Master realm
* Create one production realm
* Create sandbox and production realms

## Decision Outcome

We'll create sandbox and production keycloak realms. Given the existing inclusion of sandbox and production concepts through service mesh and ingress controllers, these realms make a simple and easy to understand separation of users that allows customers to also test and promote identity and access management policies in a similar way to application workloads. We've seen enterprises do this with okta and okta preview instances for example.

### Positive Consequences <!-- optional -->

* Simple, easy to understand
* Enables identity and access management separation

### Negative Consequences <!-- optional -->

* May be unnecessary for some organizations

## Links <!-- optional -->

* [Keycloak Concetps](https://www.keycloak.org/docs/latest/server_admin/#core-concepts-and-terms)
