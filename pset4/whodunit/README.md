### A program that modifies .bitmap image so that it reveals hidden message

# Questions

## What's `stdint.h`?

Library of integer types.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

It determines how much of a space is needed to store an integer. For example, uint8_t is unsigned 8-bit integer. It holds 8 bits and has values ranging from
0 to 2^8 - 1

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE - 1 byte
DWORD - 4 bytes
LONG - 4 bytes
WORD - 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

BM // 0x42 0x4d

## What's the difference between `bfSize` and `biSize`?

bfSize - the size in bytes of BMP file
biSize - the number of bytes required by a structure BITMAPINFOHEADER

## What does it mean if `biHeight` is negative?

That height of the image is counted from top to bottom. If positive - counted from bottom to top.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

In line 24 - if file does not exist, then function returns NULL
In line 32 - if it was not possible to create a file, then function returns NULL

## Why is the third argument to `fread` always `1` in our code?

It means that we want to read the element of data only one time (we specify also, by second argument, how many bytes long that element is)

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

2 
(4 - (3*6) % 4) % 4)

## What does `fseek` do?

Changes location of the file pointer. It helps us to navigate thoughout the file. It uses 3 arguments - file pointer fp, long int offset (by how many BYTES change the pointer position), int from_where (where to start SEEK_SET; SEEK_CUR; SEEK_END)

## What is `SEEK_CUR`?

Its an integer type data; macroinstruction, which instructs that fseek function to count offset from file pointer's current position

## Whodunit?

It was Professor Plum with the candlestick in the library
