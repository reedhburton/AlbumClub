from ast import Raise
from msilib.schema import Error


class Album:
    def __init__(self, Entry):
        fields = 10  # Increase if you change the number of fields
        if len(Entry) < fields:
            Raise("Invalid entry.")

        self.Timestamp = Entry[0]
        self.Email = Entry[1]
        self.Title = Entry[2]
        self.Artist = Entry[3]
        self.Genre = Entry[4]
        self.OtherGenre = Entry[5]
        self.Listened = Entry[6]
        self.Significance = Entry[7]
        self.Type = Entry[8]
        self.Week = Entry[9]

    def __str__(self):
        return f"'{self.Title}' by {self.Artist}"
