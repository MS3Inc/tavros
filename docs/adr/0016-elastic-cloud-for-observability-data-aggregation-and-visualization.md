# Elastic Cloud for Observability Data Aggregation and Visualization

* Status: accepted
* Deciders: @jam01, @k2merlinsix
* Date: 2020-10

## Context and Problem Statement

In a microservices architectural system observability is imperative, what components should we use for that?

## Decision Drivers <!-- optional -->

* Cost
* Feature set

## Considered Options

* Elastic Cloud
* Jaeger

## Decision Outcome

We'll use Elastic Cloud on Kubernetes for Observability Data Aggregation and Visualization. Elastic, Logstash and Kibana offer what we need for logging data. Aditionally, we can use APM server to get trace data from either Elastic's own apm agent or a Jaeger client.

### Positive Consequences <!-- optional -->

* A single pane of glass for observability
* Less components to coordinate

### Negative Consequences <!-- optional -->

* Valuable service dependency DAG only on license subscription

## Links <!-- optional -->

* [Elastic Cloud on Kubernetes](https://www.elastic.co/guide/en/cloud-on-k8s/1.3/index.html)
* [Elastic Stack Pricing](https://www.elastic.co/subscriptions)
* [Elastic with Jaeger](https://www.elastic.co/guide/en/apm/server/7.10/jaeger-reference.html)
* [ECK project](https://github.com/elastic/cloud-on-k8s/tree/master/)
* Follow up decision to use Jaeger for Tracing [ADR-0017](0017-jaeger-for-tracing-with-elasticsearch-backend.md)
