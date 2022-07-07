# DiMOS Nano

DiMOS Nano is a Docker + git wrapper for using the tools and datasets of a DiMOS federation. It offers the ability to directly mount git repositories as volumes in Docker containers, as well as the ability to trigger voting-based merging of data files (in CSV format) among branches in a git repository.

## Prerequisites

A Linux machine with:

- git
- Docker
- python 3.8+ and pip
- A Redis instance running (eg via Docker)

## Installation

```
pip3 install -r requirements.txt
```

## Configuration

- If you wish to contribute data to a DiMOS dataset:
  1. Join a dataset git repo by communicating with its maintainer
  2. Set up SSH access for your git account and set up the key with you machine or VM
  3. Create a branch **that you use to submit data**

## Developing tools and datasets

Any Docker container can be used as a DiMOS tool, as long as it produces output data in `CSV` format.

## Running tools

You can run the tool `execute_local.py` tool with the `run` parameter and a yaml file as the second parameter. The yaml file should contain the following fields:

```
---
image: your-image-here
mode: remote
input: git@github.com:your-repo-here
output: git@github.com:your-repo-here
input_mount: "/usr/src/app/input"
output_mount: "/usr/src/app/data"
branch: node2
env:
cmd:
docker_socket: false

```
#### Field exmplanations:

- **image**: The Docker image of the tool to use.
- **mode**: Whether to use local files or remote git repositories.
- **input/output**: Input and output directories or repositories. Input is optional.
- **input/output_mount**: Input and output directories inside tool container. Input is optional.
- **branch**: The branch to add the data to.
- **env/cmd**: Environment variable or custom commands for the tool container.
- **docker_socket**: Whether the tool specified has access to the host Docker socket. Some DiMOS tools need to launch additional containers and need this option.

### Hello world tool

The `image` directory of this repository includes the files to build a test tool to check that DiMOS Nano works properly. The tool can also be used as a minimal blank template to develop DiMOS-compatible tools.

## Voting

To vote use the same tool with the `vote` parameter and a yaml file as the second parameter.

Voting currently only supports `CSV` files. 

**It is recommended for automation purposes that DiMOS tools produce `CSV` files so no additional pre-proccessing is required between running and voting.**


Sample voting configuration:

```
---
dataset: git@github.com:your-repo-here
branches:
- node1
- node2
- test1
votes:
- prefix: test
  index: date

```
The vote field works as follows:

- prefix: Partial filename. Matches will be sorted and the **last** file will be merged. Useful for datasets where a date is appended to the filename as the voter will automatically select the most recent file from each branch.
- index: The name of the column to be used as the index. This column will be used as the unique identifier for each row and as such the values of that column will not be voted on.

If multiple files should be voted on, add them to the vote array in the request.

The files resulting from the vote will be pushed to the `main` branch of the repository.