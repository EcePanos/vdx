import sys
import docker
import subprocess
import os
import shutil
from docker import errors
from distutils.dir_util import copy_tree
import collect
import yaml
from yaml.loader import SafeLoader


DOCKER_SOCKET_PATH = '/var/run/docker.sock'
OUTPUT_UID = 1000
docker_client = docker.from_env()

dirname = os.path.dirname(__file__)
INPUT_TEMP = os.path.join(dirname, 'input')
os.makedirs(INPUT_TEMP, exist_ok=True)
OUTPUT_TEMP = os.path.join(dirname, 'output')
os.makedirs(OUTPUT_TEMP, exist_ok=True)
#USER = config['WORKING_ENVIRONMENT']['USER']

def empty(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def chown_output(uid, dir):
    # spawn a busybox with output repo mounted to adjust the file permissions
    docker_client.containers.run("busybox:latest",
                            volumes={dir: {'bind': '/usr/src/app/data'}},
                            command=["/bin/sh", "-c", f"chown -R {uid}:{uid} /usr/src/app/data && sleep 1"],
                            auto_remove=True
                            )

def pipeline_run(image, input_dir, output_dir, env, cmd, docker_socket, input_mount, output_mount):
    print(f"Running image {image} with input_dir {input_dir} and output_dir {output_dir}")
    _volumes = {output_dir: {'bind': output_mount}}
    # bind docker sock if tool config requires it
    if docker_socket:
        _volumes[DOCKER_SOCKET_PATH] = {'bind': DOCKER_SOCKET_PATH}
    if input_dir is not None:
        _volumes[input_dir] = {'bind': input_mount}
    # execute actual tool image with provided settings
    try:
        docker_client.containers.run(image,
                                volumes=_volumes,
                                network='host',
                                environment=env,
                                command=cmd,
                                auto_remove=True
                                )
    except errors.ImageNotFound:
        print(f"[Error] Container image {image} not found!")
        return {"error": f"container image {image} not found!"}
    print("Done")
    print("Correcting ownership of pipeline step output ...")
    chown_output(OUTPUT_UID, output_dir)
    return {"image_used": image, "output_dir": output_dir}

def branch_retrieve(dataset, branches, votes):
    print(dataset, branches)

    for branch in branches:
        subprocess.run(f"git clone --single-branch --branch {branch} {dataset} work/{branch}", shell=True)
    collect.consensus('work', votes)
    subprocess.run(f"git clone {dataset} main", shell=True)
    copy_tree('result', 'main')
    old_wd = os.getcwd()
    os.chdir(f'{old_wd}/main')
    subprocess.run(f"git add .", shell=True)
    subprocess.run(f'git commit -m "test"', shell=True)
    subprocess.run(f"git push", shell=True)
    os.chdir(old_wd)


def init(request):
    data = request
    image = data['image']
    if data['mode'] == 'local':
        if 'input' in data:
            input_dir = data['input']
            input_mount = data['input_mount']
        else:
            input_dir = None
            input_mount = None
        output_dir = data['output']
        output_mount = data['output_mount']
    else:
        if 'input' in data:
            empty(INPUT_TEMP)
            old_wd = os.getcwd()
            os.chdir(INPUT_TEMP)
            subprocess.run(f"git clone {data['input']} temp_in", shell=True)
            os.chdir(old_wd)
            input_dir = f"{INPUT_TEMP}/temp_in"
            input_mount = data['input_mount']
        else:
            input_dir = None
            input_mount = None
        empty(OUTPUT_TEMP)
        old_wd = os.getcwd()
        os.chdir(OUTPUT_TEMP)
        branch = data['branch']
        subprocess.run(f"git clone {data['input']} temp_out", shell=True)
        os.chdir(f"{OUTPUT_TEMP}/temp_out")
        subprocess.run(f"git checkout {branch}", shell=True)
        os.chdir(old_wd)
        output_dir = f"{OUTPUT_TEMP}/temp_out"
        output_mount = data['output_mount']
        pass
    env = data['env']
    cmd = data['cmd']
    docker_socket = data['docker_socket']
   
    response = pipeline_run(image, input_dir, output_dir, env, cmd, docker_socket, input_mount, output_mount)
    if data['mode'] != 'local':
        old_wd = os.getcwd()
        os.chdir(f"{OUTPUT_TEMP}/temp_out")
        subprocess.run(f"git add .", shell=True)
        subprocess.run(f"git commit -m 'auto push'", shell=True)
        subprocess.run(f"git push", shell=True)
        os.chdir(old_wd)
        pass
    return response


def vote(request):
    data = request
    dataset = data['dataset']
    branches = data['branches']
    votes = data['votes']
    empty('work')
    empty('result')
    empty('main')
    branch_retrieve(dataset, branches, votes)
    return {"success": True}


if __name__ == '__main__':
    if sys.argv[1] == 'run':
        with open(sys.argv[2], 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)
        response = init(data)
        print(response)
    elif sys.argv[1] == 'vote':
        with open(sys.argv[2], 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)
        response = vote(data)
        print(response)
    else:
        print("Unknown command")
        sys.exit(1)
