input = [5, 4, 7]
import vdx
import time

start = time.time()
#for i in range(10000):
# Calculate the distances of all pairs as a 2d array
distances = [[abs(a - b) for a in input] for b in input]

threshold = 2
# Normalize the distances so that they are between 0 and 1, 1 being identical, 0 being outside the threshold
normalized_distances = [[1 - (d / threshold) if d < threshold else 0 for d in row] for row in distances]

print(normalized_distances)

# Calculate the votes using the map() function
votes = list(map(lambda row: sum([row[j] * input[j] for j in range(len(input))]) / sum(row), normalized_distances))
print(votes)
# Average the votes, weighed by the sum of the normalized distances
output = sum([votes[i] * sum(normalized_distances[i]) for i in range(len(input))]) / sum([sum(row) for row in normalized_distances])
print(output)
end = time.time()
print("done in " + str(end - start) + " seconds")

# Alternatively we can check which candidate has the highest sum of normalized distances
# and either select a winner based on that, or use that sum as the weight for the weighted average

start = time.time()
output2 = vdx.majority_voting_bootstrapping(input, 1)
print(output2)
end = time.time()
print("done in " + str(end - start) + " seconds")
