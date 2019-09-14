// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    int n = atoi(argv[1]);

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);


    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // save properties of the infile
    int in_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int in_biWidth = bi.biWidth;
    int in_biHeight = abs(bi.biHeight);

    // set outfile's width and height
    bi.biWidth *= n;
    bi.biHeight *= n;

    // determine padding for the outfile
    int out_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // set outfile's size and file size
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + out_padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    RGBTRIPLE piArr[bi.biWidth];

    // iterate over infile's scanlines
    for (int i = 0; i < in_biHeight; i++)
    {
        int arrPos = 0;

        // iterate over pixels in scanline
        for (int j = 0; j < in_biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write pixel n times to array
            for (int k = 0; k < n; k++)
            {
                piArr[arrPos] = triple;
                arrPos++;
            }
        }

        // write array n times to outfile
        for (int l = 0; l < n; l++)
        {
            fwrite(&piArr, sizeof(piArr), 1, outptr);

            // write padding
            for (int m = 0; m < out_padding; m++)
            {
                fputc(0x00, outptr);
            }
        }

        // skip over in_padding, if any
        fseek(inptr, in_padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
