#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int shift(char c);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1; 
    }
    
    string keyword = argv[1];
    for (int i = 0; i < strlen(keyword); i++)
    {
        if (!isalpha(keyword[i]))
        {	
            printf("Usage: ./vigenere keyword\n");
            return 1;
		}
    }
    string msg = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, j = 0, key = 0; i < strlen(msg); i++)
    {
        if (j == strlen(keyword))
        {
            j = 0;
        }
        key = shift(keyword[j]);
        if (islower(msg[i]))
        {
            printf("%c", (((msg[i] + key) - 97) % 26) + 97);
            j++;
        }
        else if (isupper(msg[i]))
        {
            printf("%c", (((msg[i] + key) - 65) % 26) + 65);
            j++;
        }
        else
        {
            printf("%c", msg[i]);
        }
    }
    printf("\n");
}

int shift(char c)
{
    int a = c;
    if (islower(c))
    {
        a -= 97;
    }
    else if (isupper(c))
    {
        a -= 65;
    }
    return a;
};
