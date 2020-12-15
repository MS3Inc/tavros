# Jaeger for Tracing with Elasticsearch Backend

* Status: accepted
* Deciders: @jam01
* Date: 2020-10

## Context and Problem Statement

In a microservices architectural system observability is imperative, and Elastic Stack Open Source does not offer service dependency DAG. Can/should we fill in that feature with another component?

## Decision Drivers <!-- optional -->

* Cost
* Feature set

## Considered Options

* Elastic Stack
* Jaeger

## Decision Outcome

We'll use Jaeger by default for tracing data, with Elasticsearch as the backend. Using Jaeger enables a service DAG that's very valuable and using elasticsearch as the backend enables data aggregation and analysis in Kibana.

### Positive Consequences <!-- optional -->

* Value of the service DAG dependency graph
* Maintain the ability to cross reference logs and trace data in a single pane
* Jaeger has closer participation to OpenTracing/Telemetry projects than Elastic

### Negative Consequences <!-- optional -->

* Another integration point
* Must correlate logs and traces in Camel through MDC

## Links <!-- optional -->

* [Jaeger](https://www.jaegertracing.io/)
* [Elastic with Jaeger](https://www.elastic.co/guide/en/apm/server/7.10/jaeger-reference.html)
* [Jaeger Operator](https://www.jaegertracing.io/docs/1.20/operator/)
* Article [Jaeger Elasticsearch and Kibana](https://medium.com/jaegertracing/jaeger-elasticsearch-and-kibana-7ecb846137b6)
* Article [Distributed Tracing with Jaeger and the ELK Stack](https://logz.io/blog/jaeger-and-the-elk-stack/)
* Article [Exploring Jaeger traces with Elastic APM](https://www.elastic.co/blog/exploring-jaeger-traces-with-elastic-apm)
