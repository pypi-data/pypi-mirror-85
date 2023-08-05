#!/bin/bash

function install_nvidia_driver() {
    # Drivers
    apt-add-repository ppa:xorg-edgers/ppa -y
    add-apt-repository ppa:graphics-drivers -y
    apt-get update
    apt-get install -y nvidia-driver-410
    modprobe nvidia
    echo "Please restart the machine with '/sbin/shutdown -r now' at your earliest convinience"
}

function uninstall_old_nvidia() {
    if command -v docker >/dev/null 2>&1; then
        docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
    fi
    systemctl stop docker
    apt-get -y purge nvidia*
    #while [ $(lsmod | grep nvidia) ]; do
    lsmod | grep nvidia | awk '{ print $1; }' | xargs -r rmmod
    #done
}

function install_nvidia_docker() {
    if command -v nvidia-docker >/dev/null 2>&1; then
        nvidia-docker --version
    else
        curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
        wget -qO - https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | sudo apt-key add -
        distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
        curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
        apt-get update
        apt-get install -y nvidia-docker2
        systemctl restart containerd
        systemctl restart docker
    fi
    if cat /etc/docker/daemon.json | grep '"iptables": false'; then
        echo '{"runtimes": {"nvidia": {"path": "nvidia-container-runtime", "runtimeArgs": []}}, "iptables": false}' > /etc/docker/daemon.json
        systemctl restart docker
    fi
}


function install_nvidia() {
    if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1; then
        version=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | sed -e 's/\.[0-9]*//')
        if [ "$version" -ge 410 ]; then
            nvidia-smi
        else
            echo "Using NVIDIA driver verison $version incompatible with finetune"
            uninstall_old_nvidia
            install_nvidia_driver
        fi
    else
       echo "Command nvidia-smi not found"
       install_nvidia_driver
    fi
}

function install_main_packages() {
    apt update
    apt install -y snapd wget curl iptables python3 python3-pip postgresql-client jq
    iptables -P FORWARD ACCEPT
    iptables-save > /etc/iptables/rules.v4
    echo iptables-persistent iptables-persistent/autosave_v4 boolean true | debconf-set-selections
    echo iptables-persistent iptables-persistent/autosave_v6 boolean true | debconf-set-selections
    apt-get -y install iptables-persistent
    if command -v ufw >/dev/null 2>&1; then
        ufw default allow routed
    fi
    snap --help
    snap refresh
}
