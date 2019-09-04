import spur
import time


print("Starting ipynode connection")
shell = spur.SshShell(hostname="brincolab1", username="ipynode", private_key_file="/opt/ipynodekey/ipykey.pem", missing_host_key=spur.ssh.MissingHostKey.accept)
print("Starting ipycontroller")
result = shell.run(["screen", "-dmS", "ipycontroller" , "sh","/home/ipynode/ipynode/start_controller.sh"])
print("Waiting 3 seconds to start the engines")

time.sleep(3)
print("Starting engines on brincolab1")
result = shell.run(["screen", "-dmS", "ipyengines","bash","-c", "/home/ipynode/ipyengine/start_engine; exec bash"])

print("Waiting 3 seconds to start engines on bincolab2")
time.sleep(3)
print("Connecting to brincolab2")
shell2 = spur.SshShell(hostname="brincolab2", username="ipynode", private_key_file="/opt/ipynodekey/ipykey.pem", missing_host_key=spur.ssh.MissingHostKey.accept)
print("Starting engines on brincolab2")
shell2.run(["screen", "-dmS", "ipyengines","bash","-c", "/home/ipynode/ipyengine/start_engine; exec bash"])
print("Done")


