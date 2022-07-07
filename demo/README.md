# Voting Algorithm Demonstrator

A demo application built to allow easy evaluation
of our work on voting algorithms to aid reproducibility
of our results.

## Pre-requisites
- Python3, pip

## Install instructions

- Install the dependencies:
```
pip3 install -r requirements.txt
```

- Run the app:
```
python3 app.py
```

- Follow the displayed browser link to the app and follow the on-screen instructions to use.

## Docker image

Alternatively, if you have Docker installed, you can use a pre-built public docker image:

```
docker run panosece/voting_demo
```

The Dockerfile needed to build this image yourself is also included in this repo.

```
docker build -t <your-image:tag> .
```