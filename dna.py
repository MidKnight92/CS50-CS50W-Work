from sys import argv, exit
from csv import reader, DictReader


# Take two command-line arguments (1:name of a CSV file 2: name of DNA sequence to identify)
def main(argv):
    dna = []
    # Check for two command-line arguments if less exit program
    if len(argv) != 3:
        print('Usage: python dna.py data.csv sequence.txt')
        exit(1)
    else:
        # Open the CSV file read its coontents into memory
        with open(argv[1], 'r') as csv_file:
            csv_reader = reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    dna = row[1:]
                    line_count += 1
                else:
                    line_count += 1

        # Open the DNA file read its coontents into memory
        with open(argv[2]) as dna_file:
            dna_reader = reader(dna_file)
            dna_string = ''
            for line in dna_reader:
                dna_string = line

    # Compute the longest run of consective STR repeats in the DNA sequence
    # Code below inspired by post on Stack Overflow: https://stackoverflow.com/questions/51690245/consecutive-substring-in-python
            dna_dict = {}
            for str_seq in dna:
                count, start, tmp = 0, 0, 0
                length = len(str_seq)

                while True:
                    match = dna_string[0].find(str_seq, start)
                    if match == -1:
                        break
                    elif start != match:
                        tmp = 0
                        tmp += 1
                        start = match + length
                    else:
                        tmp += 1
                        start = match + length

                    if count < tmp:
                        count = tmp
                dna_dict[str_seq] = count

        # Open CSV File as a OrderedDict
        with open(argv[1], newline='') as csv_file:
            csv_reader = DictReader(csv_file)
            for person_str in csv_reader:
                match = 0
                for dna in dna_dict:
                    if dna_dict[dna] == int(person_str[dna]):
                        match +=1
                if match == len(dna_dict):
                    print(person_str['name'])
                    exit(0)
            print('No match')



# Compare the STR counts against each row in the CSV file
if __name__ == '__main__':
    main(argv)