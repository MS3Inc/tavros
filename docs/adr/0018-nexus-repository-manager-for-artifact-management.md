# Nexus Repository Manager for Artifact Management

* Status: accepted
* Deciders: @jam01, @k2merlinsix
* Date: 2020-10

## Context and Problem Statement

In a solid continuous delivery configuration an enterprise needs to have a history of application builds an ability to rollback deployments as necessary. What artifact manager component should we use?

## Decision Drivers <!-- optional -->

* Stability

## Considered Options

* Nexus Repository Manager
* JFrog Artifactory

## Decision Outcome

We'll use Nexus repository manager for artifact management. Sonatype is one of the main stewards/contributors of Maven and therefore their platform is one of the most mature. In order to deliver a best practices continuous delivery configuration we'll tie in Nexus into our CI/CD pipelines.

### Positive Consequences <!-- optional -->

* Available commercial support from Nexus

## Links <!-- optional -->

* [Nexus Repository Manager OSS](https://www.sonatype.com/nexus/repository-oss)
* [JFrog Artifactory](https://jfrog.com/artifactory/)
