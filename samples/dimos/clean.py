import shutil
import os

def empty(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

empty('input')
empty('output')
empty('result')
empty('work')
empty('main')