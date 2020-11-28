Zeppelin
=========

This role installs Apache Zeppelin in the given node.

Requirements
------------

A Debian-based OS.

Role Variables
--------------

Variable | Description | Default
--- | --- | ---
zeppelin_version | Version of Zeppelin to install | 0.7.3
zeppelin_user | System user owner of the Zeppelin distribution (will be created) | hduser
zeppelin_group | System group owner of the Zeppelin distribution (will be created) | hadoop
zeppelin_spark_home | Home folder of the Spark installation in the node | /opt/spark
zeppelin_hadoop_home | Conf folder of the Hadoop installation in the node | /opt/hadoop
apache_dist_server | Apache mirror from where Spark is downloaded |  http://www-eu.apache.org/dist

Dependencies
------------

- Hadoop role
- Spark role

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

Apache
