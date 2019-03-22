#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    // accept only one command line argument
    if (argc != 2)
    {
        printf("Error\n");
        return 1;
    }

    int k = atoi(argv[1]); // convert key from string to int

    // get plaintext
    string p = get_string("plaintext: ");

    printf("ciphertext: ");

    // convert plaintext to ciphertext
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        if (isalpha(p[i]))
        {
            int o = 0;
            if (isupper(p[i]))
            {
                o = (p[i] - 65 + k) % 26 + 65; //ASCII --> alphabetical (add k) --> ASCII 
                printf("%c", (char) o);
            }
            int m = 0;
            if (islower(p[i]))
            {
                m = (p[i] - 97 + k) % 26 + 97;
                printf("%c", (char) m);
            }
        }
        else
        {
            printf("%c", p[i]);
        }
    }
    printf("\n");
}