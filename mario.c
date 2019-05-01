#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    do
    {
        h = get_int("Enter a positive integer: ");
    }
    while (h < 1 || h > 8);
    for (int i = 0; i < h; i++)
    {
        for (int j = 1; j < h - i; j++)
        {
            printf(" ");
        }
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
