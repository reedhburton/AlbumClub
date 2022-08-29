class Menu:
    def __init__(self, people, genres):
        self.lookBack = 1  # Prevent same categories from repeating
        self.albumType = "LP"
        self.people = list(people.keys()).sort()
        self.genres = genres.keys()
        self.peopleFilter = people
        self.genreFilter = genres

    def main_menu(self):
        print(
            "Please select select one of the following options:"
            + "\n[0] Select a new album"
            + f"\n[1] Edit Album Type (Currently: {self.albumType})"
            + f"\n[2] Edit the number of weeks to look back (Currently: {self.lookBack})"
            + "\n[5] Close"
        )

    def setAlbumType(self):
        print(
            "Select Album Type:"
            + "\n[0] Single"
            + "\n[1] EP"
            + "\n[2] LP"
            + "\n[3] Compilation"
        )
        selection = input(">: ")
        if selection == "0":
            self.albumType = "Single"
        elif selection == "1":
            self.albumType = "EP"
        elif selection == "2":
            self.albumType = "LP"
        elif selection == "3":
            self.albumType = "Compilation"
        else:
            print(f"'{selection}' is not a valid selection.")

    def setLookBack(self, newLookBack):
        try:
            lookBack = int(newLookBack)
        except ValueError:
            print(f"'{newLookBack}' is not a valid number")
        if lookBack < 0:
            print(f"'{lookBack}' is out of range")
        self.lookBack = lookBack
