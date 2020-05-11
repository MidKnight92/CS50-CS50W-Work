import sys
from cs50 import get_float

def main():
    amount = change_owned();

    # Initialize coin variable to 0 this will be incremented as coins are being used
    coins = 0

    # Initialize diff to amount owed to customer this will keep track of remaining change owed
    diff = amount

    # Check if the diff is greater then or equal to respective amounts and not zero
    # increment coin if so and minus the difference
    while diff >= 25 and diff > 0:
        coins += 1
        diff -= 25

    while diff >= 10 and diff > 0:
        coins += 1
        diff -= 10

    while diff >= 5 and diff > 0:
        coins += 1
        diff -= 5

    while diff >= 1 and diff > 0:
        coins += 1
        diff -= 1

    return print(coins, "\n")

# Prompt user for change owed
def change_owned():

    # declare change variable
    change = 0

    # If the user inputs a non-negative number reprompt
    while True:
        change = get_float("Change owed: ")
        if change > 0:
            break

    # Convert Dollars to Cents and return
    return round(change * 100)

if __name__ == "__main__":
    main()
