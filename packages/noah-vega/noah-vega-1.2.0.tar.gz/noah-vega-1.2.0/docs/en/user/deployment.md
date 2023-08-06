# Deployment Guide

## 1. Local cluster deployment

### 1.1 Deployment Preparations

The following conditions must be met when the Vega is deployed in a local cluster:

1. Ubuntu 18.04 or later (not tested in other Linux distributions and versions)
2. CUDA 10.0
3. Python 3.7
4. pip

Before deploying a cluster, you need to install some mandatory [software packages]. You can download the script [install_dependencies.sh](../../../deploy/install_dependencies.sh) and install them.

```bash
bash install_dependencies.sh
```

In addition, you need to install the MMDetection (optional, required by the object detection algorithm) and Horovod software separately. For details, see Appendix [Install MMDetection](#mmdetection) and [Install MPI](#MPI).

After the preceding software is installed on each host, you need to configure [SSH mutual trust](#ssh) and  build the [NFS](#nfs).

After the preceding operations are complete, download the vega deploy package from the Vega library. The deployment package contains the following scripts:

1. Deployment script: deploy_local_cluster.py
2. Commissioning script: verify_local_cluster.py
3. Start script on the slave node: start_slave_worker.py

### 1.2 Deployment

1. Configure the deployment information in the deploy.yml file. The file format is as follows:

    ```yaml
    master: n.n.n.n     # IP address of the master node
    listen_port: 8786   # listening port number
    slaves: ["n.n.n.n", "n.n.n.n", "n.n.n.n"]    # slave node address
    ```

2. Run the deployment script.

    Place deploy_local_cluster.py, verify_local_cluster.py, verga-1.0.0.whl, deploy.yml, and install_dependencies.sh in the same folder on the master node of the cluster. Run the following command to deploy Vega to the master and slave nodes:

    ```bash
    python deploy_local_cluster.py
    ```

    After the execution is complete, each node is automatically verified. The following information is displayed:

    ```text
    success.
    ```

## Reference

### <span id="mmdetection"> Install MMDetection </span>

1. Download the MMDetection source code.

    Download the latest version of the MMDetection from <https://github.com/open-mmlab/mmdetection>.

2. Installation

    Switch to the mmdetection directory and run the following commands to compile and install the MMDetection:

    ```bash
    sudo python3 setup.py develop
    ```

### <span id="MPI"> Install Horovod</span>


**Install MPI：**

1. Use the apt tool to install MPI directly

    ```bash
    sudo apt-get install mpi
    ```

2. Run the following commandes to check mpi is working.

    ```bash
    mpirun
    ```

### <span id="ssh"> Configure SSH mutual trust </span>

Any two hosts on the network must support SSH mutual trust. The configuration method is as follows:

1. Install SSH.
    `sudo apt-get install sshd`

2. Indicates the public key.
    `ssh-keygen -t rsa` two file id_rsa, id_rsa.pub will be create in folder ~/.ssh/, id_rsa.pub is public key.

3. Check the authorized_keys file in the directory. If the file does not exist, create it and run the chmod 600 ~/.ssh/authorized_keys command to change the permission.

4. Copy the public key id_rsa.pub to the authorized_keys file on other servers.

### <span id="nfs"> Building NFS </span>

On the server:

1. Install the NFS server.

    ```bash
    sudo apt install nfs-kernel-server
    ```

2. Write the shared path to the configuration file.

    ```bash
    sudo echo "/data *(rw,sync,no_subtree_check,no_root_squash)" >> /etc/exports
    ```

3. Create a shared directory.

    ```bash
    sudo mkdir -p /data
    ```

4. Restart the NFS server.

    ```bash
    sudo service nfs-kernel-server restart
    ```

On the Client:

1. Install the client tool.

    ```bash
    sudo apt install nfs-common
    ```

2. Creating a Local Mount Directory

    ```bash
    sudo mkdir -p /mnt/data
    ```

3. Mount the shared directory.

    ```bash
    sudo mount -t nfs <server ip>:/data /mnt/data
    ```
