#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n;
    int b;
    int a = 1;
    
    // prompt user for a positive number lower than 23
    do
    {
        n = get_int("pyramid heigt (number lower than 24): ");
    }
    while (n < 0 || n > 23);

    // print this many rows
    for (int i = 0; i < n; i++)
    {
        b = n - a;
        
        // print this namy _'s in a row
        for (int k = 0; k < b; k++)
        {
            printf(" ");
        }

        // print this namy #'s in a row
        for (int j = 0; j < a; j++)
        {
            printf("#");
        }

        printf("  ");

        // print this namy #'s in a row
        for (int j = 0; j < a; j++)
        {
            printf("#");
        }

        printf("\n");
        a = a + 1;
    }
}