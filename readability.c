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

//prompt user for a string of text
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
       if (islower(text[i]) || isupper(text[i]))
       {
           letters++;
       }

       if (isspace(text[i]))
       {
           words++;
       }

       if (text[i] == p || text[i] == q || text[i] == e)
       {
            // printf("This is text[i]:%c p:%c q:%c e:%c\n", text[i], p, q, e);
           sentences++;
       }
   }
//   printf("This the letters, words, sentence count: %i %i %i\n", letters, words, sentences);

   avg_ltrs( letters, words);
   avg_sent(sentences, words);

   return 0;
}

// TODO
// avg number of letters per 100 words in the text
int avg_ltrs(int letter, int words)
{
    float l = 0;


    l = (letter * 100.0) / words;

    // printf("L:%.1f\n", l);
    L = l;
    return 0;
}

// //avg number of sentences per 100 words in the text
int avg_sent(int sentences, int words)
{
    float s = 0;


    s = (sentences * 100.0) / words;

    // printf("S: %.1f\n", s);
    S = s;
    return 0;
}