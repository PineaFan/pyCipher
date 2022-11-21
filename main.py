import os
import math
from ciphers.transform import encrypt as encryptTransform
from ciphers.polybius import encrypt as encryptPolybius
from ciphers.extendedPolybius import encrypt as encryptExtendedPolybius

close = False  # Exit out of the loop
currentArray = ["ABCDE", "FGHIJ", "KLMNO", "PQRST", "UVWXY"]  # The grid stored as an array of strings
lastAdded = None  # Rows added in the last command
lastEdited = None  # Rows edited in the last command
beforeChange = []  # A history of commands to allow undoing
showBefore = None  # Show text before the input

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"


def pad(string: str, length: int, char: str = " ") -> str:
    """
    INPUT:    The string to use, the length to make it, and the separator to use
    FUNCTION: Adds spaces after a string to make it a certain length
    OUTPUT:   The padded string
    """
    return string + (char * max(0, length - len(string)))


def loadArray(filename: str) -> list[str] | None:
    """
    INPUT:    The filename to load
    FUNCTION: Loads the array from a file
    OUTPUT:   The array
    """
    filename = "savedCiphers/" + filename
    # Check if the file exists first
    if not os.path.isfile(filename):
        return None
    with open(filename, "r") as f:
        return f.read().splitlines()


def saveArray(filename: str, currentArray: list[str]) -> None:
    """
    INPUT:    The filename to save, and the array to save
    FUNCTION: Saves the array to a file
    OUTPUT:   None
    """
    filename = "savedCiphers/" + filename
    with open(filename, "w") as f:
        f.write("\n".join(currentArray))


def encrypt(currentArray: list, reverse) -> tuple[str, list[str]]:
    """
    INPUT:    The current grid, and if decrypt mode should be used
    FUNCTION: Encrypts the grid
    OUTPUT:   The encrypted grid, and the key
    """
    # Ask the user which cipher to use
    print("\n"*consoleY)
    print("Select the cipher to use. Type any combination of the following in order")
    print(f"{green }[P] Polybius Square")
    print(f"{green }[E] Extended Polybius")
    print(f"{green }[R] Rotation")
    print()
    print(f"{red   }[Q] Back")
    print("\033[0m")

    cipher = input("> ").lower()
    if "p" in cipher:
        out, currentArray = encryptPolybius(currentArray, reverse)
    elif "r" in cipher:
        out, currentArray =  encryptTransform(currentArray, reverse)
    elif "e" in cipher:
        out, currentArray = encryptExtendedPolybius(currentArray, reverse)
    else:
        out = None
    return out, currentArray


def getNewData() -> list[str]:
    """
    INPUT:    None
    FUNCTION: Gets the new data from the user
    OUTPUT:   The new data
    """
    print("\n"*consoleY)
    print("Enter the data you want to store, one line per row, or paste it in one line and press enter twice")
    print("Press enter to finish")
    print()
    newData = []
    out = False
    # Repeatedly get lines of data until the user enters an empty line
    while not out:
        newData.append(input("> "))
        if newData[-1] == "":
            newData.pop()
            out = True
    if len(newData) == 0:
        # If no data was entered, return None
        return None
    if len(newData) == 1:
        # If only one line was entered, find the factors of the length of the line
        # This can be used to ask the user which size they want the grid to be
        factors = []
        for i in range(1, len(newData[0]) + 1):
            if len(newData[0]) % i == 0:
                factors.append(f"{i} x {len(newData[0]) // i}")
        valid = False
        previousOutput = None
        while not valid:
            # While the users response is not valid
            print("\n"*consoleY)
            # Render the possible factors as a table
            printAsTable(factors, max([len(i) for i in factors]))
            if previousOutput is not None:
                # Show an error if needed
                print(previousOutput)
                previousOutput = None
            x = input("\nSelect the dimensions of the array you want to use (rows x columns), or type q to quit\n> ")
            if x.lower() == "q":
                # Quit if q is entered
                return None
            elif not x.isnumeric():
                # Error if it isn't a number
                previousOutput = f"{red}Invalid input\033[0m"
                continue
            x = int(x)
            # Get the dimensions by splitting the input by the x, e.g. 16 x 4 -> [16, 4]
            dimensions = factors[x].split(" x ")
            newData = [newData[0][i:i + int(dimensions[1])] for i in range(0, len(newData[0]), int(dimensions[1]))]
            valid = True
    return newData


