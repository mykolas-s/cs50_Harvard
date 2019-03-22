// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "dictionary.h"

#define ALPHABET_SIZE 27
#define DICTIONARY "dictionaries/large"

// initialize node. Each node has an array of 27 pointers to another such structs and a bool variable
typedef struct node
{
    bool is_word;
    struct node* children[27];
}
node;

node *root = NULL;
int wordcount = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // initialize root
    root = malloc(sizeof(node));
    root->is_word = false;
    for (int j = 0; j < ALPHABET_SIZE; j++) // initialize children to NULLs
    {
        root->children[j] = NULL;
    }

    // open dictionary for reading
    FILE* dict = fopen(dictionary, "r");

    char buffer[LENGTH +1];

    while (fscanf(dict, "%s", buffer) != EOF)
    {
        node *trav = root;
        int lenght = strlen(buffer);
        for (int c = 0; c < lenght; c++)
        {
            int index;
            if (buffer[c] == '\'')
            {
                index = 26;
            }
            else
            {
                index = ((int)buffer[c] - (int)'A') % 32;
            }

            if (!trav->children[index])
            {
                node *new_node = malloc(sizeof(node));
                new_node->is_word = false;

                for (int j = 0; j < ALPHABET_SIZE; j++)
                {
                    new_node->children[j] = NULL;
                }
                trav->children[index] = new_node; //move children[index] to the new node
            }
            trav = trav->children[index]; //move trav to the new node
        }
        trav->is_word = true; // mark last node as leaf
        wordcount++;
    }
    fclose(dict);
    return true;

    if (dict == NULL)
    {
        return false;
    }
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *trav = root;
    int lenght = strlen(word);
    for (int c = 0; c < lenght; c++)
    {
        int index;
        if (word[c] == '\'')
        {
            index = 26;
        }
        else
        {
            index = ((int)word[c] - (int)'A') % 32;
        }

        if (!trav->children[index])
        {
            return false;
        }
        trav = trav->children[index];
    }
    
    // check if it's leaf
    if (trav->is_word == true && trav != NULL)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (&load)
    {
        return wordcount;
    }
    else
    {
        return 0;
    }
}

void deleteNode(node* trav)
{
    for (int c = 0; c < ALPHABET_SIZE; c++)
    {
        if (trav->children[c])
        {
            deleteNode(trav->children[c]);
        }
    }
    free(trav);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node* trav = root;
    deleteNode(trav);
    return true;

    if (root != NULL)
    {
        return false;
    }
}