from typing import Optional
import time
import random
import math

S32_CHAR = "234567abcdefghijklmnopqrstuvwxyz"
TID_LEN = 13

last_timestamp = 0
timestamp_count = 0
clockid: Optional[int] = None


def s32encode(i: int) -> str:
    s = ""
    while i:
        c = i % 32
        i = math.floor(i / 32)
        s = S32_CHAR[c] + s
    return s


def s32decode(s: str) -> int:
    i = 0
    for c in s:
        i = i * 32 + S32_CHAR.index(c)
    return i


def dedash(string: str) -> str:
    return string.replace("-", "")


class TID:
    def __init__(self, string: str) -> None:
        no_dashes = dedash(string)
        if len(no_dashes) != TID_LEN:
            raise ValueError(f"Poorly formatted TID: {len(no_dashes)} length")
        self.str = no_dashes

    @classmethod
    def next(cls, prev: Optional["TID"] = None) -> "TID":
        global last_timestamp, timestamp_count, clockid

        current_time = max(int(time.time() * 1000), last_timestamp)
        if current_time == last_timestamp:
            timestamp_count += 1
        last_timestamp = current_time
        timestamp = current_time * 1000 + timestamp_count

        # the bottom 32 clock ids can be randomized & are not guaranteed to be collision resistant
        # we use the same clockid for all tids coming from this machine
        if clockid is None:
            clockid = math.floor(random.random() * 32)

        tid = cls.from_time(timestamp, clockid)
        if not prev or tid.newer_than(prev):
            return tid
        return cls.from_time(prev.timestamp() + 1, clockid)

    @classmethod
    def next_str(cls, prev: Optional[str] = None) -> str:
        return cls.next(cls.from_str(prev) if prev else None).to_string()

    @classmethod
    def from_time(cls, timestamp: int, clockid: int) -> "TID":
        # base32 encode with encoding variant sort (s32)
        string = f"{s32encode(timestamp)}{s32encode(clockid).rjust(2, '2')}"
        return cls(string)

    @classmethod
    def from_str(cls, string: str) -> "TID":
        return cls(string)

    @staticmethod
    def oldest_first(a: "TID", b: "TID") -> int:
        return a.compare_to(b)

    @staticmethod
    def newest_first(a: "TID", b: "TID") -> int:
        return b.compare_to(a)

    @staticmethod
    def is_tid(string: str) -> bool:
        return len(dedash(string)) == TID_LEN

    def timestamp(self) -> int:
        return s32decode(self.str[:11])

    def clockid(self) -> int:
        return s32decode(self.str[11:13])

    def formatted(self) -> str:
        string = self.to_string()
        return f"{string[:4]}-{string[4:7]}-{string[7:11]}-{string[11:13]}"

    def to_string(self) -> str:
        return self.str

    # newer > older
    def compare_to(self, other: "TID") -> int:
        if self.str > other.str:
            return 1
        if self.str < other.str:
            return -1
        return 0

    def equals(self, other: "TID") -> bool:
        return self.str == other.str

    def newer_than(self, other: "TID") -> bool:
        return self.compare_to(other) > 0

    def older_than(self, other: "TID") -> bool:
        return self.compare_to(other) < 0

    def __str__(self) -> str:
        return self.to_string()
