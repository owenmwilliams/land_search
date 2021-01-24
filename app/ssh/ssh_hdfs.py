import os
from dotenv import load_dotenv
import paramiko
import time
import io
import main
from ssh.connect import ssh_postgres as sshp

def sh_hdfs(api_gateway):
    try:
        version, transport, channel, stdin, stdout = sshp()

        stdin.write("""
        cd /opt/ls-cluster-{0}/models
        python3 -c 'import main; x = main.hdfs_dl({1}); print(x)'
        exit
        """.format(version, api_gateway))
        x = stdout.read()
        print(x)

    except Exception as e:
        print('An error occured downloading the files from API: %s' % e)
