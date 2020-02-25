// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1;

// Hash table
node *table[N];

int word_count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{

    // Hash Word to Obtain a Hash Int Value
    int index = hash(word);

    // First: Access Linked List at that Index in the Hash Table
    // Second: Traverse linked list, looking for the Word
    for (node *trav = table[index]; trav != NULL; trav = trav->next)
    {
        if (strcasecmp(word, trav->word) == 0)
        {
            // Found word in Dictionary
            return true;
        }
    }

    // Word is not in Dictionary
    return false;
}

// Hashes word to a number
// Hash Function Reference from Neel Metha https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
unsigned int hash(const char *word)
{
    N = 2000;

    unsigned long hash_word = 5381;

   for (const char *ptr = word; *ptr != '\0'; ptr++)
   {
        hash_word = ((hash << 5) + hash) + tolower(*ptr);
   }

    return hash_word % table;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    // Open Dictionary File for Reading
    FILE *file = fopen(dictionary,"r");

    // Check if Opened Correctly
    if (file == NULL)
    {
        printf("File could not open/n");
        fclose(file);
        return false;
    }

    // Create a Word Array Buffer with Enough Room for Max Length of a Word Plus the Null Character
    char *word[LENGTH  + 1];

    // Read All the Strings from File until End Of File
    while (fscanf(file, "%s", word) !=  EOF)
    {
        // Allocate Memory for a New Node for Each String
        node *n = malloc(sizeof(node));

        // Check for an Error i.e., Not Enough Space in Memory
        if (n == NULL)
        {
            printf("Error in allocating memory for new node\n");
            // unload();
            return false;
        }

        // Insert node into Hash Table at that location
        strcpy(n->word, word);

        // Hash Word to Obtain a Hash Int Value
        int index = hash(word);

        // Establish pointer
        n->next = table[index];

        // Index into Hash Table Index of the Hash Value and Assign it's value to the New Node
        table[index] = n;

        word_count++;
    }

    // Close File
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{

    node *trav = table;
    node *tmp = trav;

    // Iterate over hash table
    while (table != NULL)
    {
          trav = trav->next;
          free(tmp);
          tmp = trav;
    }

    // Return True if trave is Equal to NULL i.e., All Memory was freed
    return trav == NULL ? true : false;

}

