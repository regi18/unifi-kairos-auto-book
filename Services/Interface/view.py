from os import system


def ask_for_command():
    print("WELCOME TO KAIROS BOOKER SERVICE!")
    print("================================================================")
    print("Please choose an option to start:")
    print("1. Make new lesson(s) booking(s)")
    print("2. Make new study room(s) booking(s)")
    print("3. View your booking(s)")
    print("\nPress ENTER or insert something else to close the program")
    print("================================================================")

    return input("Your choice: ")
