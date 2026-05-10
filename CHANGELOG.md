# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `phase0`: GitHub Actions lint workflow running yamllint, ansible-lint, shellcheck, and gitleaks on PR and main.
- `phase0`: Repo-root `.yamllint` and `.ansible-lint` configurations.
- `phase0`: Dependabot configuration covering GitHub Actions, pip, and Docker base images.
- `phase0`: `SECURITY.md`, `CONTRIBUTING.md`, `CODEOWNERS`, and this `CHANGELOG.md`.
- `phase1`: New `kops.networking` variable (default `cilium`) so users can override the CNI without editing role tasks.
- `phase2`: New `requirements.yml` mirroring `galaxy.yml` collection deps so contributors can run `ansible-galaxy collection install --force-with-deps -r requirements.yml`.

### Changed

- `phase0`: GitHub Actions in `ci.yml`, `ci-pr.yml`, and `ci-tag.yml` are now SHA-pinned to `actions/checkout@v4.3.0` and `dorny/paths-filter@v3.0.2`.
- `phase0`: Workflows now declare explicit `permissions` and use the built-in `GITHUB_TOKEN` to push to ghcr.io instead of a personal access token.
- `phase0`: `buildtools-build.sh` pins the installer base image to `fedora:40` and drops the `azure-cli-2.29.1-1.el7` version pin in favor of the current Microsoft repo package.
- `phase0`: README license badge now links to this repository's `LICENSE`.
- `phase1`: Default CNI for kOps clusters is now **Cilium** instead of Weave. Weave Net is unmaintained upstream as of 2024.
- `phase1`: kOps CLI flags `--master-count`, `--master-size`, `--master-zones` replaced with `--control-plane-count`, `--control-plane-size`, `--control-plane-zones`. The corresponding Ansible variables in `kops.*` were renamed to match.
- `phase1`: Default kOps node sizes bumped from `t2.large`/`t2.xlarge` to `t3.large`/`t3.xlarge` (current-generation burstable family).
- `phase1`: Collection dependency `community.kubernetes ==1.2.0` replaced with `kubernetes.core >=5.0.0,<6.0.0`. All role/plugin references updated. The `community.kubernetes` collection was renamed and retired upstream.
- `phase1`: `KUBECTL_VERSION` and `KOPS_VERSION` bumped to `1.30.0` in `buildtools-build.sh`.
- `phase2`: Tooling versions in `buildtools-build.sh` brought current — `KUBECTL_VERSION=1.32.0`, `FLUX_VERSION=2.4.0`, `KUSTOMIZE_VERSION=5.4.0`, `KUBESEAL_VERSION=0.27.0`, `YQ_VERSION=4.44.6`, `DECK_VERSION=1.40.0`. (`KOPS_VERSION` stays at `1.30.0` for now to track the K8s minor.)
- `phase2`: kubectl download URL switched from the deprecated `storage.googleapis.com/kubernetes-release/...` redirect to the canonical `dl.k8s.io/release/...`.
- `phase2`: kubeseal download switched to the new tarball-based release artifact (`kubeseal-${VER}-linux-amd64.tar.gz`); the legacy single-binary URL no longer exists for 0.27+.
- `phase2`: `flux install --version` bumped from `v0.41.2` to `v2.4.0` in `roles/fluxtoolkit`.
- `phase2`: Sealed Secrets controller manifest pin bumped from `v0.17.5` to `v0.27.0`.
- `phase2`: All Flux Toolkit CRD API versions migrated to GA — `kustomize.toolkit.fluxcd.io/v1`, `source.toolkit.fluxcd.io/v1`, `helm.toolkit.fluxcd.io/v2`, and `notification.toolkit.fluxcd.io/v1beta3` (still beta upstream). 25 files patched across `roles/`.
- `phase2`: Removed the deprecated `validation: client` field from every `flux-kustomization.j2` (the field was removed in `kustomize.toolkit.fluxcd.io/v1` GA; manifests are now validated server-side).
- `phase2`: `requirements.txt` — `ansible` requirement loosened from `==4.7.0` to `>=9.0,<11.0` (brings ansible-core ≥2.16). `boto` (Python 2 SDK, EOL) removed. `requests[security]` extra dropped (the extra was removed in `requests` 2.26).
- `phase2`: `galaxy.yml` collection ranges brought current — `amazon.aws >=8.0.0,<10.0.0`, `community.aws >=8.0.0,<10.0.0`, `community.general >=9.0.0,<11.0.0`, `azure.azcollection >=2.7.0,<4.0.0`. Added `community.crypto >=2.0.0` (already used transitively by the kops role's `community.crypto.openssh_keypair`).
- `phase3`: Nexus chart `nexus-repository-manager` bumped from `29.1.0` (Nexus 3.32.0) to `64.2.0` (Nexus 3.64.0). The Sonatype `helm3-charts` repo does not currently ship a chart matching the latest Nexus 3.84+; tracking that requires migrating to a different chart source in a future phase.
- `phase3`: Jenkins core image bumped from `jenkins/jenkins:2.416-jdk11` to `jenkins/jenkins:2.452.3-lts-jdk17`. **Java requirement bumped from 11 to 17** (required by Jenkins 2.426+). The `jenkins-operator` itself (currently `0.8.0-beta.2`) and the pinned plugin set in `roles/jenkins/files/jenkins.yaml` are intentionally left alone in this commit; plugin compatibility against 2.452 LTS should be re-validated in a follow-up before upgrading the operator.
- `phase3`: Kong Helm chart bumped from `2.15.0` to `2.52.0` (last 2.x line; the 3.x chart line is a future migration). Kong Enterprise image bumped from `kong/kong-gateway:3.0.0.0-alpine` to `kong/kong-gateway:3.9.1.1`. Kong AI plugins are now available on the gateway image but are not yet wired into any Tavros role — Phase 8 introduces a dedicated `ai-gateway` Kong instance that enables them.
- `phase3`: Kuma chart bumped from `2.4.3` to `2.13.5`. The legacy `Mesh` and `TrafficTrace` `kuma.io/v1alpha1` resources are still supported in 2.13. The new MeshTrafficPermission / MeshHTTPRoute shapes (introduced in Kuma 2.x) are additive and not adopted in this commit.
- `phase3`: Elastic stack version pin bumped from `7.13.4` to `8.15.3` across all 9 `elastic_cloud` manifests (Elasticsearch, Kibana, APM Server, Filebeat, Heartbeat, Metricbeat for kube-state-metrics, Metricbeat for node-exporter). **Breaking — Elastic 8.x has security enabled by default**: the auto-generated `<cluster-name>-es-elastic-user` Secret must be referenced when configuring Kibana, beats, and downstream consumers. Admins upgrading in place will need to coordinate the security migration per the [Elastic 7→8 upgrade guide](https://www.elastic.co/guide/en/elastic-stack/current/upgrading-elastic-stack.html). The role's existing keycloak-OIDC wiring may also require revalidation.
- `phase3`: Jaeger Operator manifest reference bumped from a vendored copy of `v1.47.0` (~27k lines) to a kustomize URL reference at `v1.62.0`. The vendored `roles/jaeger/files/operator/operator.yaml` was deleted; future bumps now require only a URL change. Jaeger v1 (`jaegertracing.io/v1` Jaeger CRD) is preserved in this commit. The OTel-native Jaeger v2 pivot is deferred to phase5, which adds the OpenTelemetry Collector that v2 expects as its input.
- `phase3`: `jaegertracing/jaeger-agent` image in the elastic_cloud daemonset bumped from `1.22.0` (2021) to `1.62.0`.

### Removed

- `phase1`: `openshift==0.11.2` Python dependency dropped. The library is deprecated; the `kubernetes` Python client (now pinned to `31.0.0`) is sufficient.
- `phase1`: All deprecated pre-Track-2 Azure SDK pins removed from `requirements.txt` (every `azure-mgmt-*` plus `azure-storage`, `msrest`, `msrestazure`, `azure-keyvault`, `azure-graphrbac`, `azure-nspkg`, `azure-cli-core`, `azure-common`). The `azure.azcollection` brings in current SDKs.

### Fixed

- `phase0`: `ci-tag.yml` no longer mixes a GitHub expression with shell parameter expansion (`${{ GITHUB_REF#refs/tags/ }}`) — replaced with `${{ github.ref_name }}`.
- `phase0`: `buildtools-build.sh` and `update-default-vars.sh` quote variables to satisfy shellcheck.

### Breaking

- `phase1`: Existing inventory files using `kops.master_count`, `kops.master_size`, `kops.master_zones` must be migrated to the `control_plane_*` names.
- `phase1`: Any out-of-tree role overrides referencing `community.kubernetes.*` modules or lookups must be updated to `kubernetes.core.*`.
- `phase1`: kOps clusters created on Tavros 0.6.x with Weave will continue to run, but new clusters default to Cilium. To preserve Weave on a new cluster, set `kops.networking: weave` (note: Weave Net is unmaintained).
- `phase2`: Flux Toolkit CRDs in any out-of-tree role overrides must be updated to the GA API versions. Existing installations will need a `flux install --version=v2.4.0 --upgrade` (or equivalent) before the new manifests are reconciled.
- `phase2`: `validation: client` on Kustomization CRs is silently ignored by Flux 2 GA but kept in this release's git history; remove it from any custom manifests when migrating.
