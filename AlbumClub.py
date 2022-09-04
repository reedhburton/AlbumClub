import pygsheets
from Album import Album
from Menu import Menu
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import random

LOOKBACK = 2


class AlbumClub:
    def __init__(self, service_file, suggestion_form):
        # Fields
        self.genres = set()
        self.members = set()
        self.played = []
        self.unplayed = []
        self.albums = []
        self.lookBack = LOOKBACK
        self.albumType = "LP"
        self.albumTypes = {"LP", "EP", "Compilation", "Single"}

        random.seed()
        # define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            service_file,
            scope,
        )
        client = gspread.authorize(creds)

        wks = client.open(suggestion_form).sheet1
        entries = wks.get_values()[1:]

        for entry in entries:
            album = Album(entry)
            self.albums.append(album)
            # Genre
            genre = album.Genre
            other = album.OtherGenre
            if genre == "Other (Please see next question)":
                genre = other
            self.genres.add(genre)
            # Check if it has already been played
            if album.Week == None:
                self.unplayed.append(album)
            else:
                self.played.append(album)

            # Get data on people
            person = album.Member
            self.members.add(person)

        self.played.sort(reverse=True, key=lambda album: album.Week)

        self.updateWhitelist()

        raw_data = wks.get_all_records()
        self.df = pd.DataFrame.from_dict(raw_data)

    def updateWhitelist(self):
        if self.lookBack > len(self.played):
            raise ("lookBack larger than number of played albums.")

        self.genreWhitelist = self.genres.copy()
        self.memberWhitelist = self.members.copy()
        print(self.played)
        for album in self.played[: self.lookBack]:
            self.memberWhitelist.remove(album.Member)
            self.genreWhitelist.remove(album.Genre)

    def displayWhitelist(self):
        print("Members:")
        for index, member in enumerate(self.members):
            print(f"[{index}] {member}: {member in self.memberWhitelist}")
        print("Genres:")
        for index, genre in enumerate(self.genres):
            print(f"[{index}] {genre}: {genre in self.genreWhitelist}")

    def selectAlbum(self):
        index = random.randint(0, len(self.memberWhitelist) - 1)
        winningMember = list(self.memberWhitelist)[index]

        validAlbums = [
            album
            for album in self.unplayed
            if album.Genre in self.genreWhitelist
            and album.Member is winningMember
            and album.Type is self.albumType
        ]
        index = random.randint(0, len(validAlbums) - 1)
        winner = validAlbums[index]
        print(winningMember)
        print(winner)

    def displayMemberStats(self):
        type_filter = lambda x: x.Type == self.albumType
        played = list(filter(type_filter, self.played))
        unplayed = list(filter(type_filter, self.unplayed))
        print(
            f"Members stats (Total {self.albumType}s: {len(played) + len(unplayed)}): Total Submitted / Total Selected / Total Unselected"
        )
        for index, member in enumerate(self.members):
            picked = len([album for album in played if album.Member == member])
            unpicked = len([album for album in unplayed if album.Member == member])
            print(
                f"[{index}] {member}: {picked + unpicked} / {picked} / {unpicked - picked}"
            )

    def displayGenreStats(self):
        type_filter = lambda x: x.Type == self.albumType
        played = list(filter(type_filter, self.played))
        unplayed = list(filter(type_filter, self.unplayed))
        print(
            f"Genre stats (Total {self.albumType}s: {len(played) + len(unplayed)}): Total Submitted / Total Selected / Total Unselected"
        )
        for index, genre in enumerate(self.genres):
            picked = len([album for album in played if album.Genre == genre])
            unpicked = len([album for album in unplayed if album.Genre == genre])
            print(
                f"[{index}] {genre}: {picked + unpicked} / {picked} / {unpicked - picked}"
            )

    def setLookBack(self, newLookBack):
        try:
            lookBack = int(newLookBack)
            if lookBack < 0:
                print(f"'{lookBack}' is out of range")
            self.lookBack = lookBack
            self.updateWhitelist()
        except ValueError:
            print(f"'{newLookBack}' is not a valid number")

    def setAlbumType(self, albumType):
        self.albumType = albumType
