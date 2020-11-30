Raspark
=========

This project contains a set of roles and an Ansible playbook to install a Spark cluster intended to be used against a Raspberry Pi cluster. This playbook allows you to select between Hadoop YARN and Spark Standalone cluster managers, setting a master node and an arbitrary number of workers. You can also decide whether to install an HDFS cluster or not in these nodes. In addition, it's possible to install a PostgreSQL database for testing and a Zeppelin server which you can use to issue jobs to the installed Spark cluster from a browser.

Motivations
------------

We are Datio, so we are a little nerds... Furthermore we wanted to demostrate that with a a little money we can build a Spark cluster.

Requirements
------------

As many Raspberry Pis as you want!!! (sorry, too obvious). We tested it with two Raspberry Pi 2 Model B and five Raspberry Pi 3 Model B. You will also need that the boards can see each other in a network (for instance using a switch), with an upstream Internet connection to download the required packages from their repositories.
> NOTE: you can use the playbook for any other machines with a Debian or Suse based OS, but you may need to tweak the configurations to support larger hardware than the present in a Raspberry Pi.

Inventory example: 
------------

The cluster topology is defined in the Inventory file. You can use the following as an example of how to configure the cluster:

```
  {{hostname-1}}   ansible_host={{ip1}} ansible_user={{os_user_rasp_1}} ansible_ssh_pass={{os_pass_rasp_1}} ansible_ssh_common_args='-o StrictHostKeyChecking=no'
  {{hostname-2}}   ansible_host={{ip2}} ansible_user={{os_user_rasp_2}} ansible_ssh_pass={{os_pass_rasp_2}} ansible_ssh_common_args='-o StrictHostKeyChecking=no'
  ...
  ...

  [masters:vars]
  hadoop_is_namenode={{true|false}}
  hadoop_is_resourcemanager={{true|false}}
  spark_is_master={{true|false}}

  [masters]
  hostname-1
  ...
  ...

  [workers:vars]
  hadoop_is_datanode={{true|false}}
  hadoop_is_nodemanager={{true|false}}
  spark_is_worker={{true|false}}

  [workers]
  hostname-2
  ...
  ...

  [postgresql]
  ...
  ...

  [zeppelin]
  ...
  ...

```

How to use:
------------

You can find more information in each role README, but we are going to do a little abstract for you:
  * Spark cluster using YARN cluster manager with HDFS

  ```
  [masters:vars]
  hadoop_is_namenode=true
  hadoop_is_resourcemanager=true
  spark_is_master=false

  [workers:vars]
  hadoop_is_datanode=true
  hadoop_is_nodemanager=true
  spark_is_worker=false
  ```

  * Spark cluster using Standalone cluster manager with HDFS

  ```
  [masters:vars]
  hadoop_is_namenode=true
  hadoop_is_resourcemanager=false
  spark_is_master=true

  [workers:vars]
  hadoop_is_datanode=true
  hadoop_is_nodemanager=false
  spark_is_worker=true
  ```

Licenses
-------

Apache, PostgreSQL
