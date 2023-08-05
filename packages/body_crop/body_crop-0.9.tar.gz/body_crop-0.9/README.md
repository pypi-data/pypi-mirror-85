# body
Small utility for cropping a text file.

Created this because there is no good way use common unix utilities to crop a file
down to some portion of the middle. In particular, there isn't a good way to remove
a specified number of lines from the end of a file without first knowing the number
of lines in the file. Though, this can be done, it would require multiple passes
through a file. For a stream, multiple passes would be impossible unless the stream
is first saved to a file, which may not be reasonable depending on the size of the 
stream.

Use is simple as you provide the number of lines to trim from the head and tail of 
the file, along with the file to be cropped. If no file is provided, then it will
operate on stdin.

Example:

body.py -h 2 -t 3 file.txt  <-- Removes the first 2 and last 3 lines from the file

