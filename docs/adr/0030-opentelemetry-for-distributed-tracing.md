# OpenTelemetry for Distributed Tracing

- Status: accepted
- Deciders: Tavros platform team, Redhawk architecture
- Date: 2026-08-28

Technical Story: Supersedes [ADR-0004](0004-opentracing-for-in-process-tracing-api.md). Recorded as
part of the CDX MOSA modernization, phase 5.

## Context and Problem Statement

[ADR-0004](0004-opentracing-for-in-process-tracing-api.md) chose OpenTracing over OpenTelemetry in
August 2020, on the reasoning that OpenTracing offered more functionality "while OpenTelemetry's
design stabilizes". It anticipated its own reversal, listing as a negative consequence: "Will need to
migrate to OpenTelemetry as it eventually deprecates OpenTracing."

That migration has already happened in practice. **This ADR records a decision that was made
implicitly; it does not propose a new one.** The October 2024 refresh of the Tavros Camel archetypes
moved generated projects to `camel-opentelemetry-starter` and the OpenTelemetry Java agent, and no
ADR was written at the time. The written record has been out of step with the platform for nearly two
years, and ADR-0004 has continued to state a position the code abandoned.

The immediate trigger for writing it down is the retirement of `tavros-camel-components`, the
repository holding Tavros's forks of `camel-tracing` and `camel-opentracing` at Camel 3.7.1 /
OpenTracing 0.33.0. Retiring that repository without superseding ADR-0004 would leave the decision
log pointing at components that no longer exist.

## Decision Drivers

- OpenTracing is archived. It merged into OpenTelemetry, which is now the CNCF-graduated standard
  and the API the ecosystem targets.
- Camel 4 ships first-party OpenTelemetry support (`camel-opentelemetry`,
  `camel-opentelemetry-starter`). The functionality gap that justified forking in 2020 is closed.
- The forked components publish into Camel's own package namespaces
  (`org.apache.camel.opentracing`, `org.apache.camel.tracing`), shadowing upstream classes wherever
  both are present. Carrying that forward is a maintenance and correctness liability.
- Maintaining forks of upstream Camel components means re-forking on every Camel upgrade. Platform
  upgrade cost should not scale with the number of components we have patched.
- Accreditation posture: an unmaintained tracing library with no upstream security response is a
  finding waiting to happen, and OpenTracing has had no releases since 2021.

## Considered Options

1. Adopt OpenTelemetry via Camel's first-party components, and retire the forks.
2. Keep the OpenTracing forks and port them forward to Camel 4.
3. Keep OpenTracing on Camel 3 and defer, running the integration tier a major version behind.

## Decision Outcome

Chosen option: **Option 1 — OpenTelemetry via Camel's first-party components**, because the
functional reason for the 2020 decision no longer exists, the platform already operates this way, and
it removes a fork whose maintenance cost recurs on every Camel upgrade.

Concretely:

- Camel/Spring Boot applications use `org.apache.camel.springboot:camel-opentelemetry-starter` plus
  the OpenTelemetry Java agent. Both Tavros Camel archetypes already configure this, so projects
  scaffolded from the archetypes need no change.
- `tavros-camel-components` is deprecated and its repository archived. The published artifact
  `com.ms3-inc.tavros:camel-components:3.7.1-002` remains on Maven Central for historical consumers;
  nothing is unpublished.
- ADR-0004 is marked superseded by this ADR.

### Positive Consequences

- Tracing comes from upstream Camel and is maintained there, not by us.
- No package-shadowing of upstream Camel classes.
- Platform upgrade cost decouples from the tracing layer — one fewer fork to carry per Camel release.
- Aligns with the wider observability direction: OTLP export feeds whichever backend the platform
  settles on, which is being re-evaluated separately (see the Elastic retirement discussion) rather
  than being fixed to Jaeger-on-Elasticsearch as [ADR-0017](0017-jaeger-for-tracing-with-elasticsearch-backend.md)
  assumes.

### Negative Consequences

- Any consumer still building against Camel 3.7.1 with the forked components must migrate to take
  further updates. The published artifact keeps them building, but it will not be patched.
- The OpenTelemetry Java agent version pinned in the archetypes (1.25.1) is itself behind current and
  needs its own uplift; adopting OpenTelemetry does not by itself make the instrumentation current.

## Links

- Supersedes: [ADR-0004](0004-opentracing-for-in-process-tracing-api.md)
- Related: [ADR-0017](0017-jaeger-for-tracing-with-elasticsearch-backend.md) — tracing backend, under
  separate re-evaluation
- [Camel OpenTelemetry component](https://camel.apache.org/components/current/others/opentelemetry.html)
- [OpenTelemetry](https://opentelemetry.io/)
- [OpenTracing — archived, merged into OpenTelemetry](https://opentracing.io/)
