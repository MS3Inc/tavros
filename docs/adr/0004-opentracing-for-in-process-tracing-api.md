# OpenTracing for In-Process Tracing API

- Status: superseded by [ADR-0030](0030-opentelemetry-for-distributed-tracing.md)
- Deciders: @jam01
- Date: 2020-08

## Context and Problem Statement

Which in-process tracing API should we use, OpenTracing or the new project OpenTelemetry?

## Decision Drivers <!-- optional -->

- Existing library integrations

## Considered Options

- OpenTracing
- OpenTelemetry

## Decision Outcome

We'll use OpenTracing for in-process tracing API. Having contributed to the OpenTracing project, and refactoring the camel-opentracing component significantly, OpenTracing provides the most functionality now while OpenTelemetry's design stabilizes.

### Negative Consequences <!-- optional -->

- Will need to migrate to OpenTelemetry as it eventually deprecates OpenTracing

## Links <!-- optional -->

- Superseded by: [ADR-0030](0030-opentelemetry-for-distributed-tracing.md) — the migration this ADR
  anticipated under Negative Consequences has happened; Camel/Spring Boot applications now use
  `camel-opentelemetry-starter`.
- [OpenTracing](https://opentracing.io/)
- [OpenTelemetry](https://opentelemetry.io/)
