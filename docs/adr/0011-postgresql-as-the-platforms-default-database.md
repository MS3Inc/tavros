# PostgreSQL as the Platform's Default Database

* Status: accepted
* Deciders: Mohammad Naeem
* Date: 2020-09

## Context and Problem Statement

Some components require a PostgreSQL database, how do we accommodate each one and future components?

## Decision Outcome

We'll use PostgreSQL as the platform's default database. Since Gitea and Keycloak require a PostgreSQL database we'll setup a single server and dynamically create what's needed for each component that uses PostgreSQL. If it's an option to use PostgreSQL for future components, we'll use that.

### Positive Consequences <!-- optional -->

* Single instance to backup, and restore in case of a disaster recovery
