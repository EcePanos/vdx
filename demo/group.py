import csv


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


def merge(file):
    with open(file, 'r') as input:
        csv_reader = csv.reader(input)
        with open('static/output.csv', 'w') as output:
            csv_writer = csv.writer(output, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            output = 0
            for row in csv_reader:
                wrow = []
                for i in range(len(row)):
                    try:
                        wrow.append(float(row[i]))
                    except:
                        pass
                # print(row)
                # print(w)

                if len(wrow) == 0:
                    csv_writer.writerow([output])
                else:
                    groups = []
                    for value in wrow:
                        groups = group(groups, value)
                    # Count the size of groups vs sample size
                    output = 9999.9999
                    for i in range(len(groups)):
                        if len(groups[i]) > 0.5*len(wrow):
                            output = sum(groups[i])/len(groups[i])
                            break
                    else:
                        output = sum(wrow)/len(wrow)
                    csv_writer.writerow([output])
