import os
from dotenv import load_dotenv
import paramiko
import time
import io
import main
from ssh.connect import ssh_in

def sh_hdfs(api_gateway):
    try:
        version, transport, channel, stdin, stdout = ssh_in('hduser')

        stdin.write("""
        cd /opt/ls-cluster-{0}/models
        python3 -c 'import main; x = main.hdfs_dl("{1}"); print(x)'
        exit
        """.format(version, api_gateway))
        
        # x = stdout.read()
        # print(x)

        while True:
            line = stdout.readline()
            if not line:
                break
            elif line.strip().startswith('*****'):
                while not line.strip().startswith('#####'):
                    line = stdout.readline()
                    print(line.rstrip())
                print('_________________________________________________________')

    except Exception as e:
        print('An error occured downloading the files from API: %s' % e)
