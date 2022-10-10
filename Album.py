from ast import Raise
from msilib.schema import Error
from datetime import datetime

NAMES = {
    "reedhburton@gmail.com": "Reed",
    "karenagarcia98@gmail.com": "Kdog",
    "emg429@nau.edu": "Elle",
    "benjamin839@gmail.com": "Ben",
    "aguilarjr.josel@gmail.com": "Jose",
    "emmibear88@gmail.com": "Emmi",
    "aiannacone88@gmail.com": "Cone",
    "anthony.g.iannacone@gamil.com": "Cone",
    "anthony.g.iannacone@gmail.com": "Cone",
    "emma.busstop949@gmail.com": "Emma",
    "sky.chilek@gmail.com": "Sky",
    "portis.avrey@gmail.com": "Avery",
}


class Album:
    def __init__(self, Entry):
        fields = 10  # Increase if you change the number of fields
        email = Entry[1].lower().strip()

        if len(Entry) < fields:
            Raise("Invalid entry.")

        self.Timestamp = datetime.strptime(Entry[0], "%m/%d/%Y %H:%M:%S")
        self.Member = email if email not in NAMES else NAMES[email]
        self.Title = Entry[2].title().strip()
        self.Artist = Entry[3].title().strip()
        self.Genre = Entry[4].strip()
        self.OtherGenre = Entry[5].strip()
        self.Listened = Entry[6] in ("Yes")
        self.Significance = Entry[7]
        self.Type = Entry[8]
        if Entry[9] == "":
            self.Week = None
        else:
            self.Week = datetime.strptime(Entry[9], "%m/%d/%Y").date()

    def __str__(self):
        return f"'{self.Title}' by {self.Artist}"

    def __repr__(self):
        return f"'{self.Title}' by {self.Artist}"
