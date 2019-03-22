#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    long long cc_number;
    int digit_number = 0;
    long long digit1;
    long long digit2;

    // prompt user to give cc_number greater than 0
    do
    {
        cc_number = get_long_long("credit card number: ");
    }
    while (cc_number <= 0);

    // determine how many digits a cc_number contains
    long long a = cc_number; //a helps not to increase cc_number value
    while (a != 0)
    {
        a = a / 10;
        ++digit_number;
    }

    // find 1st and 2nd digits
    long long b = round(pow(10, digit_number));
    long long c = b / 10;
    digit1 = cc_number % b / (b / 10);
    digit2 = cc_number % c / (c / 10);
    long long d = 10;
    long long e = d * 10;

    // Luhn’s algorithm formula
    // 1 step - multiply every other digit by 2, starting with the number’s second-to-last digit,
    // and then add those products' digits together.
    int result = 0; 
    int sum = 0;
    do
    {
        result = cc_number % e / (e / 10) * 2; //result = every other digit * 2
        if (result % 10 == result)
        {
            sum = sum + result;
        }
        else
        {
            sum = sum + result % 10 + result / 10;
        }
        e = e * 100;
    }
    while (e < b + 1);
    
    // 2 step - add the sum to the sum of the digits that weren’t multiplied by 2.
    do
    {
        sum = sum + cc_number % d / (d / 10);
        d = d * 100;
    }
    while (d < b + 1);
    
    // 3 step - check if sum's last digit is 0. If yes, the credit card number is valid.
    int x = sum % 10;

    // check the card type and validity
    if (digit1 == 3 && (digit2 == 4 || digit2 == 7) && x == 0 && digit_number == 15)
    {
        printf("AMEX\n");
    }
    else if (digit1 == 5 && (digit2 == 1 || digit2 == 2 || digit2 == 3 || digit2 == 4 || digit2 == 5) && x == 0 && digit_number == 16)
    {
        printf("MASTERCARD\n");
    }
    else if (digit1 == 4 && x == 0 && (digit_number == 13 || digit_number == 16))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}