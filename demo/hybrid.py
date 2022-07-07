import csv


def merge(file):
    with open(file, 'r') as input:
        csv_reader = csv.reader(input)
        with open('static/output.csv', 'w') as output:
            csv_writer = csv.writer(output, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            #Initialise weights
            head = next(csv_reader)
            success = [0] * len(head)
            w = [1] * len(head)

            # Remove this line for headed file
            input.seek(0)
            output = 0
            skipped = 0
            reverted = 0
            for row in csv_reader:
                for i in range(len(row)):
                    try:
                        row[i] = float(row[i])
                    except:
                        row[i] = 0
                        w[i] = 0
                #print(row)
                #print(w)

                if sum(row) == 0:
                    skipped += 1
                    csv_writer.writerow([output])
                else:
                    # Apply weights to average calculation
                    wrow = []
                    for i in range(len(row)):
                        wrow.append(row[i]*w[i])
                    if sum(w) == 0:
                        reverted += 1
                        for i in range(len(row)):
                            if row[i] != 0:
                                wrow[i] = row[i]
                                w[i] = 1
                    avg = sum(wrow)/sum(w)

                    #Calculate output
                    min = 10000
                    output = 10000
                    for i in range(len(row)):
                        if abs(row[i] - avg) < min and row[i] != 0:
                            min = abs(row[i] - avg)
                            output = row[i]

                    csv_writer.writerow([output])
                # Adjust weights
                #count += 1
                for i in range(len(row)):
                    s = 0
                    for y in range(len(row)):
                        if i != y and abs(row[i]) >= abs(0.95*row[y]) and abs(row[i]) <= abs(1.05*row[y]):
                            s += 1
                        elif i != y and abs(row[i]) >= abs(0.9*row[y]) and abs(row[i]) <= abs(1.1*row[y]):
                            k = abs(row[i] - row[y])
                            s += 2 - (k / (0.05 * abs(row[y])))
                    s_total = s / (len(row) - 1)

                    k = abs(row[i] - output)
                    e = 0.05*output
                    if k <= e:
                        success[i] += 1
                    elif k > e and k < 2 * e:
                        success[i] += 2 - (k / e)

                    #p = success[i] / count
                    if success[i] >= sum(success)/len(success):
                        w[i] = s_total
                    else:
                        w[i] = 0
            print(w)
