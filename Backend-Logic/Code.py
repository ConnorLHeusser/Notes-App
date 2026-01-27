notes = input("Enter new notes here (type e to exit): ")
new_notes = notes
while (new_notes != "e"):
    print("")
    print(notes)
    print("")
    new_notes = input("Enter new notes here (type e to exit): ")
    notes = notes + "  " + new_notes

