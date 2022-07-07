import csv
import service_redis as service
#import service

service.create_algorithm("simple", collation='nearest_neighbor', error=0.05, bootstrapping=True)


def merge(file):
    with open(file, 'r') as input:
        csv_reader = csv.reader(input)
        with open('output.csv', 'w') as output:
            csv_writer = csv.writer(output, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
            #Initialise candidates
            head = next(csv_reader)
            for i in range(len(head)):
                service.create_candidate(head[i])

            # Remove this line for headed file
            #input.seek(0)
            results = []
            count = 1
            for row in csv_reader:
                #print(f"Row {count} of 10000")
                values = row
                candidates = head
                #print(candidates)
                result, history, weights = service.vote_num('simple', candidates, values)
                #print(result)
                results.append(result)
                csv_writer.writerow([result])
                count += 1

merge('diffs.csv')








        




   