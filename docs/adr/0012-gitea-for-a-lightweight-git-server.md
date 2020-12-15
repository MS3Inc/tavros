# Gitea for a Lightweight Git Server

* Status: accepted
* Deciders: Mohammad Naeem, @jam01
* Date: 2020-09

## Context and Problem Statement

Given that Flux requires a Git repository to provide GitOps, and that our CI/CD pipelines will require the same for continuous delivery, what component should be our default/bundled Git server?

## Decision Drivers <!-- optional -->

* Lightweight as we expect a number of customers will already have a Git saas
* Easy to integrate

## Considered Options

* GitLab
* Gitea

## Decision Outcome

We'll use Gitea as our bundled and lightweight Git server. Gitea is more lightweight than the alternatives, and has the necessary APIs for us to integrate with.

### Negative Consequences <!-- optional -->

* No out of the box integration with Flux

## Links <!-- optional -->

* [Gitea](https://gitea.io/en-us/)
* [GitLab](https://about.gitlab.com/)
