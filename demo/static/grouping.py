values = [0.9, 1.0, 1.0]

"""
def group(groups, value):
    if groups == []:
        groups.append([value])
        return groups
    else:
        for i in range(len(groups)):
            if value >= 0.95 * (sum(groups[i])/len(groups[i])) and value <= 1.05 * (sum(groups[i])/len(groups[i])):
                groups[i].append(value)
                return groups
        groups.append([value])
        return groups

for value in values:
    groups = group(groups, value)
print(groups)
"""

def group_sum(values, indices):
    sum = 0
    for index in indices:
        sum +=values[index]
    return sum

def group(values):
    groups = []
    for i in range (len(values)):
        if groups == []:
            groups.append([i])
        else:
            for y in range(len(groups)):
                if values[i] >= 0.95 * (group_sum(values, groups[y])/len(groups[y])) and values[i] <= 1.05 * (group_sum(values, groups[y])/len(groups[y])):
                    groups[y].append(i)
                    break
            else:
                groups.append([i])
    return groups

print(group(values))
