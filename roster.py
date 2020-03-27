# Print a list of students for a given house in alphabetical order

from sys import argv, exit
from cs50 import SQL

# Accept the Name of a House as a Command-line Argument
def main(argv):
    # Check that three arguments were given
    if len(argv) != 2:
        print('Usage: python roster.py [House Name]')
        exit(1)
    else:
        # Assign house to the last argument
        house = argv[len(argv) - 1]

        # Connect to Students Database
        db = SQL('sqlite:///students.db')

        # Query for students in specified house
        students = db.execute('SELECT * FROM students WHERE house =  ? ORDER BY last, first', house)

        # Print out each student's full name and birth year
        for student in students:
            middle = ' '+ student['middle'] + ' ' if student['middle'] != None else ' '
            full_name = student['first'] + middle + student['last']
            year = student['birth']
            print(f'{full_name}, born {year}')
    exit(0)

if __name__ == '__main__':
    main(argv)