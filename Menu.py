class Menu:
    def __init__(self):
        pass

    def main_menu(self, albumType, memberLookBack, genreLookBack):
        print(
            "Please select select one of the following options:"
            + "\n[0] Select a new album"
            + f"\n[1] Edit Album Type (Currently: {albumType})"
            + f"\n[2] Edit the number of weeks to look back for members (Currently: {memberLookBack})"
            + f"\n[3] Edit the number of weeks to look back for genres (Currently: {genreLookBack})"
            + f"\n[4] Display member info"
            + f"\n[5] Display genre info"
            + f"\n[6] Display whitelist info"
            + "\n[10] Close"
        )

    def setAlbumType(self):
        print(
            "Select Album Type:"
            + "\n[0] Single"
            + "\n[1] EP"
            + "\n[2] LP"
            + "\n[3] Compilation"
        )

    def setLookBack(self, lookBack):
        print(f"Input new look back value. Current look back: {lookBack}")
