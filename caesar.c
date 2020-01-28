// Converts Plain Text to Cipher Text
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int key;
int prompt(void);
int enicpher(void);


// Takes User Command Line Arguments as Key if criteria are met
int main(int argc, string argv[])
{
    // Throws Error if there is not an arg provided or more than two
    if (argc != 2)
    {
        printf("Usage: ./casesar key\n");
        return 1;
    }
    else
    {
        // If arg is provided checks indiviual values
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            // Throws error if not a number
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./casesar key\n");
                return 1;
            }
        }
        // Convert digit to an int
        key = atoi(argv[1]);
        printf("Success\n%i\n", key);
        prompt();
        return 0;
    }
}

// Prompt user for plain text input and ouput cipher
int prompt(void)
{
    int cipher_digits;
    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    // Loops over the plaintext and output cipher text
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        cipher_digits = (text[i] + key);
        if (islower(text[i]))
        {
            printf("%c", ((cipher_digits - 'a') % 26) + 'a');
        }
        else if (isupper(text[i]))
        {
            printf("%c", ((cipher_digits - 'A') % 26) + 'A');
        }
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
    return 0;
}
