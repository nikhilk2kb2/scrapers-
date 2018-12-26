# In order to run this script, you will be required to install aws cli
# Install for Linux : https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-linux.html
# Install for MacOS : https://docs.aws.amazon.com/cli/latest/userguide/cli-install-macos.html
# Install for Windows : https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html

# You will also be required to connect AWS CLI to your account 
# To do that follow the instructions mentioned here : https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

import os, json, pprint, time  

def getAllHigherInstance():
    output = os.popen('aws ec2 describe-instances --filters "Name=instance-type,Values=h1.2xlarge, h1.4xlarge, h1.8xlarge,' + 
    ' h1.16xlarge, i3.large, i3.xlarge, i3.2xlarge, i3.4xlarge, i3.8xlarge, i3.16xlarge, i3.metal, d2.xlarge, d2.2xlarge,' + 
    ' d2.4xlarge, d2.8xlarge"').read()

    outputObj = json.loads(output)
    pprint.pprint(outputObj)
    return outputObj

def startInstance(InstanceId):
    output = os.popen("aws ec2 start-instances --instance-ids " + str(InstanceId)).read()
    print(output)


def stopInstance(InstanceId):
    output = os.popen("aws ec2 stop-instances --instance-ids " + str(InstanceId)).read()
    print(output)

print("What function you need to perform?")
print("1) Get all Higher Instances\n2) Start Instance\n3) Stop Instance\n")

answer = int(raw_input("Enter the option number: "))
print

if(answer == 1):
    getAllHigherInstance()

if(answer == 2):
    instanceId = raw_input("Please input the instance ID for which the instance has to be started: ")
    startInstance(instanceId)

if(answer == 3):
    instanceId = raw_input("Please input the instance ID for which the instance has to be stopped: ")
    stopInstance(instanceId)