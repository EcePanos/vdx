import time


input = [5, 4, 7]

start = time.time()
for i in range(10000):
    # For each element of the input, calculate the inverse sum of distances to all other elements
    # catch division by zero, and set the distance to max int
    dists = []
    for i in range(len(input)):
        try:
            dists.append(1 / sum([abs(input[i] - input[j]) for j in range(len(input)) if i != j]))
        except ZeroDivisionError:
            dists.append(999)

    #print(dists)

    # Calculate the weighted average of the input, weighed by the inverse sum of distances
    output = sum([input[i] * dists[i] for i in range(len(input))]) / sum(dists)
    print(output)
end = time.time()
print("done in " + str(end - start) + " seconds")