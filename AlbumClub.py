import pygsheets
import pandas as pd
from datetime import datetime
from Album import Album
from Menu import Menu


def getData():
    # authorization
    gc = pygsheets.authorize(
        service_file="/Users/Reed/Documents/Programming/cone-inc-album-club-6f68b289cf9d.json"
    )

    # open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open("Cone Inc Album Club - Album Suggestion Form (Responses)")

    # select the first sheet
    wks = sh[0]

    entries = wks.get_all_values(
        include_tailing_empty=True, include_tailing_empty_rows=False
    )[1:]

    albums = []

    for entry in entries:
        albums.append(Album(entry))

    return albums


if __name__ == "__main__":
    print("Welcome to the Cone Inc Album Club!")
    print("###################################")
    albums = getData()

    genres = {}
    people = {}
    played = []
    unplayed = []

    # Iterate through all albums
    for album in albums:
        # Genre
        genre = album.Genre
        other = album.OtherGenre
        if genre == "Other (Please see next question)":
            genre = other
        if genre not in genres:
            genres[genre] = 1
        else:
            genres[genre] += 1

        # Get data on people
        person = album.Name
        if person not in people:
            people[person] = 1
        else:
            people[person] += 1

        # Check if it has already been played
        if album.Week == None:
            unplayed.append(album)
        else:
            played.append(album)

    played.sort(reverse=False, key=lambda album: album.Week)
    print(people)

    menu = Menu(people, genres)
    user_input = ""

    menu.main_menu()

    selected = [
        album
        for album in albums
        if album.Genre == "Instrumental / Classical"
        and album.Type == "LP"
        and album.Week == ""
    ]
