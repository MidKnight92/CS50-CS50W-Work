// Determines grade level of inputed text

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>



string prompt();
int count_args();
int avg_ltrs();
int avg_sent();

float S;
float L;

int main(void)
{

    prompt();
    float real_num = 0.0588 * L - 0.296 * S - 15.8;

    // Round float to int
    int index = roundf(real_num);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index <= 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

// Prompt user for a string of text
string prompt(void)
{
    string text;
    do
    {
        text = get_string("Text: ");
    }
    while (strlen(text) == 0);
    count_args(text);
    return 0;
}


// Determine the number of letters, words, and sentences in the text
int count_args(string text)
{
    int letters = 0, words = 1, sentences = 0;
    char p = '.', q = '?', e = '!';

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // If a lowercase or uppercase letter is detected increment letters
        if (islower(text[i]) || isupper(text[i]))
        {
            letters++;
        }

        // If a space is detected increment words and add one for the last word in the sentence
        if (isspace(text[i]))
        {
            words++;
        }

        // If '.', '!', or '?' is detected increment sentences
        if (text[i] == p || text[i] == q || text[i] == e)
        {
            sentences++;
        }
    }
    // Pass the ints of letters and words as args to avg_ltrs
    avg_ltrs(letters, words);

    // Pass the ints of letters and words as args to avg_sent
    avg_sent(sentences, words);

    return 0;
}


// Average number of letters per 100 words in the text
int avg_ltrs(int letter, int words)
{
    float l = 0;

    l = (letter * 100.0) / words;
    //redefine the global variable
    L = l;
    return 0;
}

// Average number of sentences per 100 words in the text
int avg_sent(int sentences, int words)
{
    float s = 0;

    s = (sentences * 100.0) / words;
    // Redefine the global variable
    S = s;
    return 0;
}