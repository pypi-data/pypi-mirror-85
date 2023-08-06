from os import system as _exec
from os import listdir as _listdir
from os import getcwd as _getcwd
from os.path import isdir as _isdir
from os.path import join as _join

from platform import system as _system

def clear(*args):
    if _system() == "Windows":
        _exec("cls")
    else:
        _exec("clear")

def ls(*args):
    if len(args) == 0:
        for i in _listdir():
            if _isdir(_join(_getcwd(), i)):
                print(f"{i} ..")
            else:
                print(f"{i} .")
    elif len(args) == 1:
        if _isdir(args[0]):
            for i in _listdir():
                if _isdir(_join(_getcwd(), i)):
                    print(f"{i} ..")
                else:
                    print(f"{i} .")
        else:
            print("Directory not found")
    else:
        print("Too much arguments")