#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    float dollars;
    int remainder;
    int coins = 0;

    do {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);

    int cents = round(dollars * 100);

    while (cents >= 25)
    {
        coins++;
        cents -= 25;
    };

    while (cents >= 10)
    {
        coins++;
        cents -= 10;
    };

    while (cents >= 5)
    {
        coins++;
        cents -= 5;
    };

    while (cents >= 1)
    {
        coins++;
        cents -= 1;
    };

    printf("%i\n", coins);
}

