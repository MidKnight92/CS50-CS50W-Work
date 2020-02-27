import sys

def main():
    height = prompt()
    if height:
        pyramid(height)
    else:
        sys.exit()

def prompt():
    height = input("Height: ")
    if not (height.isdigit()) or int(height) not in range(1,9):
        main()
    else:
        return int(height)

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