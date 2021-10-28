# Tavros Provision Playbook
## Configuration Variables

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
cluster_name | String | **Required** The name of the Tavros Kubernetes cluster
cluster_domain | String | **Required** The domain name to use for the platform. This should be managed by the cloud provider chosen in order to setup routes and certificates
cluster_admin_email | String | **Required** The email for alerts and general notifications. |
kubernetes_cluster | [Kubernetes Cluster Object](#kubernetes-cluster-object) | **Required** Configuration for the Kubernetes Cluster to be provisioned
kong | [Kong Object](#kong-object) | Configuration for Kong
kuma | [Kuma Object](#kuma-object) | Configuration for Kuma
namespaces | [[Namespace Object](#namespace-object)] | An array of Namespace configurations
keycloak | [Keycloak Object](#keycloak-object) | Configuration for Keycloak

### Kubernetes Cluster Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
cloud | String | The cloud provider to provision the cluster in | 'aws'
master_count | Integer | The number of master nodes | 3
master_size | String | The machine instance type for master nodes | 'T2.Large'
node_count | Integer | The number of worker nodes | 2
node_size | String | The machine instance type for worker nodes | 'T2.XLarge'
zones | String | A comma separated list of availability zones in which to place the machines | 'us-east-1,us-east-2'
state_bucket | String | The name of the S3 bucket to place the cluster state in | 'troubaodur'
ssh_public_key | String | The SSH public key to setup as authorized user on provisioned machines | _read from ~/.ssh/id_rsa.pub_
aws_access_key_id | String | The AWS IAM AccessKeyId | _uses aws cli logged in user_
aws_secret_access_key | The AWS IAM SecretAccessKey | _uses aws cli logged in user_
keycloak | [Kubernetes Cluster Keycloak Object](#kubernetes-cluster-keycloak-object) | Keycloak Config | { "realm": "", "client_secret": "" }

### Kubernetes Cluster Keycloak Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
realm | String | Keycloak Realm Name | 
client_secret | String | Client Secret | 

### Kong Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
default_ingress_class | String | The default ingress controller class for other components to use | 'prod'
ee_creds | [[Kong EE Credentials Object](#kong-ee-credentials-object)] | An array of Kong Enterprise Edition Credentials available for Kong instances to use |
instances | [[Kong Instance Object](#kong-instance-object)] | An array of Kong instance object to be configured |

### Kong EE Credentials Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
license | String | **Required** The Enterprise Edition license |
name | String | **Required** Identifier for EE Kong Instance |

### Kong Instance Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
name | String | **Required** The name of the Kong instance |
hybrid | Boolean | **Required** Deployment Type |
ingress_class | String | **Required**  The name of the ingress class |
kuma_mesh_name | String | The name of the Kuma mesh that the Kong instance should be part of |
ee | [Kong Instance EE Object](#kong-instance-ee-object) | The EE configuration for the Kong instance |

### Kong Instance EE Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to use Enterprise Edition | false
creds | String | The name of the Kong EE Credentials resource to use | 'default'
keycloak | [Kong Keycloak Object](#kong-keycloak-object) | Keycloak Config | { "realm": "", "client_secret": "" }

### Kong Keycloak Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
realm | String | Keycloak Realm Name | 
client_secret | String | Client Secret | 


### Kuma Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
meshes | [[Kuma Mesh Object](#kuma-mesh-object)] | The Kuma mesh configuration object |

### Kuma Mesh Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
name | String | **Required** The name of the Kuma mesh |
mtls | [Kuma mTLS Object](#kuma-mtls-object) | The mTLS configuration for the Kuma mesh |

### Kuma mTLS Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to enable mTLS | false

### Namespace Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
name | String | **Required** The name of the Namespace |
kuma_mesh_name | String | The name of the Kuma mesh this namespace should be a part of |

### Keycloak Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to use Keycloak | true
realms | Array of [Keycloak Realms Object](#keycloak-realms-object) | Enumeration of Desired Realms | [{"name": "sandbox"}, {"name": "prod"}]

### Keycloak Realms Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
name | Boolean | Whether to use Keycloak | 

### Nexus Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to use Elastic Cloud | true
keycloak | [Nexus Keycloak Object](#nexus-keycloak-object) | Keycloak Config | { "realm": "", "client_secret": "" }

### Nexus Keycloak Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
realm | String | Keycloak Realm Name | 
client_secret | String | Client Secret | 

### Elastic Cloud Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to use Elastic Cloud | true
ee | [Elastic Cloud EE Object](#elastic-cloud-ee-object) | EE Config | { "enabled": false }

### Elastic Cloud EE Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to use EE | 
trial | Boolean | Whether to use 30 day cluster trial license | 
licnese | String | License JSON | 
keycloak | [Elastic Cloud Keycloak Object](#elastic-cloud-keycloak-object) | Keycloak Config | { "realm": "", "client_secret": "" }

### Elastic Cloud Keycloak Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
realm | String | Keycloak Realm Name | 
client_secret | String | Client Secret | 


### Gitea Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to use Gitea | true

### Jaeger Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to use Jaeger | true
keycloak | [Jaeger Keycloak Object](#jaeger-keycloak-object) | Keycloak Config | { "realm": "", "client_secret": "" }

### Jaeger Keycloak Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
realm | String | Keycloak Realm Name | 
client_secret | String | Client Secret | 

### Jenkins Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
enabled | Boolean | Whether to use Jenkins | true
keycloak | [Jenkins Keycloak Object](#jenkins-keycloak-object) | Keycloak Config | { "realm": "" }

### Jenkins Keycloak Object

| Field Name | Type | Description | Default Value |
| ---------- | ---- | ----------- | ------------- |
realm | String | Keycloak Realm Name | 

