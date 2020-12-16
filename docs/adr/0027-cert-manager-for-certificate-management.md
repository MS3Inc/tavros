# cert-manager for Certificate Management

* Status: accepted
* Deciders: @jam01
* Date: 2020-11

## Context and Problem Statement

The platform will required TLS certificates to signed by well known CAs. What tool do we use for generate those certificates?

## Decision Drivers <!-- optional -->

* Automation, including rotation before expiration
* Cost

## Considered Options

* cert-manager

## Decision Outcome

We'll use cert-manager as our certificate manager. cert-manager is the best known certificate manager for Kubernetes, it will automatically generate certificates as they're request by Ingress TLS configuration and will automatically re-generate them before they expire. For CA we'll use Let's Encrypt which is free.

### Positive Consequences <!-- optional -->

* Automatic generation and re-generation

### Negative Consequences <!-- optional -->

* Let's Encrypt limit of 50 certificates per week

## Links <!-- optional -->

* [cert-manager](https://cert-manager.io/)
* [Securing Ingress Resources](https://cert-manager.io/docs/usage/ingress/)
* [ACME Issuers](https://cert-manager.io/docs/configuration/acme/#creating-a-basic-acme-issuer)
* [Let's Encrypt Docs](https://letsencrypt.org/docs/)
