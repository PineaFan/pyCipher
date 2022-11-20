import math

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"


bases = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz=+"


def convertToBase(number: int, base: int, padding: int) -> str:
    out = ""
    # Given a number, convert it to the given base
    while number > 0:
        out = bases[number % base] + out
        number = math.floor(number / base)
    out = "0" * max(0, padding - len(out)) + out
    return out


def generateExtendedPolybius(currentArray: list[str], base: int) -> dict[str, str]:
    maxCharsForRow = math.ceil(math.log(len(currentArray), int(base)))
    maxCharsForColumn = math.ceil(math.log(len(currentArray[0]), int(base)))
    polybius = {}
    for i, row in enumerate(currentArray):
        for j, column in enumerate(row):
            rowString = convertToBase(i, int(base), maxCharsForRow)
            columnString = convertToBase(j, int(base), maxCharsForColumn)
            polybius[column] = rowString + columnString
    return polybius, maxCharsForRow, maxCharsForColumn


def encrypt(currentArray: list[str], reverse: bool) -> tuple[str, list[str]]:
    out = None
    if reverse:
        string = input("Enter the string to decrypt: ")
        checkSum = sum([int(n) for n in string[1:] if n.isnumeric()] + [0])
        base = None
        for i in range(2, len(bases)):
            if bases[(checkSum + i) % len(bases)] == string[0]:
                base = i
                break
        if not base:
            return "Invalid checksum", currentArray
        string = string[1:]
        polybius, maxCharsForRow, maxCharsForColumn = generateExtendedPolybius(currentArray, base)
        out = ""
        for i in range(0, len(string), maxCharsForRow + maxCharsForColumn):
            if string[i] == ".":
                out += string[i+1:i+maxCharsForRow+maxCharsForColumn]
            else:
                row = string[i:i+maxCharsForRow]
                column = string[i+maxCharsForRow:i+maxCharsForRow+maxCharsForColumn]
                try:
                    out += list(polybius.keys())[list(polybius.values()).index(row + column)]
                except ValueError:
                    pass

    else:
        string = input("Enter the string to encrypt: ")
        valid = False
        while not valid:
            base = input("Enter the base to use (Standard bases: 2, 10, 16) or q to go back: ")
            if base == "q":
                return None, currentArray
            valid = base.isnumeric()
            if valid:
                valid = int(base) > 1 and int(base) <= len(bases)
        out = ""
        polybius = generateExtendedPolybius(currentArray, base)[0]
        for i in string:
            if i in polybius:
                out += polybius[i]
            else:
                out += "." + i
        checkSum = sum([int(n) for n in out if n.isnumeric()] + [0])
        baseNumber = bases[(checkSum + int(base)) % len(bases)]
        out = baseNumber + out
    return out, currentArray
