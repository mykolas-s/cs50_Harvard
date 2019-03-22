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
    // chekc if all characters are alphabetical
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!(isalpha(argv[1][i])))
        {
            printf("Error\n");
            return 1;
        }
    }

    string p = get_string("plaintext: ");
    printf("ciphertext: ");

    int k = strlen(argv[1]);
    int count = 0; //counter for non-alphabetic chars the programm went through
    // convert plaintext to ciphertext
    for (int i = 0, n = strlen(p); i < n; i++)
    {

        int j = (i - count) % k;
        if (isalpha(p[i]))
        {
                int c = 0;
                if (isupper(p[i]) && isupper(argv[1][j]))
                {
                    c = (p[i] - 65 + argv[1][j] - 65) % 26 + 65; //ASCII --> alphabetical (add k) --> ASCII
                    printf("%c", (char) c);
                }
                else if (islower(p[i]) && islower(argv[1][j]))
                {
                    c = (p[i] - 97 + (argv[1][j] - 97)) % 26 + 97;
                    printf("%c", (char) c);
                }

                else if (isupper(p[i]) && islower(argv[1][j]))
                {
                    c = (p[i] - 65 + (argv[1][j] - 97)) % 26 + 65;
                    printf("%c", (char) c);
                }

                else if (islower(p[i]) && isupper(argv[1][j]))
                {
                    c = (p[i] - 97 + (argv[1][j] - 65)) % 26 + 97;
                    printf("%c", (char) c);
                }
        }
        else
        {
           printf("%c", p[i]);
           count++;
        }
    }
    printf("\n");
}