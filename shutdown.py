import ipyparallel as ipp
import spur
import time

c = ipp.Client(profile="brincolab-cluster")
c.shutdown(hub=True)

time.sleep(3)

shell = spur.SshShell(hostname="brincolab1", username="ipynode", private_key_file="/opt/ipynodekey/ipykey.pem", missing_host_key=spur.ssh.MissingHostKey.accept)
shell.run(["screen", "-X","-S", "ipyengines","quit"])
shell2 = spur.SshShell(hostname="brincolab2", username="ipynode", private_key_file="/opt/ipynodekey/ipykey.pem", missing_host_key=spur.ssh.MissingHostKey.accept)
shell2.run(["screen", "-X","-S", "ipyengines","quit"])
#c = ipp.Client(profile="brincolab-cluster")
#c.shutdown(hub=True)

