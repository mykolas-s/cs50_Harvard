#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include "helpers.h"
#include <math.h>
#include <string.h>

// convert a fraction formatted as x/y to eighths
int duration(string fraction)
{
    if (fraction[0] == '1')
    {
        if (fraction[2] == '8')
        {
            return 1;
        }
        else if (fraction[2] == '4')
        {
            return 2;
        }
        else if (fraction[2] == '2')
        {
            return 4;
        }
        else if (fraction[2] == '1')
        {
            return 8;
        }
    }
    else if (fraction[0] == '3' && fraction[2] == '8')
    {
        return 3;
    }
    else
    {
        return 0;
    }
    return 0;
}

// calculate frequency (in Hz) of a note
#define A4 440
int frequency(string note)
{
    int n = 0;
    const string NOTES[] = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"};
    if (strcmp(note, "A4") == 0)
    {
        return 440;
    }

    // calculate octave if note lenght = 2
    if (strlen(note) == 2)
    {
        int octave = atoi(&note[1]); // convert octave number from string to integer
        n += (octave - 4) * 12;
    }

    // calculate octave if xnote lenght = 3
    else if (strlen(note) == 3)
    {
        int octave = atoi(&note[2]);
        n += (octave - 4) * 12;

    // calculate accidentals
    if (note[1] == '#')
    {
        n += 1;
    }
        else if (note[1] == 'b')
    {
        n -= 1;
    }
    }
    else
    {
        printf("Wrong usage \n");
        return 1;
    }

    // linear search. calculate note in octave
    for (int c = 0, j = 12; c < j; c++)
    {
        if (note[0] == NOTES[c][0])
        {
            n += c - 9; // 9 here because "A" is 10th element of the array
            break;
        }
    }
    double f = round((pow(2, (double) n / 12)) * A4);
    return f;
}

// determine whether a string represents a rest
bool is_rest(string s)
{
    if (strncmp(s, "", 1))
    {
        return false;
    }
    else
    {
        return true;
    }
}