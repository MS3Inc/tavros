# Spring Boot as the Base Application Framework

* Status: accepted
* Deciders: @k2merlinsix, @jam01, @mnorton
* Date: 2020-08

## Context and Problem Statement

Should we add a base application framework to Apache Camel such as Spring Boot or Quarkus?

## Decision Drivers <!-- optional -->

* Speed up development
* Maturity
* Solid documentation and community

## Considered Options

* Spring Boot
* Quarkus

## Decision Outcome

We'll use Spring Boot as the base application framework to Apache Camel. We found that Spring Boot's auto-configuration features greatly speed up development time and it is well known and documented

### Positive Consequences <!-- optional -->

* Existing proficiency with Spring Boot as part of our internal bootcamp
* Access to a bigger ecosystem, e.g.: Spring Cloud Config

## Links <!-- optional -->

* [Spring Boot](https://spring.io/projects/spring-boot)
* [Quarkus](https://quarkus.io/)
