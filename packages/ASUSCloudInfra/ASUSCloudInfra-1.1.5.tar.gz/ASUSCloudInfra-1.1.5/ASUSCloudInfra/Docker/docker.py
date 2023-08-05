import subprocess
import platform


def supportDockerCmd():
    if platform.system().lower() == 'windows':
        print("windows isn't supported")
        return False
    elif platform.system().lower() == 'linux':
        return True
    else:
        print("unknow OS")
        return False

def login(url, account, password):
    if supportDockerCmd():
        cmd = "docker login " + url + " --username " + account + " --password " + password
        subprocess.call(cmd, shell=True)

def logout(url):
    if supportDockerCmd():
        cmd = "docker logout " + url
        subprocess.call(cmd, shell=True)

def pull(imagePath):
    if supportDockerCmd():
        cmd = "docker pull " + imagePath
        subprocess.call(cmd, shell=True)

def tag(oriImagePath, afterImagePath):
    if supportDockerCmd():
        cmd = "docker tag " + oriImagePath + " " + afterImagePath
        subprocess.call(cmd, shell=True)

def push(imagePath):
    if supportDockerCmd():
        cmd = "docker push " + imagePath
        subprocess.call(cmd, shell=True)