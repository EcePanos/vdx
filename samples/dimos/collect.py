import os
import glob
#import verify
import csv_merger as verify

#change this so it returns a list
def consensus(path, votes):
    dirs = [f.path for f in os.scandir(path) if f.is_dir() and "__" not in f.path]
    #rint(dirs)
    dirs.sort()
    data = votes
    print(data)
    for item in data:
        prefix = item['prefix']
        index = item['index']
        candidates = []
        for dir in dirs:
            files = glob.glob(f"{dir}/{prefix}*.csv")
            files.sort()
            candidates.append(files[-1])
        print(candidates)
        verify.validate(prefix, index, candidates)
