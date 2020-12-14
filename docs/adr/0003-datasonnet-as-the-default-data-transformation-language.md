# DataSonnet as the Default Data Transformation Language

* Status: accepted
* Deciders: @k2merlinsix, @jam01, @JakeMHughes
* Date: 2020-08

## Context and Problem Statement

Does DataSonnet, or can we make it, meet functional and performance requirements for modern integration workloads?

## Decision Drivers <!-- optional -->

* Provide the necessary transformation functions
* Performance

## Decision Outcome

We'll extend DataSonnet and use it as our default data transformation language. Extending ModusBox' work on top of DataBrick's sjsonnet project we delivered a feature-full and very performant language.

### Positive Consequences <!-- optional -->

* Joint ownership with ModusBox offers great visibility to our company and offerings
* Apache 2.0 License opens possibilities of adoption by the larger community or existing projects in the same space

### Negative Consequences <!-- optional -->

* Lead time to delivery of the next major release
* Responsibility of maintaining and stewarding the project with the community

## Links <!-- optional -->

* [DataSonnet Mapper Project](https://github.com/datasonnet/datasonnet-mapper)
* [DataSonnet](https://datasonnet.com/)
* [Jsonnet](https://jsonnet.org/)
* [sjsonnet Project](https://github.com/databricks/sjsonnet/)
