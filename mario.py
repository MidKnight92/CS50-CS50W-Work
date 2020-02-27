import sys
from cs50 import get_int

def main():
    height = prompt()
    if height:
        pyramid(height)
    else:
        sys.exit()

def prompt():
    while True:
        height = get_int("Height: ")
        if height > 0 and height < 9:
            break
    return height

def pyramid(height):
    for i in range(height):
        n = height - i
        for j in range(n):
            print(end=" ")
        for k in range(i + 1):
            print("#", end="")
        print(" ")


if __name__ == "__main__":
    main()