def printAsTable(currentArray: list[str], arrayMaxWidth: int) -> None:
    """
    INPUT:    The array to print, and the maximum width of one line
    FUNCTION: Prints the array as a table
    OUTPUT:   None
    """
    # Get the amount of characters of the width of the largest number.
    maxNumberWidth = math.ceil(math.log10(len(currentArray))) + 1
    print(f"┌{'─' * (maxNumberWidth + 2)}┬{'─' * (arrayMaxWidth + 2)}┐")  # Header
    for i in range(len(currentArray)):
        lmc = "\033[0m"  # Last modified colour
        lm = green if lastAdded == i or lastAdded == "all" else ""  # Set to green if the line was added
        lm = yellow if lastEdited == i or lastEdited == "all" else ""  # Or yellow if it was edited
        print(f"│ {lm}{pad(str(i), maxNumberWidth)}{lmc} │ {pad(currentArray[i], arrayMaxWidth, f'{red}█')}\033[0m │")
    print(f"└{'─' * (maxNumberWidth + 2)}┴{'─' * (arrayMaxWidth + 2)}┘")


while not close:
    consoleX, consoleY = os.get_terminal_size()
    # Show newlines to hide the previous output
    print("\n"*consoleY)
    # Get the width of the largest line
    arrayMaxWidth = max([len(i) for i in currentArray]) if len(currentArray) > 0 else 0
    if arrayMaxWidth:
        # If there is data, print it as a table
        printAsTable(currentArray, arrayMaxWidth)
    else:
        # Otherwise, print an error
        print("No cipher entered")
    print(f"{green }[+ y]  Add a row at the end that says y")  # Add commands
    print(f"{green }[++ y] Add a row at the start that says y")
    print(f"{green }[+x y] Add a row before row x that says y")
    print(f"{red   }[-]    Remove the last row")  # Remove commands
    print(f"{red   }[--]   Remove the first row")
    print(f"{red   }[-x]   Remove row x")
    print(f"{yellow}[x y]  Modify row x to be y")  # Modify commands
    print(f"{yellow}[*]    Enter a new full set of data, replacing the current one")
    print()
    print(f"{blue  }[e]    Encrypt the current cipher")  # Encrypt / decrypt
    print(f"{blue  }[d]    Decrypt the current cipher")
    print(f"{green }[s x]  Save the current cipher to file x")  # Save / load
    print(f"{yellow}[l x]  Load a cipher from file x")
    print(f"{blue  }[u]    Undo")  # Undo
    print(f"{red   }[q]    Quit")  # Quit
    print("\033[0m")
    if showBefore:
        # If the user wants to see the previous output, show it
        print(f"Message after cipher: {showBefore}")
        showBefore = None

    lastAdded = None
    lastEdited = None

    command = input("> ").strip()  # Get the command
    substrings = command.split(" ")

    if substrings[0] != "u":  # If the command isn't undo, add it to the undo stack
        beforeChange.append(currentArray.copy())

    if substrings[0] == "+" and len(substrings) >= 2:  # Add a row at the end
        currentArray.append(" ".join(substrings[1:]))
        lastAdded = len(currentArray) - 1
    elif substrings[0] == "++" and len(substrings) >= 2:  # Add a row at the start
        currentArray.insert(0, " ".join(substrings[1:]))
        lastAdded = 0
    elif substrings[0].startswith("+") and substrings[0][1:].isnumeric() and len(substrings) >= 2:
        # Add a row before a specific row
        currentArray.insert(int(substrings[0][1:]), " ".join(substrings[1:]))
        lastAdded = int(substrings[0][1:])
    elif substrings[0] == "-":  # Remove the last row
        currentArray.pop()
        lastAdded = None
    elif substrings[0] == "--":  # Remove the first row
        currentArray.pop(0)
    elif substrings[0].startswith("-") and substrings[0][1:].isnumeric():  # Remove a specific row
        currentArray.pop(int(substrings[0][1:]))
    elif substrings[0].isnumeric() and len(substrings) >= 2:  # Modify a specific row
        currentArray[int(substrings[0])] = " ".join(substrings[1:])
        lastEdited = int(substrings[0])
    elif substrings[0] == "*":  # Enter a new full set of data
        tmp = getNewData()
        if tmp is not None:  # If the user didn't quit, set the new data
            currentArray = tmp
        lastEdited = "all"
    elif substrings[0] == "e":  # Encrypt the current cipher
        showBefore, currentArray = encrypt(currentArray, False)
    elif substrings[0] == "d":  # Decrypt the current cipher
        showBefore, currentArray = encrypt(currentArray, True)
    elif substrings[0] == "s":  # Save the current cipher to a file
        if not len(substrings) >= 2:
            substrings.append(input("Filename:\n> "))
        saveArray(" ".join(substrings[1:]), currentArray)
    elif substrings[0] == "l":  # Load a cipher from a file
        if not len(substrings) >= 2:
            substrings.append(input("Filename:\n> "))
        tmp = loadArray(" ".join(substrings[1:]))
        if tmp is not None:  # If the file existed, set the new data
            currentArray = tmp
    elif substrings[0] == "u":  # Undo
        if len(beforeChange) > 0:  # If there is something to undo
            currentArray = beforeChange.pop()
            lastEdited = "all"
        lastAdded = None
    elif substrings[0] == "q":  # Quit
        close = True
