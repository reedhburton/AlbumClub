from tkinter import W
import pygsheets
from Album import Album
from Menu import Menu
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import random

MEMBER_LOOKBACK = 7
GENRE_LOOKBACK = 5
DEFAULT_GENRES = {
    "Rock",
    "Country",
    "Folk",
    "Rap",
    "Pop",
    "Jazz",
    "Metal / Hard Rock",
    "Punk",
    "Funk",
    "R&B",
    "2010's",
    "2000's",
    "90s",
    "80s",
    "70s",
    "60s",
    "50s",
    "40s",
    "Big Band / 20-30s",
    "1910s and before",
    "Latin / Mariachi",
    "Accapella",
    "Electronic",
    "Alternative",
    "Instrumental / Classical",
    "Musical / Show Tune",
    "Indie",
}


class AlbumClub:
    def __init__(self, service_file, suggestion_form):
        # Fields
        self.genres = set()
        self.members = set()
        self.played = []
        self.unplayed = []
        self.albums = []
        self.memberLookBack = MEMBER_LOOKBACK
        self.genreLookBack = GENRE_LOOKBACK
        self.albumType = "LP"
        self.albumTypes = {"LP", "EP", "Compilation", "Single"}

        self.genres.update(DEFAULT_GENRES)

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
        if self.memberLookBack > len(self.played) or self.genreLookBack > len(
            self.played
        ):
            raise ("lookBack larger than number of played albums.")

        self.genreWhitelist = self.genres.copy()
        self.memberWhitelist = self.members.copy()

        for album in self.played[: self.memberLookBack]:
            self.memberWhitelist.remove(album.Member)

        for album in self.played[: self.genreLookBack]:
            self.genreWhitelist.remove(album.Genre)

    def displayWhitelist(self):
        print("Members:")
        for index, member in enumerate(self.members):
            print(f"[{index}] {member}: {member in self.memberWhitelist}")
        print("Genres:")
        for index, genre in enumerate(self.genres):
            print(f"[{index}] {genre}: {genre in self.genreWhitelist}")

    def selectAlbum(self):
        validAlbums = []
        input("Press enter to continue...")
        validTypes = {self.albumType}
        if self.albumType == "LP":
            user_input = input("Include compilations in pool? [Y/n]>: ")
            if user_input.lower() != "n":
                validTypes.add("Compilation")

        # Genres
        genreList = list(self.genreWhitelist)
        order = list(range(0, len(genreList)))
        random.shuffle(order)
        for index in order:
            winningGenre = genreList[index]
            validAlbums = [
                album
                for album in self.unplayed
                if album.Genre == winningGenre
                and album.Member in self.memberWhitelist
                and album.Type in validTypes
            ]
            if len(validAlbums) != 0:
                break
        if len(validAlbums) == 0:
            print("No valid albums!")
            return

        input(f"Winning genre is: {winningGenre}. Press enter to continue.")

        member_pool = set()
        for album in validAlbums:
            member_pool.add(album.Member)

        index = random.randint(0, len(member_pool) - 1)
        winningMember = list(member_pool)[index]

        winnerPool = list(filter(lambda x: x.Member is winningMember, validAlbums))

        print(f"Winning member: {winningMember}")
        print("Valid albums:")
        for index, album in enumerate(winnerPool):
            print(f"[{index}]: {album}")

        user_input = input("Would you like to randomly select a winner? [Y/n] >: ")

        if user_input.lower() == "n":
            print(
                f"Congrats to {winningMember} for being selected for this week's album club nominee!"
            )
        else:
            index = random.randint(0, len(winnerPool) - 1)
            winner = winnerPool[index]
            print(
                f"Congrats to {winningMember} for being selected for this week's album club nominee!"
                + f"\nThe winning album is {winner}!"
            )

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
            print(f"[{index}] {member}: {picked + unpicked} / {picked} / {unpicked}")

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
            print(f"[{index}] {genre}: {picked + unpicked} / {picked} / {unpicked}")

    def setMemberLookBack(self, newLookBack):
        try:
            lookBack = int(newLookBack)
            if lookBack < 0:
                print(f"'{lookBack}' is out of range")
            self.memberLookBack = lookBack
            self.updateWhitelist()
        except ValueError:
            print(f"'{newLookBack}' is not a valid number")

    def setGenreLookBack(self, newLookBack):
        try:
            lookBack = int(newLookBack)
            if lookBack < 0:
                print(f"'{lookBack}' is out of range")
            self.genreLookBack = lookBack
            self.updateWhitelist()
        except ValueError:
            print(f"'{newLookBack}' is not a valid number")

    def setAlbumType(self, albumType):
        self.albumType = albumType
