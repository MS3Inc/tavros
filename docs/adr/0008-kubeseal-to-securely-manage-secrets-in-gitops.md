# Kubeseal to Securely Manage Secrets in GitOps

* Status: accepted
* Deciders: @jam01, @rmccright-ms3
* Date: 2020-09

## Context and Problem Statement

In order to store secrets safely in a public or private Git repository, what tool do we use?

## Decision Drivers <!-- optional -->

* Simplicity
* Integration with Flux

## Decision Outcome

We'll use Bitnami's Sealed Secrets controller to securely manage secrets in GitOps. The sealed secrets can be decrypted only by the controller running in your cluster and nobody else can obtain the original secret, even if they have access to the Git repository.

## Links <!-- optional -->

* [Flux Sealed Secrets recommendation](https://toolkit.fluxcd.io/guides/sealed-secrets/)
* [Sealed Secrets project](https://github.com/bitnami-labs/sealed-secrets)
