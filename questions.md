# Questions

## What's `stdint.h`?

stdint.h is a header file that provides a set of int types with a fixed size.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

Using these data types you can know their specific size and the range of bits that can be stored on it.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE = 1 byte
DWORD = 4 bytes
LONG = 4 bytes
WORD = 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

1st byte: 0x42
2nd byte:  0X4D

## What's the difference between `bfSize` and `biSize`?

The first expresses the size of the bitmap file and the last the size of its header (BITMAPINFOHEADER).

## What does it mean if `biHeight` is negative?

It means that the bitmap's vertical orientation is top-down.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in `copy.c`?

fopen might return NULL if it can't open the input or output file.

## Why is the third argument to `fread` always `1` in our code?

The third argument is always '1' because we are only reading one item at a time (the BITMAPFILEHEADER, BITMAPINFOHEADER and the "triple" encapsulated RGB values).

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

fseek moves the file pointer to a specific location.

## What is `SEEK_CUR`?

SEEK_CUR is a constant, storing the current position of the file pointer.
