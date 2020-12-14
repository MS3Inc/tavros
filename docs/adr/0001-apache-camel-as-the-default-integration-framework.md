# Apache Camel as the Default Integration Framework

* Status: accepted
* Deciders: @k2merlinsix, @jam01, @mnorton
* Date: 2020-08

## Context and Problem Statement

What should be our main/default software framework for integration services?

## Decision Drivers <!-- optional -->

* Modern framework
* Low learning curve
* Maturity
* Solid documentation and community
* Cost

## Considered Options

* Spring Boot
* Spring Integration
* Apache Camel
* Python Flask
* Alpakka
* Go

## Decision Outcome

We'll use and extend Apache Camel as our default integration framework. Given the proficiency with Java and Enterprise Integration Patterns within our company and the industry in general, Apache Camel gives our customers a straight forward and low cost migration path from existing implementations.

### Positive Consequences <!-- optional -->

* Existing proficiency with Java and EIP
* Enables re-use of Maven based artifacts, e.g.: custom exceptions, domain classes, logging layouts, CI/CD pipelines
* Lower barrier for our customers finding professional resources

## Links <!-- optional -->

* [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)
* [Apache Camel](https://camel.apache.org/)
* [Spring Boot](https://spring.io/projects/spring-boot)
* [Spring Integration](https://spring.io/projects/spring-integration)
* [Alpakka](https://doc.akka.io/docs/alpakka/current/)
