from srenamer import MovieDatabase, Renamer


def main():
    key = True
    db = MovieDatabase.get_api_key()
    while key:
        renamer = Renamer.getwd()
        db.search()
        renamer.rename(db.episodes)
        answer = input("Continiue? (yes/no): ")
        if answer.lower() in ["yes", "y"]:
            continue
        else:
            key = False
            print("Bye, bye!")


if __name__ == "__main__":
    main()
