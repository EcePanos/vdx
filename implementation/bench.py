import vdx
import random
import time


# Repeat the experiment 1 billion times
input = []
for i in range(100000):
    # Create a list of 25 random floats between 0 and 1
    input.append([random.random() for i in range(25)])
start_time = time.time()
for item in input:
    # vote using the majority voting bootstrapping with an error of 0.05
    _ = vdx.majority_voting_bootstrapping(item, 0.05)
print("Time taken: {} seconds".format(time.time() - start_time))
print("Average time per vote: {} seconds".format((time.time() - start_time)/len(input)))
