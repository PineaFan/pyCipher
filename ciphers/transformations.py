import matplotlib.pyplot as plt
import wordninja


# Config used when running this file directly
config = {
    "puzzleNumber": 4,
    "showPlot": True,
    "hideExcludedLetters": False
}


# Grids defined by a puzzle given in lesson
grid = [
    "UZSVCSHEE", "LCMKOPONA", "YRMKIYNOE", "DUWEVJUCE", "INBRFDDGE",
    "ADOMCCSTT", "QOARAPPLA", "LMEEUDMPE", "YQAOSREAR"
]
grid2 = [
    "XPHUEIMZT", "UWVHUETLS", "HMEWTPGQP", "OWRALOAST", "IGNOAAEJT",
    "SUDSEBXLA", "TFKSVTTRE", "CARYZHGEG", "XREELYIWA"
]
grid3 = [
    "HEREA", "REFIV", "ETHIN", "GSXYZ"
]

decryption = [
    "100001010", "001000000", "100000101", "001010000", "100000101",
    "001010000", "000000001", "010100000", "000001010"
]

newDecryption = []
newGrid = []


def rotateGridClockwise(array):
    """
    INPUT:    A 2D array
    FUNCTION: Rotates the array 90 degrees clockwise
    OUTPUT:   A 2D array
    """
    out = []
    for i in range(len(array[0])):
        out.append([])
        for j in range(len(array)):
            out[i].append(array[j][i])
    return flipGridHorizontally(out)


def rotateGridAntiClockwise(array):
    """
    INPUT:    A 2D array
    FUNCTION: Rotates the array 90 degrees anti-clockwise
    OUTPUT:   A 2D array
    """
    out = []
    for i in range(len(array[0])):
        out.append([])
        for j in range(len(array)):
            out[i].append(array[j][i])
    return flipGridVertically(out)


def flipGridHorizontally(array):
    """
    INPUT:    A 2D array
    FUNCTION: Flips the array horizontally
    OUTPUT:   A 2D array
    """
    out = []
    for i in range(len(array)):
        out.append(array[i][::-1])
    return out


def flipGridVertically(array):
    """
    INPUT:    A 2D array
    FUNCTION: Flips the array vertically
    OUTPUT:   A 2D array
    """
    out = []
    for i in range(len(array)):
        out.append(array[len(array) - i - 1])
    return out


if __name__ == "__main__":
    # If using this file directly, this defines the grid and decryption mask to use for the specified puzzle
    if config["puzzleNumber"] == 0:
        newDecryption = decryption
        newGrid = grid
    elif config["puzzleNumber"] == 1:
        newDecryption = rotateGridClockwise(decryption)
        newGrid = grid
    elif config["puzzleNumber"] == 2:
        newDecryption = flipGridHorizontally(decryption)
        newGrid = grid2
    elif config["puzzleNumber"] == 3:
        newDecryption = rotateGridClockwise(flipGridHorizontally(decryption))
        newGrid = grid2
    elif config["puzzleNumber"] == 4:
        newGrid = flipGridHorizontally(rotateGridClockwise(grid3))
        out = " ".join(["".join(newGrid[i]) for i in range(len(newGrid))])
        print(out)
        exit()


def stringFromGrid(grid, decryption, humanise=False) -> str:
    """
    INPUT:    A 2D array, a 2D array of 1s and 0s, and if the string should be converted to words
    FUNCTION: Decodes the grid using the decryption mask
    EXAMPLE:
        ABC | 100 |
        DEF | 010 |
        GHI | 100 | -> "ADG"
    OUTPUT:   A string
    """
    out = ""
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if decryption[i][j] == "1":
                out += grid[i][j]
    if humanise:
        return " ".join(wordninja.split(stringFromGrid(newGrid, newDecryption)))
    return out


def gridToString(grid) -> str:
    """
    INPUT:    A 2D array
    FUNCTION: Converts the grid to a string
    OUTPUT:   A string
    """
    return " ".join(["".join(grid[i]) for i in range(len(grid))])


if __name__ == "__main__":
    if config["showPlot"]:
        # Using matplotlib, show the grid and decryption mask as a plot
        plt.imshow([[~int(j) for j in list(n)] for n in newDecryption], cmap="binary")
        for i in range(len(newGrid)):
            for j in range(len(newGrid[i])):
                col = "k"
                if not config["hideExcludedLetters"]:
                    col = "w" if newDecryption[i][j] == "0" else "k"
                plt.text(j, i, newGrid[i][j], ha="center", va="center", color=col)
        # At the bottom, show the decrypted string
        plt.text(4.5, 9.5, stringFromGrid(newGrid, newDecryption, humanise=True), ha="center", va="center", color="k")
        plt.show()
        exit()

    print(stringFromGrid(newGrid, newDecryption, True))