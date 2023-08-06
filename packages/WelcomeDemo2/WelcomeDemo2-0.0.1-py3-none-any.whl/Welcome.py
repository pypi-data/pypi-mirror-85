import os 

class Welcome:
    """
    This class writes a string a user inputs into a file on a computer in one function and writes strings in file in another function,
    2 function contained:
            1. Configure() - inputs string in file
            2. Print_welcome_message() - outputs strings in file
    """
    def __init__(self):
        """ 
        Empty constructor
        """
        pass

    def Configure(self, filename):
        """
        The file to be written on is taken as an argument. Using a for loop the file is searched for in path of the computer
        The path searched is the current working director
        Paramerter:
                filename - file to be added string to
        Outputs:
                "File found" or "File not found" 
        """
        word = input("Enter a sentence: ")
        fail = True
        path = os.getcwd()
        for root, dirs, files in os.walk(path):
            if filename in files:
                print("File Found")
                file1 = open(filename, "a")
                file1.write(word)
                file1.flush()
                file1.close()
                print(word + " added to " + filename)
                fail = False
        if fail:
            print("File Not Found")

    def Print_welcome_message(self, filename):
        """
        The file to be read on is taken as an argument. Using a for loop the file is searched for in path of the computer
        The path searched is the current working director
        Paramerter:
                filename - file to be read
        Outputs:
                Content of the file or "File not found"
        """
        fail = True
        path = os.getcwd()
        for root, dirs, files in os.walk(path):
            if filename in files:
                print("File Found")
                file1 = open(filename, "r")
                x = file1.read()
                print(x)
                file1.close()
                fail = False 
        if fail:
            print("File Not Found")



