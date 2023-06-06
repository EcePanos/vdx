import vdx
import time

input = [0.9, 1.0, 1.1]
weights = [0.9, 0.9, 0.9]

def mlv(input, weights, margin):
    deltas = []
    for i in range(len(input)):
        delta = []
        for y in range(len(input)):
            if i != y:
                k = abs(input[i] - input[y])
                # round k to the nearest 0.1
                k = round(k * 100) / 100
                #print(k)
                if k <= margin:
                    delta.append(weights[i])
                else:
                    p = (1-weights[i])/(len(input) - 1)
                    p = round(p * 100) / 100
                    delta.append(p)
            #print(delta)
        # append the product of the deltas to the deltas list
        product = 1
        for item in delta:
            product *= item
            product = round(product * 100) / 100
        deltas.append(product)
    # find the index of the largest delta
    #print(deltas)
    index = deltas.index(max(deltas))
    # return the input at the index
    return input[index]
result1 = []
start = time.time() 
for i in range(10000):
    p = mlv(input, weights, 0.1)
    result1.append(p)
end = time.time()
print("done in " + str(end - start) + " seconds")

result2 = []
start = time.time()
for i in range(10000):
    p = vdx.weighted_average(input, weights)
    p = vdx.nearest_neighbor(p, input)
    result2.append(p)
end = time.time()
print("done in " + str(end - start) + " seconds")

result3 = []
start = time.time()
for i in range(10000):
    p = vdx.majority_voting_bootstrapping(input, 0.1)
    p = vdx.nearest_neighbor(p, input)
    result3.append(p)
end = time.time()
print("done in " + str(end - start) + " seconds")

# MLV is O(n^2) and is the slowest algorithm.
# Weighted average is O(n) and is the fastest algorithm.
# Majority voting bootstrapping is O(n) and is slower than weighted average but faster than MLV.