import sys
from cs50 import get_int


def main():
    # Call Prompt for User Input
    height = prompt()
    # Run Pyramid if True else Exit
    if height:
        pyramid(height)
    else:
        sys.exit()

# Gather Input from User


def prompt():
    # Run until User Provides a Number between 1-8
    while True:
        height = get_int("Height: ")
        if height > 0 and height < 9:
            break
    return height

# Print Pyramid


def pyramid(height):
    # Loop up to height
    for i in range(height):
        # Spaces are the Difference Between Total Number of Rows and the Row Number
        print(" " * (height - i - 1), end="")
        # Hashes are One More then the Row Number
        print("#" * (i + 1), end="")
        print()
        

if __name__ == "__main__":
    main()