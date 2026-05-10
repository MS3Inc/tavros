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

### Changed

- `phase0`: GitHub Actions in `ci.yml`, `ci-pr.yml`, and `ci-tag.yml` are now SHA-pinned to `actions/checkout@v4.3.0` and `dorny/paths-filter@v3.0.2`.
- `phase0`: Workflows now declare explicit `permissions` and use the built-in `GITHUB_TOKEN` to push to ghcr.io instead of a personal access token.
- `phase0`: `buildtools-build.sh` pins the installer base image to `fedora:40` and drops the `azure-cli-2.29.1-1.el7` version pin in favor of the current Microsoft repo package.
- `phase0`: README license badge now links to this repository's `LICENSE`.

### Fixed

- `phase0`: `ci-tag.yml` no longer mixes a GitHub expression with shell parameter expansion (`${{ GITHUB_REF#refs/tags/ }}`) — replaced with `${{ github.ref_name }}`.
- `phase0`: `buildtools-build.sh` and `update-default-vars.sh` quote variables to satisfy shellcheck.
