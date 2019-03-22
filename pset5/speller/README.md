### A program that spell-checks a file

# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

An imaginary lung disease caused by inhaling very fine ash and sand dust :)

## According to its man page, what does `getrusage` do?

Returns resource usage for one of several processes: calling process, all children of calling processes or the calling thread.
This resource usage is returned to the structure of a particular form pointed by a pointer.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

So that these memory parts could be used by all functions in the program.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

'Main' takes in 2 or 3 variables from the command line - the dictionary that text will be compared against, and the text.
The dictionary is loaded and the file (text) is opened for reading. Char word size of [LENGHT + 1] is initialized - for storing the whole word, plus '\0'.
Then, as long as EOF of the file(text) is not reached, we continue to go after each word in a text and check it.
First, it is checked if characters are alphabetical / apostrophes. If yes, we store those characters, each after each in an array pointed by "word".
Strings too long to be words are ignored by remaining the index value 0. If the program finds the digit it ignores that string also.
Then, the program appends the word by '\0' (calculates the checking time on the way) and prints it, if it is misspelled.
Index is set to zero for a new word, and the loop goes on for another word, until EOF.
Then the text is closed, the time for calculating resource usage for calculating the size of the dictionary, and the programm prints time values, which indicate how fast the program was.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

We wouldn't be able to determine if the string we got by 'fscanf' is not bigger than lenght of words we accept.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

So that, later in the code, it is not possible to change variables' values these pointers point to.
This is needed to ensure that the word and the whole dictionary, after read, both remain unchanged.
