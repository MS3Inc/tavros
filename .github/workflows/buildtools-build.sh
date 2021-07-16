#!/usr/bin/env bash

set -o nounset
set -o errexit

KUBECTL_VERSION=1.21

# https://github.com/fluxcd/kustomize-controller/blob/v0.10.0/go.mod#L34
# https://github.com/kubernetes-sigs/kustomize/blob/kustomize/v3.9.4/kustomize/go.mod#L11
FLUX_VERSION=0.10.0
KUSTOMIZE_VERSION=3.9.4

KUBESEAL_VERSION=0.15.0
KOPS_VERSION=1.21
YQ_VERSION=4.6.3
DECK_VERSION=1.5.1

function dnf_install {
  local packages=${1}
  export $(podman exec installer grep VERSION_ID /etc/os-release)

  podman exec installer bash -c "yum install --quiet -y ${packages} \
      --installroot /mnt/container --releasever $VERSION_ID \
      --setopt install_weak_deps=false --setopt tsflags=nodocs \
      --setopt override_install_langs=en_US.utf8 \
    && yum clean all -y --installroot /mnt/container --releasever $VERSION_ID
  rm -rf /mnt/container/var/cache/yum
  rm -rf /mnt/container/var/cache/dnf"
}

function pip_install {
  local packages=${1}

  podman exec installer bash -c "PYTHONUSERBASE=/mnt/container/usr/local \
    pip install --quiet --user --upgrade --ignore-installed --no-cache-dir ${packages}"
}

printf "\nCreating new container from scratch...\n"
container=$(buildah from scratch)
mount=$(buildah mount $container)

printf "\nSetting up installer container...\n"
podman run --detach --tty --name installer --volume ${mount}:/mnt/container:rw --volume $PWD:$PWD:Z --workdir $PWD fedora:latest

# Add Azure CLI DNF repository
# See: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=dnf
podman exec installer bash -c "rpm --import https://packages.microsoft.com/keys/microsoft.asc"
podman cp ./.github/workflows/azure-cli.repo installer:/etc/yum.repos.d/azure-cli.repo

podman exec installer bash -c "yum upgrade -y --quiet"
podman exec installer bash -c "yum install pip -y --quiet"

printf "\nInstalling tools with package manager...\n"
dnf_install "vi make curl telnet openssl bind-utils diffutils python awscli git jq azure-cli procps nano traceroute iputils iproute"

pip_install "-r requirements.txt"

printf "\nCleaning up installer container...\n"
podman stop installer
podman rm installer

printf "\nInstalling other tools...\n"
curl -sSL "https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl" -o /tmp/kubectl
chmod u+x /tmp/kubectl
buildah copy $container "/tmp/kubectl" /usr/local/bin/

curl -sSL0 "https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv${KUSTOMIZE_VERSION}/kustomize_v${KUSTOMIZE_VERSION}_linux_amd64.tar.gz" | tar -zx -C /tmp/
chmod +x /tmp/kustomize
buildah copy $container "/tmp/kustomize" /usr/local/bin/

curl -sSL "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION}/kubeseal-linux-amd64" -o /tmp/kubeseal
chmod u+x /tmp/kubeseal
buildah copy $container "/tmp/kubeseal" /usr/local/bin/

curl -sSL0 "https://github.com/fluxcd/flux2/releases/download/v${FLUX_VERSION}/flux_${FLUX_VERSION}_linux_amd64.tar.gz" | tar -zx -C /tmp/
chmod +x /tmp/flux
buildah copy $container "/tmp/flux" /usr/local/bin/

curl -sSL "https://github.com/kubernetes/kops/releases/download/v${KOPS_VERSION}/kops-linux-amd64" -o /tmp/kops
chmod +x /tmp/kops
buildah copy $container "/tmp/kops" /usr/local/bin/

curl -sSL "https://github.com/mikefarah/yq/releases/download/v${YQ_VERSION}/yq_linux_amd64" -o /tmp/yq
chmod +x /tmp/yq
buildah copy $container "/tmp/yq" /usr/local/bin/

curl -sSL0 "https://github.com/Kong/deck/releases/download/v${DECK_VERSION}/deck_${DECK_VERSION}_linux_amd64.tar.gz" | tar -zx -C /tmp/
chmod +x /tmp/deck
buildah copy $container "/tmp/deck" /usr/local/bin/

printf "\nCleaning up...\n"
buildah unmount $container

printf "\nCommitting...\n"
buildah config --cmd /bin/bash ${container}
buildah config --label name=tavros-buildtools ${container}
buildah commit --rm $container $IMAGE_TAG
