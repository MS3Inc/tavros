![alt text](https://www.ms3-inc.com/wp-content/uploads/2021/02/b.png)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# Tavros

Tavros is a cost-effective, cloud-native, and modular integration platform composed of best-of-breed, and seamlessly integrated open-source components.

## Ansible Collection - ms3_inc.tavros

The objective of this Ansible Collection is to provide the necessary Ansible Playbooks to configure, provision, and manage the Tavros Kubernetes Cluster and supported components.

### Provision Playbook

The provision playbook provisions a Kubernetes cluster and configures Tavros's platform components, application environments, etc. All of the components are configurable through Ansible variables or the default configuration can be chosen. See the provision playbook's [documentation](playbooks/provision_playbook/README.md) for more information.

## Supported Platform Components

Versions below reflect what the Ansible collection provisions as of the modernization phases 0–3. Where a component is installed via a Helm chart, the chart version is noted in parentheses next to the product version.

| Concern                          | Component                | Version               |
| -------------------------------- | ------------------------ | --------------------- |
| Container Orchestration          | Kubernetes               | 1.32                  |
| Cluster Provisioning             | kOps                     | 1.30                  |
| Cluster Networking (CNI)         | Cilium                   | kOps-managed          |
| Platform GitOps                  | Flux v2                  | 2.4.0                 |
| Secret Management                | Sealed Secrets           | 0.27.0                |
| Certificate Management           | cert-manager             | 1.11.0                |
| API Gateway and Manager          | Kong                     | 3.9 (chart 2.52.0)    |
| API Portal                       | Kong Enterprise Edition  | 3.9.1.1               |
| Service Mesh                     | Kuma                     | 2.13.5                |
| Identity and Access Management   | Keycloak                 | 19.0.3 [^keycloak]    |
| Default Database                 | PostgreSQL               | Bitnami chart 10.3.17 |
| Git Server                       | Gitea                    | chart 2.2.4           |
| Artifact Management              | Nexus Repository Manager | 3.64.0 (chart 64.2.0) |
| Continuous Delivery              | Jenkins                  | 2.452.3 LTS (JDK 17)  |
| Observability                    | Elastic Cloud            | 8.15.3                |
| Observability                    | Jaeger                   | 1.62.0                |
| Static Code Qualitative Analysis | SonarQube                | Planned [^sonarqube]  |

[^keycloak]: Pinned to the last stable release of the legacy `keycloak.org/v1alpha1` operator lineage. The migration to Keycloak 26 (the Quarkus-based `k8s.keycloak.org/v2alpha1` operator) is planned for a dedicated follow-up phase; see [`roles/keycloak/MIGRATION-26.md`](roles/keycloak/MIGRATION-26.md).

[^sonarqube]: SonarQube is an intended platform component (see [ADR-0015](docs/adr/0015-sonarqube-for-application-static-code-analysis.md)) but is not yet automated by a role in the provision playbook.

## Roadmap

The Tavros team will maintain an up to date roadmap for major and minor releases through its [Milestones](https://github.com/MS3Inc/tavros/milestones).

For items that are not yet targeting a milestone, you can see our [Backlog](https://github.com/MS3Inc/tavros/issues?q=is%3Aopen+is%3Aissue+no%3Amilestone)

## Architectural Decision Log

This project documents significant architectural decisions in MADR, a lightweight format for recording architectural decisions in Markdown. See our [Architectural Decision Log](docs/adr/index.md).

## Acceptance Tests

See the [acceptance tests](docs/AcceptanceTests.md) for verifying cluster functionality out of the box.

## DNS Cache

Subsequent Tavros re installs will cause your DNS Cache to be invalid and prevent Hosts from being resolved for various API calls. You can flush the Cache diffferently based on your system. Below are some common examples:

Mac:

```bash
# Newer MacOs
sudo killall -HUP mDNSResponder

#10.11 and 10.9
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

#10.10
sudo discoveryutil mdnsflushcache
sudo discoveryutil udnsflushcaches

#10.6 and 10.5
sudo dscacheutil -flushcache
```

Linux

```bash
# If using Systemd Resolved
sudo systemd-resolve --flush-caches

# Or if using DNSMasq
sudo service dnsmasq restart

# OR IF USING Nscd
sudo service nscd restart
```
