# Troubadour as a Single Tenant Platform

* Status: accepted
* Deciders: @jam01
* Date: 2020-11

## Context and Problem Statement

A single platform for an indefinite amount of tenants would allow us to provide Troubadour in a cloud 'as-a-service' offering to our customers, instead of only as managed services. However, there is an unknown complexity and level of effort behind multi-tenancy.

## Decision Drivers <!-- optional -->

* Scope creep
* Speed of delivery
* Complexity

## Considered Options

* Build multi-tenancy from the ground up
* Automated single-tenant offered as PaaS

## Decision Outcome

We'll build Troubadour as a single tenant platform. The Ansible automation can be developed in a way that accommodates two modes of operation:

* Build a troubadour cluster to be owned by the client and optionally operated by us, as was the original objective
* Build a troubadour cluster to be owned and operated by us, transparently to the client.

The second mode allows us to offer a PaaS while keeping the platform simple.

### Positive Consequences <!-- optional -->

* Explicit separation to other clusters
* Simpler to build and consequently faster to deliver
* Can still offer as PaaS

### Negative Consequences <!-- optional -->

* May complicate day-2 operations on multiple clusters at once
