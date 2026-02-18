#This reads a file and counts the # of words
def ctWord(filename):

#Opens a file and starts reading
    with open(filename, "r") as book:
        text = book.read()

#Splits the text so it only hads individual words
    return len(text.split())
