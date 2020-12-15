# Architectural Decision Log

This log lists the architectural decisions for Troubadour.

<!-- adrlog -- Regenerate the content by using "adr-log -i". You can install it via "npm install -g adr-log" -->

- [ADR-0000](0000-prefer-proven-foss-components-with-optional-support-for-licensed-derivatives.md) - Prefer Proven FOSS Components with Optional Support for Licensed Derivatives
- [ADR-0001](0001-apache-camel-as-the-default-integration-framework.md) - Apache Camel as the Default Integration Framework
- [ADR-0002](0002-spring-boot-as-the-base-application-framework.md) - Spring Boot as the Base Application Framework
- [ADR-0003](0003-datasonnet-as-the-default-data-transformation-language.md) - DataSonnet as the Default Data Transformation Language
- [ADR-0004](0004-opentracing-for-in-process-tracing-api.md) - OpenTracing for In-Process Tracing API
- [ADR-0005](0005-kubernetes-as-the-computing-platform.md) - Kubernetes as the Computing Platform
- [ADR-0006](0006-kops-to-provision-a-kubernetes-cluster.md) - Kops to Provision a Kubernetes Cluster
- [ADR-0007](0007-flux-to-provide-platform-gitops.md) - Flux to Provide Platform GitOps
- [ADR-0008](0008-kubeseal-to-securely-manage-secrets-in-gitops.md) - Kubeseal to Securely Manage Secrets in GitOps
- [ADR-0009](0009-keycloak-for-indetity-and-access-management.md) - Keycloak for Indetity and Access Management
- [ADR-0010](0010-kong-as-kubernetes-ingress-and-api-gateway.md) - Kong as Kubernetes Ingress and API gateway
- [ADR-0011](0011-postgresql-as-the-platform's-default-database.md) - PostgreSQL as the Platform's Default Database
- [ADR-0012](0012-gitea-for-a-lightweight-git-server.md) - Gitea for a Lightweight Git Server
- [ADR-0013](0013-kuma-for-service-mesh.md) - Kuma for Service Mesh
- [ADR-0014](0014-jenkins-for-continuous-integration.md) - Jenkins for Continuous Integration
- [ADR-0015](0015-sonarqube-for-application-static-code-analysis.md) - Sonarqube for Application Static Code Analysis
- [ADR-0016](0016-elastic-cloud-for-observability-data-aggregation-and-visualization.md) - Elastic Cloud for Observability Data Aggregation and Visualization
- [ADR-0017](0017-jaeger-for-tracing-with-elasticsearch-backend.md) - Jaeger for Tracing with Elasticsearch Backend
- [ADR-0018](0018-nexus-repository-manager-for-artifact-management.md) - Nexus Repository Manager for Artifact Management
- [ADR-0019](0019-prefer-daemonsets-over-sidecars.md) - Prefer Daemonsets Over Sidecars
- [ADR-0020](0020-spring-cloud-config-for-application-configuration-management.md) - Spring Cloud Config for Application Configuration Management
- [ADR-0021](0021-prefer-kong-enterprise-edition.md) - Prefer Kong Enterprise Edition
- [ADR-0022](0022-use-ansible-as-the-provisioning-engine.md) - Use Ansible as the Provisioning Engine
- [ADR-0023](0023-helm-and-operators-for-component-installation-and-management.md) - Helm and Operators for Component Installation and Management
- [ADR-0024](0024-use-ansible-collection-to-structure-and-package-ansible-code.md) - Use Ansible Collection to Structure and Package Ansible Code
- [ADR-0025](0025-setup-sandbox-and-production-kuma-meshes-and-kong-ingress-controllers-by-default.md) - Setup Sandbox and Production Kuma Meshes and Kong Ingress Controllers by Default
- [ADR-0026](0026-setup-sandbox-and-production-keycloak-realms-by-default.md) - Setup Sandbox and Production Keycloak Realms by Default
- [ADR-0027](0027-cert-manager-for-certificate-management.md) - cert-manager for Certificate Management
- [ADR-0028](0028-use-markdown-architectural-decision-records.md) - Use Markdown Architectural Decision Records

<!-- adrlogstop -->

For new ADRs, please use [template.md](template.md) as basis.
More information on MADR is available at <https://adr.github.io/madr/>.
General information about architectural decision records is available at <https://adr.github.io/>.
