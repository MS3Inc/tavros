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
