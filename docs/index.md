![alt text](https://www.ms3-inc.com/wp-content/uploads/2021/02/b.png)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/Kong/kong/blob/master/LICENSE)

# Tavros

Tavros is a cost-effective, cloud-native, and modular integration platform composed of best-of-breed, and seamlessly integrated open-source components.

## Ansible Collection

The objective of the `ms3_inc.tavros` Ansible Collection is to provide the necessary Ansible Playbooks to configure, provision, and manage the Tavros Kubernetes Cluster and supported components.

### Provision Playbook

The provision playbook provisions a Kubernetes cluster and configures Tavros's platform components, application environments, etc. All of the components are configurable through Ansible variables or the default configuration can be chosen. See the  [provision playbook's documentation](reference/playbooks/provision_playbook.md) for more information.

## Supported Platform Components

| Concern | Component | Version |
| ------- | --------- | ------- |
| Platform GitOps | Flux v2 | 0.10.0 |
| Platform GitOps | Sealed Secrets | 0.15.0 |
| API Gateway and Manager | Kong | 2.3.3 |
| API Portal | Kong Enterprise Edition | 2.3.3 |
| Service Mesh | Kuma | 1.2.0 |
| Identity and Access Management | Keycloak | 12.0.4 |
| Artifact Management | Nexus Repository Manager | 3.28.1 |
| Continuous Delivery | Jenkins | 2.277.4 |
| Observability | Elastic Cloud | 7.13.4 |
| Observability | Jaeger | 1.22.0 |
| Static Code Qualitative Analysis | Sonarqube | 8.5 |

## Roadmap

The Tavros team will maintain an up to date roadmap for major and minor releases through its [Milestones](https://github.com/MS3Inc/tavros/milestones).

For items that are not yet targeting a milestone, you can see our [Backlog](https://github.com/MS3Inc/tavros/issues?q=is%3Aopen+is%3Aissue+no%3Amilestone)

## Architectural Decision Log

This project documents significant architectural decisions in MADR, a lightweight format for recording architectural decisions in Markdown. See our [Architectural Decision Log](adr/index.md).
