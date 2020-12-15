# Kong as Kubernetes Ingress Controller and API Gateway

* Status: accepted
* Deciders: @k2merlinsix
* Date: 2020-08

## Context and Problem Statement

Which component should serve as our Kubernetes Ingress Controller, to do load balancing and proxying?

Which component should serve as our API Gateway? How easy is it to tie into the application networking of the Ingress Controller?

## Decision Drivers <!-- optional -->

* Network performance
* Feature set of API Gateway

## Considered Options

* NGINX
* Kong
* Apigee
* KrakenD

## Decision Outcome

Kong will be our Kubernetes Ingress Controller and API Gateway as well. Having a single component perform both functions should make it easier to maintain and more performant.

### Positive Consequences <!-- optional -->

* Enterprise Edition pricing is more cost effective than some alternatives

### Negative Consequences <!-- optional -->

* Lua as the main language for developing plugins

## Links <!-- optional -->

* [Kong](https://konghq.com/)
* [NGINX](https://nginx.org/en/)
* [Apigee](https://cloud.google.com/apigee/)
* [KrakenD](https://www.krakend.io/)
