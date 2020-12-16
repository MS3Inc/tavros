# Helm and Operators for Component Installation and Management

* Status: accepted
* Deciders: @jam01, @rmccright-ms3
* Date: 2020-11

## Context and Problem Statement

We're currently installing components ad-hoc through directly modified Kubernetes manifests from helm charts. This removes the ability to use Helm's upgrade features. This is done because we can't use Helm until Flux is up and running, and Flux depends on other components being installed before.

## Decision Drivers <!-- optional -->

* Ability to use Helm upgrades
* Minimize hand crafted manifests

## Considered Options

* Helm releases through Flux v2
* Operators

## Decision Outcome

We'll use Helm releases and Operators custom resources for component installation and management. Given that we're now using Flux v2 we can use their Helm release functionality before any Git repository is available, this way we can do Helm releases through Flux and eventually commit them to Git to enable GitOps from that point on. Kubernets Operators enable a higher level of component lifecycle management, these should always be preferred to Helm whenever available.

### Positive Consequences <!-- optional -->

* Upon provisioning the platform it will be entirely driven by GitOps
* Will be able to do component upgrades through Helm releases
* Less custom code by using official functionality as available

## Links <!-- optional -->

* [Helm](https://helm.sh/)
* [Operator Pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)
* [Operator Hub](https://operatorhub.io/)
* [Flux v2 Helm Controller](https://toolkit.fluxcd.io/components/helm/controller/)
