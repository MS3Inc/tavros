# Getting started with Tavros

## Prerequisites
### Choose a supported installation
Tavros is Kubernetes Native and will require Cluster access to provision the various components. You can utilize an existing Cluster or have Tavros provision a new one for you.

=== "Existing K8s"
    To install Tavros on an existing cluster it must meet the following requirements.

    - K8s 1.19,1.20,1.21
    - Has a default Storage Class 
    - Supports Service of Type Loadbalancer
    
=== "AKS"
    Tavros will provision an Azure Kubernetes Service with a provided Azure user. Then install your chosen components. 

    - You will need an Azure account with an available Subcription capable of provisioning AKS Clusters, DNS Zones, Resource Groups, and Storage Accounts on demand.
=== "AWS"
    Tavros will use KOps to provision K8s on Amazon Web Services. Then install your chosen components.

### Install a container runtime 
We provide a Tavros Collection image pre-installed with the latest version and required tooling. To utilize this you will need a Container Runtime such as [Docker](https://docs.docker.com/get-docker/) or [Podman](https://podman.io/getting-started/installation)

### Prepare a FQDN
Tavros requires a FQDN to be provided for its Root Domain. This allows the Gatway to expose deployed components via Sub Domains of the provided FQDN. DNS resolution for these various FQDNs will need to be configured for the corresponding IP of the Gateways LoadBalancer. 

> Note: If using a Cluster Provisioning Role such as `kops` or `aks` this will be configured for you. For installing to existing Clusters the DNS Role will output a list of DNS Records to be created manually durring Playbook execution. DNS Resolution is currently required for select components. Theirfor the DNS Role will wait for you to complete its setup in this case.

## Installation

### Pull the Tavros Collection
```
docker pull ghcr.io/ms3inc/tavros-collection
```

### Create a working directory
This folder will be used to provide your Tavros configuration files. The Tavros playbook will also use this directory to store provisoning logs, IAC, and credentials generated through the provisioning process.
```
mkdir tavros
cd tavros
```

### Configure an Inventory
Tavros is designed to use an Ansible Inventory for configuration. This file specifies custom settings for each component in Tavros. We provide a set of Inventores to choose from as a starting point.

> - Advanced users may want to customize further
  - Inventory files are documented in the [reference docs](/tavros/reference/playbooks/) for each Playbook. 
  
We'll create our config in the working directory and name it `{{ cluster_fqdn }}_vars.yaml`.
=== "Existing K8s"
    ``` yaml
    --8<-- "existing_standard_vars.yaml"
    ```

    1.  FQDN to be used for Tavros
    2.  Starting Admin user for Tavros

=== "AKS"
    ``` yaml
    --8<-- "aks_standard_vars.yaml"
    ```

    1.  FQDN to be used for Tavros
    2.  Starting Admin user for Tavros
    3.  Resrouce group previously created
    4.  Storage account created for tavros configs

=== "AWS"
    ``` yaml
    --8<-- "aws_standard_vars.yaml"
    ```

    1.  FQDN to be used for Tavros
    2.  Starting Admin user for Tavros

### Shell into a Tavros Collection instance
We'll mount our current directory into an interactive instance of the Tavros Collection.
```
docker run -it --rm -v $PWD:/tmp/ -w /tmp/ ghcr.io/ms3inc/tavros-collection:latest
```

### Complete Cluster Prerequisites
=== "Existing K8s"
    For existing clusters you will need to provide the Tavros Collection with K8s access. This is done by providing a Kube config at `~/.kube/config` in the instance. 

    #### Provide Kube Config
    You can do this by placing the config into the mounted working directory and then copying it to the correct location from the open bash shell.
    ```
    cp config ~/.kube/config
    ```

    Validate this is succesfull by using `kubectl`
    ```
    kubectl get nodes -o wide
    ```

=== "AKS"
    When using Tavros to provision Azure Kubernetes Services you will need to login from the Tavros Collection Instance and create a few Azure resources.
    #### Login to Azure

    This will redirect you and output your Tennant and Subscription info.
    ```
    az login
    ```

    #### Create Resource Group

    This resrouce group will be used to namespace the Azure resource used.
    ```
    az group create -n tavros-aks --location eastus
    ```
    #### Create Storage Account

    You'll also need to provide a storage location for your Tavros configuration.
    ```
    az storage account create -n <tavros-storage> -g tavros-aks
    ```
    #### Create DNS Zone
    The DNS Zone will be used to map your FQDN to the IPs of your configured Gateways.
    ```
    az network dns zone create -n az.ms3-inc.com -g tavros-aks 
    ```
    
=== "AWS"
    KOps Kubernetes on Amazon Web Services
    #### IAM

    For Tavros cluster on AWS, IAM should be configured as follows:
    ``` bash
    #!/bin/bash
    aws iam create-group --group-name tavros-provisioner
    ​
    # required for kops
    # https://github.com/kubernetes/kops/blob/master/docs/getting_started/aws.md#setup-iam-user
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess --group-name tavros-provisioner
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonRoute53FullAccess --group-name tavros-provisioner
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --group-name tavros-provisioner
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/IAMFullAccess --group-name tavros-provisioner
    aws iam attach-group-policy --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess --group-name tavros-provisioner
    ​
    aws iam create-user --user-name tavros-ci
    aws iam add-user-to-group --user-name tavros-ci --group-name tavros-provisioner
    aws iam create-access-key --user-name tavros-ci
    ```

    The resulting Access Key and Secret should be passed to the Ansible Playbook.

    For more detailed information see https://kops.sigs.k8s.io/getting_started/aws/

    #### Route53

    Route53 should manage the domain to be used for the cluster as a Hosted Zone. It is not necessary for Route53 to serve as the root domain registrar. For more information see [Configuring Amazon Route 53 as your DNS service](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring.html).

    For more detailed information see https://kops.sigs.k8s.io/getting_started/aws/

    
### Run Tavros
You can dry run first to make sure there are no issues with the Templeting phase
```
ansible-playbook ms3_inc.tavros.provision_playbook.yaml -i <inventory> --tags all,dry-run | tee $(date '+%s')_tavros_dryrun.log
```
Provision the Tavros Cluster by removing the `dry-run` tag.  
```
ansible-playbook ms3_inc.tavros.provision_playbook.yaml -i <inventory> --tags all | tee $(date '+%s')_tavros.log
```
Optionaly you can use Staging Lets Encrypt certs by adding the `test-run` tag.  
```
ansible-playbook ms3_inc.tavros.provision_playbook.yaml -i <inventory> --tags all | tee $(date '+%s')_tavros_testrun.log
```

#### Track install progress

From here you can see the progress of the Tavros Playbook in the Tavros Collection stdout.

You can also use `kubectl` to observe the progress. https://kubernetes.io/docs/tasks/tools/#kubectl

Other tools such as `k9s` are useful for monitoring progress and interacting with the cluster. https://github.com/derailed/k9s