#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    char *image = argv[1];

    FILE *inptr = fopen(image, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", image);
        return 2;
    }

    FILE *photo;

    BYTE *buffer = malloc(512);

    int exist_jpeg = 0;

    char name[8];

    int n = 0;

    while (fread(buffer, 512, 1, inptr))
    {
        // start of a new JPEG?
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Already found a JPEG?
            if (exist_jpeg)
            {
                fclose(photo);
                sprintf(name, "%03i.jpg", n);
                n++;
                photo = fopen(name, "w");
                fwrite(buffer, 512, 1, photo);
            }
            else
            {
                sprintf(name, "%03i.jpg", n);
                n++;
                photo = fopen(name, "w");
                fwrite(buffer, 512, 1, photo);
                exist_jpeg = 1;
            }
        }
        else if (exist_jpeg)
        {
            fwrite(buffer, 512, 1, photo);
        }
    }

    free(buffer);

    fclose(inptr);
}
