import os
from ciphers.transform import encrypt as encryptTransform
from ciphers.polybius import encrypt as encryptPolybius

close = False
currentArray = ["ABCDE", "FGHIJ", "KLMNO", "PQRST", "UVWXY"]
lastAdded = None
lastEdited = None
beforeChange = []

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"


def pad(string: str, length: int, char: str = " ") -> str:
    return string + (char * max(0, length - len(string)))


def encrypt(currentArray: list, reverse) -> tuple[str, list[str]]:
    print("\n"*consoleY)
    print("Select the cipher to use. Type any combination of the following in order")
    print(f"{green }[P] Polybius Square")
    print(f"{green }[R] Rotation")
    print()
    print(f"{red   }[Q] Back")
    print("\033[0m")

    cipher = input("> ").lower()
    if "p" in cipher:
        out, currentArray = encryptPolybius(currentArray, reverse)
    elif "r" in cipher:
        out, currentArray =  encryptTransform`(currentArray, reverse)
    else:
        out = None
    return out, currentArray


def getNewData() -> list[str]:
    print("\n"*consoleY)
    print("Enter the data you want to store, one line per row, or paste it in one line and press enter twice")
    print("Press enter to finish")
    print()
    newData = []
    out = False
    while not out:
        newData.append(input("> "))
        if newData[-1] == "":
            newData.pop()
            out = True
    if len(newData) == 0:
        newData = None
    elif len(newData) == 1:
        factors = []
        for i in range(1, len(newData[0]) + 1):
            if len(newData[0]) % i == 0:
                factors.append(f"{i} x {len(newData[0]) // i}")
        valid = False
        previousOutput = None
        while not valid:
            print("\n"*consoleY)
            printAsTable(factors, max([len(i) for i in factors]))
            if previousOutput is not None:
                print(previousOutput)
                previousOutput = None
            print("\nSelect the dimensions of the array you want to use (rows x columns), or type q to quit")
            x = input("> ")
            if x.lower() == "q":
                return None
            elif not x.isnumeric():
                previousOutput = f"{red}Invalid input\033[0m"
                continue
            x = int(x)
            dimensions = factors[x].split(" x ")
            newData = [newData[0][i:i + int(dimensions[1])] for i in range(0, len(newData[0]), int(dimensions[1]))]
            valid = True
    return newData


def printAsTable(currentArray: list[str], arrayMaxWidth: int) -> None:
    maxNumberWidth = len(currentArray) // 10 + 1
    print(f"┌{'─' * (maxNumberWidth + 2)}┬{'─' * (arrayMaxWidth + 2)}┐")
    for i in range(len(currentArray)):
        lmc = "\033[0m"
        lm = green if lastAdded == i or lastAdded == "all" else ""
        lm = yellow if lastEdited == i or lastEdited == "all" else ""
        print(f"│ {lm}{pad(str(i), maxNumberWidth)}{lmc} │ {pad(currentArray[i], arrayMaxWidth, f'{red}█')}\033[0m │")
    print(f"└{'─' * (maxNumberWidth + 2)}┴{'─' * (arrayMaxWidth + 2)}┘")


showBefore = None

while not close:
    consoleX, consoleY = os.get_terminal_size()
    print("\n"*consoleY)
    arrayMaxWidth = max([len(i) for i in currentArray]) if len(currentArray) > 0 else 0
    if arrayMaxWidth:
        printAsTable(currentArray, arrayMaxWidth)
    else:
        print("No cipher entered")
    print(f"{green }[+ y]  Add a row at the end that says y")
    print(f"{green }[++ y] Add a row at the start that says y")
    print(f"{green }[+x y] Add a row before row x that says y")
    print(f"{red   }[-]    Remove the last row")
    print(f"{red   }[--]   Remove the first row")
    print(f"{red   }[-x]   Remove row x")
    print(f"{yellow}[x y]  Modify row x to be y")
    print(f"{yellow}[*]    Enter a new full set of data, replacing the current one")
    print()
    print(f"{blue  }[e]    Encrypt the current cipher")
    print(f"{blue  }[d]    Decrypt the current cipher")
    print(f"{green }[s x]  Save the current cipher to file x")
    print(f"{yellow}[l x]  Load a cipher from file x")
    print(f"{blue  }[u]    Undo")
    print(f"{red   }[q]    Quit")
    print("\033[0m")
    if showBefore:
        print(f"Message after cipher: {showBefore}")
        showBefore = None

    lastAdded = None
    lastEdited = None

    command = input("> ").strip()
    substrings = command.split(" ")

    if substrings[0] != "u":
        beforeChange.append(currentArray.copy())

    if substrings[0] == "+" and len(substrings) >= 2:
        currentArray.append(" ".join(substrings[1:]))
        lastAdded = len(currentArray) - 1
    elif substrings[0] == "++" and len(substrings) >= 2:
        currentArray.insert(0, " ".join(substrings[1:]))
        lastAdded = 0
    elif substrings[0].startswith("+") and substrings[0][1:].isnumeric() and len(substrings) >= 2:
        currentArray.insert(int(substrings[0][1:]), " ".join(substrings[1:]))
        lastAdded = int(substrings[0][1:])
    elif substrings[0] == "-":
        currentArray.pop()
        lastAdded = None
    elif substrings[0] == "--":
        currentArray.pop(0)
    elif substrings[0].startswith("-") and substrings[0][1:].isnumeric():
        currentArray.pop(int(substrings[0][1:]))
    elif substrings[0].isnumeric() and len(substrings) >= 2:
        currentArray[int(substrings[0])] = " ".join(substrings[1:])
        lastEdited = int(substrings[0])
    elif substrings[0] == "*":
        tmp = getNewData()
        if tmp is not None:
            currentArray = tmp
        lastEdited = "all"
    elif substrings[0] == "e":
        showBefore, currentArray = encrypt(currentArray, False)
    elif substrings[0] == "d":
        showBefore, currentArray = encrypt(currentArray, True)
    elif substrings[0] == "s":
        if not len(substrings) >= 2:
            substrings.append(input("Filename:\n> "))
        filename = " ".join(substrings[1:])
        with open("savedCiphers/" + filename, "w") as f:
            f.write("\n".join(currentArray))
    elif substrings[0] == "l":
        if not len(substrings) >= 2:
            substrings.append(input("Filename:\n> "))
        filename = " ".join(substrings[1:])
        with open("savedCiphers/" + filename, "r") as f:
            currentArray = f.read().splitlines()
        lastEdited = "all"
    elif substrings[0] == "u":
        if len(beforeChange) > 0:
            currentArray = beforeChange.pop()
            lastEdited = "all"
        lastAdded = None
    elif substrings[0] == "q":
        close = True
