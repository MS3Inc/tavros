# Prefer Daemonsets over Sidecars

* Status: accepted
* Deciders: @jam01
* Date: 2020-11

## Context and Problem Statement

Kubernetes supports deploying workloads as daemonsets or sidecars. For example, when deploying Jaeger Agent for reporting trace data, in a DaemonSet strategy there will be a single Agent deployment in every Kubernetes node, so all applications' Jaeger Client in a single node share the same agent. Conversely, in a side-car strategy each application will have its own dedicated Jaeger Agent deployment, requiring extra resources.

Which should we favor for cross cutting concern deployments?

## Decision Drivers <!-- optional -->

* Cost

## Considered Options

* Sidecars
* Daemonsets

## Decision Outcome

We'll prefer daemonsets over sidecar deployments whenever there is the option. Given that Tavros is designed as a single tenant platform there are computing resource savings when using daemonsets (deployment per node) vs sidecars (deployment per service).

### Positive Consequences <!-- optional -->

* Less resource utilization

### Negative Consequences <!-- optional -->

* Would have to refactor in order to support multi-tenancy

## Links <!-- optional -->

* [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
* See about single tenancy in [ADR-0029](0029-tavros-as-a-single-tenant-platform.md)
