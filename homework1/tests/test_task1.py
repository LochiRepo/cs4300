#Bring in the test
import task1

#Run the main function
def test_main_output(capsys):
    task1.main()

#Test the print for Hello World
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, World!"
