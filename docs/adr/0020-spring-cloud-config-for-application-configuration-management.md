# Spring Cloud Config for Application Configuration Management

* Status: accepted
* Deciders: @jam01
* Date: 2020-11

## Context and Problem Statement

In a solid continuous delivery configuration an enterprise needs to manage application configuration properties independently of the application source code. What component should we use?

## Decision Drivers <!-- optional -->

* Flexible backend support
* Easy integration with Camel and Spring Boot

## Considered Options

* Spring Cloud Config

## Decision Outcome

We'll use spring cloud config as our application configuration manager. Spring cloud config is very simple to integrate since we chose Spring Boot as our base application framework. We'll use a Git backend from Gitea which will allow our customers to keep a history of changes and enable rollback.

### Positive Consequences <!-- optional -->

* Simple integration to Spring Boot

## Links <!-- optional -->

* [Spring Cloud Config](https://cloud.spring.io/spring-cloud-config/reference/html/)
