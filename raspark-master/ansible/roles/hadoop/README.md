Hadoop (HDFS + YARN)
=========

This role allows to install a Hadoop distribution with HDFS and YARN as cluster
manager. It doesn't support HA, it can only handle one master.

Requirements
------------

A Debian or Suse based OS.

Role Variables
--------------

Variable | Description | Default
--- | --- | ---
hadoop_version | Version of Hadoop to install | 2.8.2
hadoop_user | System user owner of the Hadoop distribution (will be created) | hduser
hadoop_group | System group owner of the Hadoop distribution (will be created) | hadoop
hadoop_namenode | Hostname of the host which will act as HDFS namenode | localhost
hadoop_resourcemanager | Hostname of the host which will act as YARN resource manager | localhost
hadoop_nodemanager_port | Port that the YARN nodemanager uses in that node (node defined, to put a node manager together with a resource manager change the default value) | 8040
hadoop_is_namenode | If the node is a namenode (installs the service) | false
hadoop_is_datanode | If the node is a datanode (installs the service) | false
hadoop_is_resourcemanager | If the node is a resourcemanager (installs the service) | false
hadoop_is_nodemanager | If the node is a nodemanager (installs the service) | false
apache_dist_server | Apache mirror from where Hadoop is downloaded |  http://www-eu.apache.org/dist

Dependencies
------------

No dependencies

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: hadoop, hadoop_namenode: master, hadoop_resourcemanager: master }

License
-------

Apache

