import math

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"


bases = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz=+"


def convertToBase(number: int, base: int, padding: int) -> str:
    """
    INPUT:   The number to convert, the base to convert to, and the padding
    FUNCTION: Converts a number to a string in a given base
    OUTPUT:  The number in the given base
    """
    out = ""
    while number > 0:
        out = bases[number % base] + out
        number = math.floor(number / base)
    out = "0" * max(0, padding - len(out)) + out
    return out


def generateExtendedPolybius(currentArray: list[str], base: int) -> dict[str, str]:
    """
    INPUT:   The grid to use, and the base to use
    FUNCTION: Generates the extended Polybius square
    OUTPUT:  The encryption key, and the maximum number of characters for the row and column (e.g. 3 binary characters to show 6)
    """
    # Using logs, calculate the maximum number of characters for the row and column
    maxCharsForRow = math.ceil(math.log(len(currentArray), int(base)))
    maxCharsForColumn = math.ceil(math.log(len(currentArray[0]), int(base)))
    polybius = {}
    for i, row in enumerate(currentArray):
        for j, column in enumerate(row):
            # For each character, convert the row and column to the base and add it to the dictionary
            rowString = convertToBase(i, int(base), maxCharsForRow)
            columnString = convertToBase(j, int(base), maxCharsForColumn)
            polybius[column] = rowString + columnString
    return polybius, maxCharsForRow, maxCharsForColumn


def encrypt(currentArray: list[str], reverse: bool) -> tuple[str, list[str]]:
    """
    INPUT:   The grid to use, and if decryption is being used
    FUNCTION: Encrypts or decrypts a string using the Extended Polybius cipher, which uses a base other than 10
    OUTPUT:  The encrypted/decrypted string, and the grid
    """
    out = None
    if reverse:
        # If decrypting
        string = input("Enter the string to decrypt: ")
        # Count the sums of every character to calculate the base
        checkSum = sum([bases.index(n) for n in string[1:] if n in bases] + [0])
        base = None
        # Find which base it is by checking using with the equation below
        for i in range(2, len(bases)):
            if bases[(checkSum + i) % len(bases)] == string[0]:
                base = i
                break
        if not base:  # Return if the base is invalid
            return "Invalid checksum", currentArray
        # Remove the base character
        string = string[1:]
        # Generate the data required to decrypt
        polybius, maxCharsForRow, maxCharsForColumn = generateExtendedPolybius(currentArray, base)
        out = ""
        for i in range(0, len(string), maxCharsForRow + maxCharsForColumn):
            # For each character, run the decryption similar to a normal Polybius cipher
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
        # If encrypting
        string = input("Enter the string to encrypt: ")
        valid = False
        while not valid:
            # Ask for a valid base. This can be up to the length of the bases string
            base = input("Enter the base to use (Standard bases: 2, 10, 16) or q to go back: ")
            if base == "q":
                # If the user wants to go back, return
                return None, currentArray
            valid = base.isnumeric()
            if valid:
                valid = int(base) > 1 and int(base) <= len(bases)
        out = ""
        # Generate the data required to encrypt
        polybius = generateExtendedPolybius(currentArray, base)[0]
        for i in string:
            # For each character, run the encryption similar to a normal Polybius cipher
            if i in polybius:
                out += polybius[i]
            else:
                out += "." + i
        # Calculate the checksum and the base character
        checkSum = sum([bases.index(n) for n in string[1:] if n in bases] + [0])
        baseNumber = bases[(checkSum + int(base)) % len(bases)]
        # Add it to the string
        out = baseNumber + out
    return out, currentArray
