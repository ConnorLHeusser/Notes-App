#refactored to force notes as string
notes = input(str("Please enter what notes you would like to enter (type exit to exit): "))
newNotes = ""
#decluttered while loop with better logic 
while (newNotes!= "exit"):
    newNotes = input(str("Please continue entering notes (Type exit to exit): "))
    notes += " " + newNotes
    print(f"Notes so far: {notes}")

print(f"Final notes: {notes}")