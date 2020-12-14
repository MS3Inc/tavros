# Troubadour

Troubadour is a cost-effective, cloud-native, and modular integration platform composed of best-of-breed, and seamlessly integrated open-source components.

## Ansible Collection - ms3_inc.troubadour

The objective of this Ansible Collection is to provide the necessary Ansible Playbooks to configure, provision, and manage the Troubadour Kubernetes Cluster and supported components.

### Provision Playbook

The provision playbook provisions a Kubernetes cluster and configures Troubadour's platform components, application environments, etc. All of the components are configurable through Ansible variables or the default configuration can chosen. See the provision playbook's [documentation](playbooks/provision_playbook/README.md) for more information.

## Supported Platform Components

| Concern | Component | Version | Since Trou. Version |
| ------- | --------- | ------- | ------------------ |
| Platform GitOps | Flux v2 | 0.4.3 | 0.1.0 |
| API Gateway and Manager | Kong | 2.2.0 | 0.1.0 |
| API Portal | Kong Enterprise Edition | 2.2.0 | 0.1.0 |
| Service Mesh | Kuma | 1.0.0 | 0.1.0 |
| Identity and Access Management | Keycloak | 11.0.2 | 0.1.0 |
| Application Artifact Management | Nexus Repository Manager | 3.28.1 | na |
| Continuous Delivery | Jenkins | 2.249.2 | na |
| Observability | Elastic Cloud | 7.9.3 | na |
| Observability | Jaeger | 1.20.0 | na |
| Static Code Qualitative Analysis | Sonarqube | 8.5 | na |

## Roadmap

na

## Architectural Decision Log

This project documents significant architectural decisions in MADR, a lightweight format for recording architectural decisions in Markdown. See our [Architectural Decision Log](docs/adr/index.md).
