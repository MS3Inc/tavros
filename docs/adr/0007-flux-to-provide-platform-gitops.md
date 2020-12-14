# Flux v2 Toolkit to Provide Platform GitOps

* Status: accepted
* Deciders: Mohammad Naeem, @jam01, @rmccright-ms3
* Date: 2020-09

## Context and Problem Statement

We want to enable continuous delivery of platform and application workloads in a GitOps way. What tools should we use?

## Decision Drivers <!-- optional -->

* Simplicity
* Integration with tools like Helm and Kustomize

## Considered Options

* Flux
* Flux v2 GitOps Toolkit
* Argo CD

## Decision Outcome

We'll use Flux v2 GitOps Toolkit to enable continuous delivery of the platform and application workloads. Having had experience with Flux v1 internally, along with the newer features of v2 while still maintaining a simple workflow, it's the more appropriate tool.

### Positive Consequences <!-- optional -->

* Flux v2 Custom Resource Definitions make it easy to utilize Flux Helm functionality before the source Git repository is up
* Alert features through integrations like Slack

### Negative Consequences <!-- optional -->

* Have to be careful with the 'chicken and egg problem' between Flux managing the platform, and provisioning platform components through Flux

## Links <!-- optional -->

* [GitOps Guide](https://www.weave.works/technologies/gitops/)
* [Flux v2 GitOps Toolkit](https://toolkit.fluxcd.io/)
* [Argo CD](https://argoproj.github.io/argo-cd/)
