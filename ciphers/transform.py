from ciphers.transformations import flipGridHorizontally, flipGridVertically
from ciphers.transformations import rotateGridClockwise, rotateGridAntiClockwise, gridToString

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"


def encrypt(currentArray: list[str], reverse: bool) -> tuple[str, list[str]]:
    print("Select the cipher to use. Type any combination of the following in order")
    print(f"{green }[H] Flip horizontally")
    print(f"{green }[V] Flip vertically")
    print(f"{green }[D] Flip diagonally")
    print(f"{yellow}[R] Rotate 90 degrees clockwise")
    print(f"{yellow}[L] Rotate 90 degrees counter-clockwise")
    print(f"{yellow}[U] Rotate 180 degrees")
    print()
    print(f"{red   }[Q] Back")
    print("\033[0m")
    cipherType = input("> ").strip().lower()
    if cipherType == "q":
        return None, currentArray
    cipherType = cipherType.lower().replace("d", "hv").replace("u", "rr")
    if reverse:
        cipherType = cipherType[::-1]
        cipherType = cipherType.replace("h", "t").replace("v", "h").replace("t", "v")
        cipherType = cipherType.replace("r", "t").replace("l", "r").replace("t", "l")
    ciphered = currentArray.copy()
    for i in cipherType:
        if i == "h":
            ciphered = flipGridHorizontally(ciphered)
        elif i == "v":
            ciphered = flipGridVertically(ciphered)
        elif i == "r":
            ciphered = rotateGridClockwise(ciphered)
        elif i == "l":
            ciphered = rotateGridAntiClockwise(ciphered)
    out = gridToString(ciphered)
    return out, ["".join(i) for i in ciphered]
