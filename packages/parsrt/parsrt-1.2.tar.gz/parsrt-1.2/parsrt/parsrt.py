"""A minimalistic (100LOC) library to read SRT files into a workable format.

Simply provides a way to convert SRT strings into Sub objects (via the parse 
functions) and vice versa (via the Sub class' __str__ function).
By avoiding regex it gets speeds around 50% faster than the fastest python 
SRT/Subtitle library I could find (cdown/srt).
Install via: pip install parsrt
"""

from datetime import timedelta

class Sub:
    """Subtitle info object.

    Attributes:
        index: An SRT index value.
        time: A tuple containing the start and end timestamps as timedelta objects.
        text: A string value containing the subtitle's text.
    """

    __slots__ = ["index", "time", "text"]

    def __init__(self, index, time, text):
        self.index = index
        self.time = time
        self.text = text

    def __str__(self):
        def td_to_str(td):
            s = td.total_seconds()
            ms = (s%1)*1000
            m = s/60
            h = m/60
            s = s%60
            return "%02d:%02d:%02d,%03d" % (h, m, s, ms)

        def time_to_str(time):
            return td_to_str(time[0]) + " --> " + td_to_str(time[1]) + " "

        return str(self.index) + "\n" + time_to_str(self.time) + "\n" + self.text + "\n\n"

def parse_str(srt):
    """Converts a string into an Sub object array.

    Args:
        srt: A valid SRT string.

    Returns:
        An Sub object array.

    Raises:
        ValueError: Invalid SRT string.
    """

    def parse_time(timestr):
        def parse_timestamp(timestamp):
            return timedelta(
                        hours=int(timestamp[0:2]),
                        minutes=int(timestamp[3:5]),
                        seconds=int(timestamp[6:8]),
                        milliseconds=int(timestamp[9:12])
                    )

        timestamps = timestr.strip().split(" --> ")
        return (
            parse_timestamp(timestamps[0]),
            parse_timestamp(timestamps[1]),
        )

    def parse_sub(sub):
        lines = sub.split("\n")
        if len(lines) < 2:
            raise ValueError(f"Invalid SRT input: {lines}.")

        return Sub(
            index = int(lines[0]),
            time = parse_time(lines[1]),
            text = "\n".join(lines[2:])
        )

    return (parse_sub(sub) for sub in srt.split("\n\n"))

def parse_file(path, encoding="ascii"):
    """Reads a file and converts the contents into an Sub object array.

    Args:
        path: The path the SRT file is located at.
        encoding: The encodding of the file (same as with open()).

    Returns:
        An Sub object array.
    """

    with open(path, "r", encoding=encoding) as srt:
        return parse_str(srt.read().strip())
