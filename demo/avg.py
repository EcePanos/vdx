import csv

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

                #print(w)

                if len(wrow) == 0:
                    csv_writer.writerow([output])
                else:
                    output = sum(wrow)/len(wrow)
                    csv_writer.writerow([output])
