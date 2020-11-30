import os
from dotenv import load_dotenv
import paramiko
import time

load_dotenv()
remote_user = 'hduser'
remote_host = 'pi0'
remote_port = 22
ssh_key = os.getenv("ssh_key")
  
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(remote_host, port=remote_port, username=remote_user, key_filename=ssh_key)
transport = client.get_transport()
channel = client.invoke_shell()
stdin = channel.makefile('wb')
stdout = channel.makefile('rb')

stdin.write('''
cd
spark-submit --master yarn --deploy-mode cluster /opt/ls-cluster-v0.1/spark/db_conn.py
exit
''')
print(stdout.read())

stdout.close()
stdin.close()
client.close()


time.sleep(2)
