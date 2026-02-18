import task6

#Import the read me and then test it for word count
#This will test that words exist and its higher than 0
def test_word_count():
    count = task6.count_words("task6_read_me.txt")
    assert count > 0
