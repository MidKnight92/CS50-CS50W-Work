# Determine grade level of inputed text
from cs50 import get_string
L = 0.00
S = 0.00

# Todo
def main(l,s):
    # Invoke the promptUser function
    promptUser()

    # Coleman-Liau Index
    real_num = 0.0588 * L - 0.296 * S - 15.8

    # Round float to int
    index = round(real_num)

    # Index is above 16 the Reading Level is at 16+. When the Index is below 1, the reading level is below first grade
    if index >= 16:
        print('Grade 16+')
    elif index <= 1:
        print('Before Grade 1')
    else:
        print(f'Grade {index}')





# Prompt user for a string of text
def promptUser():
    # Run as long as it takes to get input from the user
    while(True):
        text = get_string('Text: ')
        # Check that user gave input by the length of text; Break out of loop when user gives input
        if len(text) > 0:
            break
    return countArgs(text)

# Determine the number of letters, and words, and senteces in the text
def countArgs(text):

    # Assign variables to track the amounts
    letters, words, sentences = 0,  1, 0

    # Loop through each word in the text and increment values accordingly
    for t in text:
        if t.isupper() or t.islower():
            letters += 1

        if t.isspace():
            words += 1

        if t == '.' or t == '?' or t == '!':
            sentences += 1

    # Pass the number of letters and words as args to avg_ltrs
    avg_ltrs(letters, words)

    # Pass the number of letter and words as args to avg_sent
    avg_sent(sentences, words)


def avg_ltrs(letter, words):
    l = (letter * 100) / words
    global L
    L = l




def avg_sent(sentences, words):
    s = (sentences * 100) / words
    global S
    S = s


# Calls main function last
if __name__ == '__main__':
    main(L,S)


