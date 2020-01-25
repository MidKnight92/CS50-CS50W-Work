#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>



string prompt();
int count_args();
int avg_ltrs();
int avg_sent();

float S;
float L;

int main(void)
{

    prompt();
    int index = 0.0588 * L - 0.296 * S - 15.8;

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

//Prompt user for a string of text
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


// Find the number of letters, words, and sentences in the text
int count_args(string text)
{

   int letters = 0;
   int words = 1;
   int sentences = 0;
   char p = '.';
   char q = '?';
   char e = '!';


   for (int i = 0, n = strlen(text); i < n; i++)
   {
       // If an upper of lowercase letter is detected increment letters
       if (islower(text[i]) || isupper(text[i]))
       {
           letters++;
       }

       // If a space is detected increment words and add one for the last word
       if (isspace(text[i]))
       {
           words++;
       }

       // If '.', '?', or '!' is detected increment sentences
       if (text[i] == p || text[i] == q || text[i] == e)
       {
           sentences++;
       }
   }

   avg_ltrs( letters, words);
   avg_sent(sentences, words);

   return 0;
}


// avg number of letters per 100 words in the text
int avg_ltrs(int letter, int words)
{
    float l = 0;

    if (words < 100)
    {
        l = (letter * 100) / words;
    }

    L = l;
    return 0;
}

// //avg number of sentences per 100 words in the text
int avg_sent(int sentences, int words)
{
    float s = 0;

    if (words < 100)
    {
        s = (sentences * 100) / words;
    }

    S = s;
    return 0;
}