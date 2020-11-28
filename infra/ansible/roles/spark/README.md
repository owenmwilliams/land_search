Spark
=========

This role allows to install Spark in the target nodes, including an option to
deploy a Spark Standalone cluster with one master.

Requirements
------------

A Debian or Suse based OS.

Role Variables
--------------

Variable | Description | Default
--- | --- | ---
spark_version | Version of Spark to install | 2.2.0
spark_user | System user owner of the Spark distribution (will be created) | hduser
spark_group | System group owner of the Spark distribution (will be created) | hadoop
spark_standalone_cluster | Whether to install an standalone cluster or not | false
spark_master | Hostname of the host which will act as Spark standalone master | localhost
spark_is_master | If the node is a Spark standalone master (installs the service) | false
spark_is_worker | If the node is a Spark standalone worker (installs the service) | false
spark_hadoop_conf | Hadoop configuration folder | /opt/hadoop/etc/hadoop
apache_dist_server | Apache mirror from where Spark is downloaded |  http://www-eu.apache.org/dist

Dependencies
------------

No dependencies.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: spark }

License
-------

Apache
