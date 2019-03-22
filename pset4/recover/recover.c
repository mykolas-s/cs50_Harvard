#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char* argv[])
{
    // ensure that there is only one command line argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image \n");
        return 1;
    }

    // open file for reading
    FILE *infile = fopen(argv[1], "r");

    // ensure that the file can be opened for reading
    if (infile == NULL)
    {
        fprintf(stderr, "Could not open %s \n", argv[1]);
        return 2;
    }

    // counter for counting a number of .jpegs
    int counter = 0;
    // create new jpeg
    char filename[8];
    sprintf(filename, "%03i.jpg", counter); // assign value of counter to filename
    FILE *outfile = fopen(filename, "w");
    fclose(outfile);

    uint8_t buffer[512]; // get memory for reading
    int* p = NULL;

    do
    {
        // read 512B into a buffer
        int a = fread(&buffer, 1, 512, infile);
        p = &a; // get the address of a and assign it to *p
        if (*p == 512)
        {

        // if it is a start of a new jpeg
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            if (counter > 0)
            {
               fclose(outfile); // close old jpeg
            }
            // create new jpeg
            sprintf(filename, "%03i.jpg", counter);
            outfile = fopen(filename, "w");
            fwrite (&buffer, 1, 512, outfile);
            counter++;
        }

        // check if we have already found a jpeg
        else
        {
            if (counter > 0)
                fwrite (&buffer, 1, 512, outfile);
        }
        }
    }
    while (*p == 512);
    fclose (infile);
    fclose (outfile);
    return 0;
}