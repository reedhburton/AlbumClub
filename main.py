import pandas as pd
from datetime import datetime
from Album import Album
from Menu import Menu
from AlbumClub import AlbumClub

SERVICE_FILE_PATH = (
    "/Users/Reed/Documents/Programming/cone-inc-album-club-6f68b289cf9d.json"
)
SUGGESTION_FORM = "Cone Inc Album Club - Album Suggestion Form (Responses)"


if __name__ == "__main__":
    print("Welcome to the Cone Inc Album Club!")
    print("###################################")

    club = AlbumClub(SERVICE_FILE_PATH, SUGGESTION_FORM)
    # club.displayWhitelist()
    # club.displayGenreStats()
    # club.displayMemberStats()

    menu = Menu()

    while True:
        menu.main_menu(club.albumType, club.lookBack)
        user_selection = input(">: ")
        if user_selection == "0":
            club.selectAlbum()
        elif user_selection == "1":
            while True:
                menu.setAlbumType()
                user_selection = input(">: ")
                if user_selection == "0":
                    club.albumType = "Single"
                    break
                elif user_selection == "1":
                    club.albumType = "EP"
                    break
                elif user_selection == "2":
                    club.albumType = "LP"
                    break
                elif user_selection == "3":
                    club.albumType = "Compilation"
                    break
                else:
                    print(f"Invalid selection: '{user_selection}'")
                    continue
        elif user_selection == "2":
            while True:
                menu.setLookBack(club.lookBack)
                user_selection = input(">: ")
                try:
                    lookBack = int(user_selection)
                    if lookBack > len(club.played):
                        print(f"Lookback of {lookBack} is too high!")
                        continue
                    else:
                        club.setLookBack(lookBack)
                        club.updateWhitelist
                        break
                except ValueError:
                    print(f"Invalid input: '{user_selection}'")
                    continue
        elif user_selection == "3":
            club.displayMemberStats()
        elif user_selection == "4":
            club.displayGenreStats()
        elif user_selection == "5":
            club.displayWhitelist()
        elif user_selection == "10":
            break
        else:
            print(f"Invalid input: '{user_selection}'")
