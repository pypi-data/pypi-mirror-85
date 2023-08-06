Module parsrt
=============
A minimalistic (100LOC) library to read SRT files into a workable format.

Simply provides a way to convert SRT strings into Sub objects (via the parse 
functions) and vice versa (via the Sub class' __str__ function).
By avoiding regex it gets speeds around 50% faster than the fastest python 
SRT/Subtitle library I could find (cdown/srt).
Install via: pip install parsrt

Functions
---------

    
`parse_file(path, encoding='ascii')`
:   Reads a file and converts the contents into an Sub object array.
    
    Args:
        path: The path the SRT file is located at.
        encoding: The encodding of the file (same as with open()).
    
    Returns:
        An Sub object array.

    
`parse_str(srt)`
:   Converts a string into an Sub object array.
    
    Args:
        srt: A valid SRT string.
    
    Returns:
        An Sub object array.
    
    Raises:
        ValueError: Invalid SRT string.

Classes
-------

`Sub(index, time, text)`
:   Subtitle info object.
    
    Attributes:
        index: An SRT index value.
        time: A tuple containing the start and end timestamps as timedelta objects.
        text: A string value containing the subtitle's text.
