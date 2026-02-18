#Creates a list of books and students then prints the books
books = [
    ("Shadows Linger", "Glen Cook"),
    ("The Wizards First Rule", "Terry Goodkind"),
    ("Deadhouse Gates", "Steven Erickson"),
    ("The Lightning Thief", "Rick Riordan"),
]

#Student name and id Num
students = {
    "Levi C": 12345678,
    "Tara Reid": 9876543,
    "Sven Olstad": 11223344
}

#Prints the books, leaving out the authors
def threeBooks():
    return books[:3]

#Prints students + ID
def Students():
    return students
