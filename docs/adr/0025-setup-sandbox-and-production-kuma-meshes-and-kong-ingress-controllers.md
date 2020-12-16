# Setup Sandbox and Production Kuma Meshes and Kong Ingress Controllers

* Status: accepted
* Deciders: @jam01, @rmccright-ms3
* Date: 2020-11

## Context and Problem Statement

What should be our default service mesh and application environments look like? Given that we'll enable mutual TLS on the meshes, each mesh will require a Kong Ingress Controller which in turn requires a Load Balancer from the cloud provider.

## Decision Drivers <!-- optional -->

* Must reflect best practice configuration
* Segregate production from non-production workloads as much as possible
* Satisfy 'common' enterprise requirements
* Cost

## Considered Options

* One dev, one test, and one production environment, all segregated through Kuma meshes
* Dev and test environments separated by kuma meshes in one cluster, production in another
* Dev and test environments in one 'sandbox' kuma mesh, production in a 'production' mesh

## Decision Outcome

We'll setup a Sandbox and Production Kuma mesh, sandbox will have a dev and test namespaced environment, and production will have the production namespaced environment. The service mesh and mutual TLS plugin enforces the segregation of non-production (aka sandbox) environments and the production environment to where we don't fuctionally need a separate cluster. Moreover aggregating dev and test into a sandbox mesh saves us provisioning a load balancer for each environment, so we could support any arbitrary environment configuration needs.

### Positive Consequences <!-- optional -->

* Reduced cost of extra load balancer
* Reduced complexity of dedicated cluster

### Negative Consequences <!-- optional -->

* Learning curve of service mesh mutual TLS enforcement
* Sandboxed environments can still communicate with each other

## Links <!-- optional -->

* [Kuma mTLS](https://kuma.io/docs/1.0.3/policies/mutual-tls/#usage-of-builtin-ca)
* [Kuma Gateway](https://kuma.io/docs/1.0.3/documentation/dps-and-data-model/#gateway)
