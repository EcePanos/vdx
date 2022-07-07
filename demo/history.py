import csv

def merge(file):
    with open(file, 'r') as input:
        csv_reader = csv.reader(input)
        with open('static/output.csv', 'w') as output:
            csv_writer = csv.writer(output, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            #Initialise weights
            count = 0
            head = next(csv_reader)
            success = [0] * len(head)
            w = [1] * len(head)

            # Remove this line for headed file
            input.seek(0)
            output = 0
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
                    csv_writer.writerow([output])
                else:
                    # Apply weights to average calculation
                    wrow = []
                    for i in range(len(row)):
                        wrow.append(row[i]*w[i])
                    if sum(w) == 0:
                        for i in range(len(row)):
                            if row[i] != 0:
                                wrow[i] = row[i]
                                w[i] = 1
                    output = sum(wrow)/sum(w)
                csv_writer.writerow([output])
                # Adjust weights
                """
                count += 1
                for i in range(len(row)):
                    if row[i] >= 0.95*avg and row[i] <= 1.05*avg:
                        success[i] += 1
                    w[i] = (success[i]/count)**2
                """
                count += 1
                for i in range(len(row)):
                    s = 0
                    for y in range(len(row)):
                        if i != y and row[i] >= 0.95*row[y] and row[i] <= 1.05*row[y]:
                            s += 1
                    if s >= (len(row)-1)/2:
                        success[i] += 1
                    w[i] = (success[i]/count)**2
            print(w)
