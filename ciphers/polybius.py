red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"


def encrypt(currentArray: list[str], reverse: bool) -> tuple[str, list[str]]:
    out = None
    if reverse:
        string = input("Enter the string to decrypt: ")
        string = string[:-(len(string) % 2)]
        out = ""
        for i in range(0, len(string), 2):
            if string[i] == ".":
                out += string[i + 1]
            elif string[i:i+1].isnumeric():
                out += currentArray[int(string[i])-1][int(string[i+1])-1]
    else:
        polybius = {}
        for i, row in enumerate(currentArray):
            for j, column in enumerate(row):
                polybius[column] = f"{i+1}{j+1}"
        string = input("Enter the string to encrypt: ")
        out = ""
        for i in string:
            if i in polybius:
                out += polybius[i]
            else:
                out += "." + i
    return out, currentArray
