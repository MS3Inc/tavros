# Contributing to Tavros

## Branches

- `main` is the integration branch. Direct pushes are not accepted; open a pull request.
- Modernization work uses the `modernization-phase-N` branch convention (one branch per phase, see `docs/modernization/ROADMAP.md` if you have local access to the planning docs).
- Feature and fix branches use `feat/<short-description>` or `fix/<short-description>`. Documentation-only changes use `docs/<short-description>`.

## Commit messages

We follow a lightweight conventional style:

- `phaseN: <imperative summary>` for modernization phase commits.
- `feat: <imperative summary>` for new functionality.
- `fix: <imperative summary>` for bug fixes.
- `docs: <imperative summary>` for documentation-only changes.
- `chore: <imperative summary>` for tooling, CI, dependency, or repo-hygiene changes.

Subject lines stay under 72 characters and are written in the imperative ("add role for X", not "added" or "adds"). Wrap body text at 100 characters. Reference issues with `Fixes #123` where applicable.

## Local checks

Before opening a PR, run the same checks CI will:

```bash
yamllint --strict .
ansible-lint
shellcheck .github/workflows/*.sh .jenkins/*.sh
```

To run the integration tests locally:

```bash
make install test
```

`make install` builds the collection tarball and installs it into `~/.ansible/collections`. `make test` runs `ansible-test integration` against the installed collection.

## Pull requests

- Keep each PR focused on a single phase or topic; do not bundle unrelated changes.
- Update `CHANGELOG.md` under `## [Unreleased]`.
- Update relevant ADRs in `docs/adr/` when you change an architectural decision.
- Update default vars and the JSON schema (`playbooks/provision_playbook/{default_vars.yaml,vars_schema.yaml}`) when you add or change configuration.
