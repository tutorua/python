# cd .\snippets
# python file_read.py  
# os, pathlib, shutil
import os
from pathlib import Path


file = "example.txt"

script_dir = os.getcwd()
print(f"Script dir is: ", {script_dir})

file_name = os.path.join(script_dir, file)
print(f"File name is: ", {file_name})

path = Path("examplew.txt")
print(f"Script for write test file was found at: ", {path})

if path.is_file():
    path.unlink()  # delete the file
    print("Script for write test file was deleted")


with open(file_name, "r") as file:

    # data = file.read()
    # print(data)
    # lines = file.readlines() # returns a list of strings
    # print(lines)
    # line = file.readline(5) # stops reading after the first 5 symbols
    # print(line)
    line = file.readline() # stops reading after the first line
    print(line)


with open("examplew.txt", "w") as file:

    file.write("Hello, world!\n")


with open("examplew.txt", "r") as file:
    file.seek(10)  # move the pointer 10 bytes from the beginning
    data = file.read()
    print(data)

    