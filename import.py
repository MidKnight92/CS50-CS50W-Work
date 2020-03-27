# Imports data from a CSV
from sys import argv, exit
from csv import reader, DictReader
from cs50 import SQL




# Accept the name of a CSV file as command-line argumnet
def main(argv):
    # Check if length does not equal 2
    if len(argv) != 2:
        # Print Error Message and Exit
        print('Usage: python import.py characters.csv')
        exit(1)
    else:
        # Create Student Database
        open('students.db', 'w').close()
        db = SQL('sqlite:///students.db')

        # Create tables
        db.execute('CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)')

        # Open Charactrer's CSV file
        with open(argv[len(argv) - 1], 'r') as file:

            # Create DictReader for CSV
            reader = DictReader(file)

            # Iterate over CSV file
            for row in reader:

                # Assign Values to House and Birth
                house, birth = row['house'], int(row['birth'])

                # Check for Name Row
                if row['name']:

                    # Split Name Row into a List Of Names
                    split_name = row['name'].split()

                    # Check if the Length does not have Middle Name and Assign None to it Else Assign the Name
                    if len(split_name) != 3:
                        first = split_name[0]
                        middle = None
                        last = split_name[1]
                    else:
                        first = split_name[0]
                        middle = split_name[1]
                        last = split_name[2]

                # Insert into Student DB
                db.execute('INSERT INTO students (first, middle, last, house, birth) VALUES(?,?,?,?,?)', first, middle, last, house, birth)

    exit(0)

if __name__ == '__main__':
    main(argv)
