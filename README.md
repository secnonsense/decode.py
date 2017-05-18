# decode.py
Python script for decoding Base64, Url Encoding and ROT encoding.  

Switches can be used to decode a string (must use quotes if there are spaces in the string) or if no switch is supplied the script will attempt to guess the encoding type based on character-set and some math and will decode accordingly.  If the string has multiple layers of encoding, it will continue to attempt decoding until it finds that there are no guesses or comes up with what it believes to be a best guess.   This can lead to an infinite loop if output criteria continues to match possible encoding types.

-h help screen

usage: decode.py [-h] [-b] [-u] [-r] TEXT

positional arguments:
  TEXT             Enter a string to decode in quotes

optional arguments:
  -h, --help       show this help message and exit  
  -b, --base64     For base64 decoding  
  -u, --urldecode  For URL decoding  
  -r, --ROTdecode  For rot decoding  
