from os import system


def update_status(message, perc, bookings_found):
    print(message)
    progress_bar(perc)
    if bookings_found is not None:
        print("Bookings found: " + str(bookings_found) + "\n")


def progress_bar(percentage):
    bar = ""

    if percentage > 100:
        percentage = 100
    elif percentage < 0:
        percentage = 0

    for i in range(percentage):
        bar = bar + "#"

    for j in range(100 - percentage):
        bar = bar + "_"

    if percentage == 100:
        print("[" + bar + "] (100%)")
        return
    if percentage < 10:
        print("[" + bar + "] (  " + str(percentage) + "%)")
        return
    print("[" + bar + "] ( " + str(percentage) + "%)")
