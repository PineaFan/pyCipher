red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"


def encrypt(currentArray: list[str], reverse: bool) -> tuple[str, list[str]]:
    """
    INPUT:   The grid to use, and if decryption is being used
    FUNCTION: Encrypts or decrypts a string using the Polybius square
    OUTPUT:  The encrypted/decrypted string, and the grid
    """
    out = None
    if reverse:
        # If decrypting
        string = input("Enter the string to decrypt: ")
        # Ensure string has an even number of characters by removing the last one if it doesn't
        string = string[:-1] if len(string) % 2 != 0 else string
        out = ""
        for i in range(0, len(string), 2):
            # If its a full stop, just add the next character
            if string[i] == ".":
                out += string[i + 1]
            elif string[i:i+1].isnumeric():
                # If the first character is a number, add the next character to the end of the string
                out += currentArray[int(string[i])-1][int(string[i+1])-1]
    else:
        # If encrypting, generate a key of the letters, and their corresponding numbers in the grid
        polybius = {}
        for i, row in enumerate(currentArray):
            for j, column in enumerate(row):
                polybius[column] = f"{i+1}{j+1}"
        # Ask for the string to encrypt
        string = input("Enter the string to encrypt: ")
        out = ""
        for i in string:
            if i in polybius:  # If its in the grid, add its index to the output
                out += polybius[i]
            else:  # Otherwise, add a full stop and the character
                out += "." + i
    return out, currentArray
