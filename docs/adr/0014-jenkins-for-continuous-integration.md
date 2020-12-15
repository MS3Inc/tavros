# Jenkins for Continuous Integration

* Status: accepted
* Deciders: @jam01
* Date: 2020-09

## Context and Problem Statement

We'll be using Flux for continuous deployment, leaving us to choose a component for continuous delivery, i.e.: building and running tests against artifacts before deploying.

## Decision Drivers <!-- optional -->

* Existing proficiency and pipelines
* Simplicity

## Considered Options

* Jenkins
* Jenkins X
* Tekton

## Decision Outcome

We'll use Jenkins as our CI component. Since we're using Flux for deployment we don't need too Kubernetes specific features like Jenkins X has, and Jenkins can support for complex pipelines than Tekton.

### Positive Consequences <!-- optional -->

* Can re-use existing pipelines with little modification

### Negative Consequences <!-- optional -->

* Less 'modern' than other options

## Links <!-- optional -->

* [Jenkins X](https://jenkins-x.io/)
* [Jenkins](https://www.jenkins.io/)
* [Tekton Project](https://github.com/tektoncd)
