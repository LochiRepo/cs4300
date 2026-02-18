import task5

#Test specific book in the array, this one is Shadows Linger
def test_books():
    books = task5.books()
    assert len(books) == 3
    assert books[0][0] == "Shadows Linger"

#Test the top student, which is me
def test_student_dictionary():
    students = task5.students()
    assert students["Levi C"] == 12345678
