#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float f;
    
    //prompt user for a positive number
    do
    {
        f = get_float("Change owed: ");
    }
    while (f < 0);

    // float --> integer
    int x = 0;
    int i = roundf(f * 100);

    // give a 25$ coin until change owed is lower than 25$
    while (i >= 25)
    {
        i = i - 25;
        x = x + 1;
    }

    // give a 10$ coin until change owed is lower than 10$
    while (i >= 10)
    {
        i = i - 10;
        x = x + 1;
    }

    // give a 5$ coin until change owed is lower than 5$
    while (i >= 5)
    {
        i = i - 5;
        x = x + 1;
    }

    // give a 1$ coin until change owed is lower than 1$
    while (i >= 1)
    {
        i = i - 1;
        x = x + 1;
    }

    // x - number of coins we should give back
    printf("%i\n", x);
}
