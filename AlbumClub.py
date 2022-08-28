import pygsheets
import pandas as pd
from Album import Album


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
    albums = getData()
    Rock = [album for album in albums if album.Genre == "Rock"]

    for album in Rock:
        print(album)
