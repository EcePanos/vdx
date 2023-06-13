import time


input = [5, 4, 7]

# Calculate the distances of all pairs as a 2d array
def vote(input):
    distances = [[abs(a - b) for a in input] for b in input]
    threshold = 2
    # Normalize the distances so that they are between 0 and 1, 1 being identical, 0 being outside the threshold
    normalized_distances = [[1 - (d / threshold) if d < threshold else 0 for d in row] for row in distances]

    # Calculate the votes using the map() function
    votes = [sum([row[j] * input[j] for j in range(len(input))]) for row in normalized_distances]
    #print(votes)
    # Average the votes, weighed by the sum of the normalized distances
    output = sum([votes[i] for i in range(len(input))]) / sum([sum(row) for row in normalized_distances])
    return output

def dwm(input):
    distances = [[abs(a - b) for a in input] for b in input]
    threshold = 2
    # Normalize the distances so that they are between 0 and 1, 1 being identical, 0 being outside the threshold
    normalized_distances = [[1 - (d / threshold) if d < threshold else 0 for d in row] for row in distances]
    weights = [sum(row) for row in normalized_distances]
    # Calculate the weighted average of the input, weighed by the inverse sum of distances
    output = sum([input[i] * weights[i] for i in range(len(input))]) / sum(weights)
    #print(output)
    return output

start = time.time()
for i in range(10000):
    vote(input)
end = time.time()
print("vote done in " + str(end - start) + " seconds")

start = time.time()
for i in range(10000):
    dwm(input)
end = time.time()
print("dwm done in " + str(end - start) + " seconds")