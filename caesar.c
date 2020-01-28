// Converts Plain Text to Cipher Text
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int key;
int prompt(void);
int enicpher(void);
// int upper[];
// int lower[];

// Takes User Command Line Arguments as Key if criteria is meet
int main(int argc, string argv[])
{
    // Throws Error if there is not an arg provided or more than two
    if (argc != 2 || argc > 2 )
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
    char cipher_digits;
    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        cipher_digits = (text[i] + key);
        if (isdigit(text[i]) || ispunct(text[i]))
        {
            printf("%c", text[i]);
        }
        else if (isupper(text[i]))
        {
            if (cipher_digits > 90 || cipher_digits < 65)
            {
                printf("%c", ((cipher_digits -  65) % 26) + 65);
            }
            else
            {
                printf("%c", cipher_digits);
            }
        }
        else
        {
            if (cipher_digits > 122 || cipher_digits < 97)
            {
                printf("%c", ((cipher_digits - 97) % 26) + 97);
            }
            else
            {
                printf("%c", cipher_digits);
            }
        }

    }
    printf("\n");
    return 0;
}
