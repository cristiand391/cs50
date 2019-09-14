#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    int key;
    if (argc == 2)
    {
        string str_key = argv[1];
        for (int i = 0; i < strlen(str_key); i++)
        {
            if (!isdigit(str_key[i]))
            {	
                printf("Usage: ./caesar key\n");
                return 1;   
            }
        }
        key = atoi(str_key);
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    string msg = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; i < strlen(msg); i++)
    {
        if (islower(msg[i]))
        {
            printf("%c", (((msg[i] + key) - 97) % 26) + 97);
        }
        else if (isupper(msg[i]))
        {
            printf("%c", (((msg[i] + key) - 65) % 26) + 65);
        }
        else
        {
            printf("%c", msg[i]);
        }
    }
    printf("\n");
}
