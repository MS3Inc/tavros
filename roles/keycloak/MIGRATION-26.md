# Keycloak 19 → 26 Migration Plan

This role still targets the **legacy keycloak-operator** (`keycloak.org/v1alpha1` API group), pinned at the last stable release of that lineage (`19.0.3`). The full migration to Keycloak 26 has been deferred from `phase3` because it is a near-rewrite of the role — significantly larger than any other component upgrade in this phase.

## Why this isn't done in phase3

The Keycloak 17→20 transition replaced the WildFly-based legacy operator with a new Quarkus-based operator under a different API group:

| Aspect               | Legacy (≤19.x)                        | New (≥20.x)                                      |
| -------------------- | ------------------------------------- | ------------------------------------------------ |
| API group            | `keycloak.org/v1alpha1`               | `k8s.keycloak.org/v2alpha1`                      |
| `Keycloak` CRD       | exists                                | exists (different schema)                        |
| `KeycloakRealm` CRD  | exists                                | **removed**                                      |
| `KeycloakClient` CRD | exists                                | **removed**                                      |
| `KeycloakUser` CRD   | exists                                | **removed**                                      |
| `KeycloakBackup` CRD | exists                                | **removed**                                      |
| Realm bootstrap      | individual `KeycloakRealm` CRs        | declarative JSON inside `KeycloakRealmImport` CR |
| Admin env vars       | `KEYCLOAK_USER` / `KEYCLOAK_PASSWORD` | `KEYCLOAK_ADMIN` / `KEYCLOAK_ADMIN_PASSWORD`     |
| Distribution         | WildFly                               | Quarkus                                          |

Tavros currently uses every one of the removed CRDs (`KeycloakRealm`, `KeycloakClient`, `KeycloakUser`, `KeycloakBackup`) across many roles — gitea, jaeger, nexus, kong, jenkins, elastic_cloud all template `KeycloakClient` resources, and most of those also template `KeycloakUser` resources for service accounts. Every one of those templates needs to be replaced with declarative client configuration inside a single `KeycloakRealmImport` JSON document per realm.

## Migration steps (planned for a follow-up phase, e.g. `phase3.5` or `phase12-keycloak`)

1. **Operator install** — replace `roles/keycloak/files/operator/kustomization.yaml` with a reference to the official Keycloak 26 operator install bundle (`https://raw.githubusercontent.com/keycloak/keycloak-k8s-resources/26.x/kubernetes/kubernetes.yml`) plus the matching CRDs (`keycloaks.k8s.keycloak.org`, `keycloakrealmimports.k8s.keycloak.org`).
2. **Keycloak CR** — rewrite `roles/keycloak/files/keycloak.yaml` from the legacy schema to the new `k8s.keycloak.org/v2alpha1` `Keycloak` resource. Switch from the WildFly env vars to `KEYCLOAK_ADMIN` / `KEYCLOAK_ADMIN_PASSWORD`. Add explicit DB credentials (the new operator does not auto-provision Postgres).
3. **Realm bootstrap** — collapse all `roles/keycloak/templates/keycloakrealm.j2`, `keycloakclient-kubernetes.j2`, `keycloakuser-admin.j2` and their cross-role siblings (`gitea/templates/keycloakclient.j2`, `jaeger/templates/keycloakclient.j2`, etc.) into a single `KeycloakRealmImport` CR per realm. Per-component clients become `clients[]` entries inside that JSON; service accounts become `users[]` entries.
4. **Cross-role refactor** — every role that currently emits a `KeycloakClient` or `KeycloakUser` resource needs to instead contribute a fragment (Jinja partial or JSON snippet) that the keycloak role assembles into the realm import. Affected: `gitea`, `jaeger`, `nexus`, `kong_ee_sso`, `jenkins`, `elastic_cloud`.
5. **Plugin module** — `plugins/modules/keycloak_client_roles.py` calls the Keycloak admin REST API directly. The endpoints are stable across 19→26 but the access-token issuance changed (no more master-realm direct grant by default in 26). Re-test against 26.
6. **kong_ee_sso role** — currently bootstraps the Kong Enterprise admin SSO via the old `KeycloakClient` CRD. Needs to switch to the same realm-import path (or use the Keycloak admin API directly during provisioning).
7. **Acceptance tests** — `docs/AcceptanceTests.md` includes Keycloak login flows; rebuild against 26.

## Why we kept `19.0.3` pinned now

- The role still works as-is.
- All cross-role `KeycloakClient` / `KeycloakUser` templates remain valid until the realm-import refactor is done atomically — partial migration would leave the platform broken.
- Bumping to the last stable `19.x` patch (`19.0.3`) gets us the latest security fixes in that lineage with zero schema churn.

## Tracking

When this migration is undertaken, it gets its own branch (`modernization-phase-2026-keycloak-26` or similar) and ADR-0009 should be rewritten to reflect the new operator path.
