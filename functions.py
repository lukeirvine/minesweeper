DEBUG = False

# ============================================================
'''
 * Function: getInput
 * Preparamter: - minimum value for input, 
 *              - maximum value for input,
 *              - and string to display the prompt
 * Purpose: checks input for type and range errors
 * Postparamter: Returns a value from input once it
 *               has been checked.
 *
'''
def getInput(min, max, prompt):
    invalid = True

    while invalid:
        invalid = False
        try:
            userInput = input(prompt)
            userInput = int(userInput)
            if userInput < min or userInput > max:
                print("\nError: Please enter proper input.")
                invalid = True
        except(ValueError, TypeError):
            print("\nError: Please enter proper input.")
            invalid = True
        
    return userInput


# ============================================================
'''
 * Function: welcome
 * Preparamter: none
 * Purpose: Prints out a welcome screen that prompts user
 *          to either start a new game or load an old one.
 * Postparamter: Returns an int either 1 or 2 to specify
 *               which menu option has been chosen.
 *
'''
def welcome():
    print("        Welcome to Mine Sweeper!")
    print("===========================================")
    print("Would you like to")
    print("   1: Start a new game, or")
    print("   2: Load a saved game?")

    return getInput(1, 2, "Enter the number of your desired option: ")


# ============================================================
'''
 * Function: instructions
 * Preparamter: display choice
 * Purpose: Prints out a where the game board is and how to
 *          enter what you want to do for the rest of the
 *          game.
 * Postparamter: none
 *
'''
def instructions(display):
    if display == 1:
        print("\n")
        print("===============================================")
        print("Open \"game_board.txt\" to see your game board")
        print("in real time!")
        print("===============================================")

    if display == 2:
        print("\n")
        print("===============================================")
        print("Your game board above will be displayed after")
        print("each action below.")
        print("===============================================")

    print("Enter 'action' letter")
    print("   u: to uncover the cell,")
    print("   f: to flag the cell for a bomb,")
    print("   r: to remove a flag,")
    print("   s: to save your game and quit, or")
    print("   q: to quit without saving.")
    print("Then enter the row and column numbers of the")
    print("cell you'd like to uncover.")
    print("===============================================")


# ============================================================
'''
 * Function: setSize
 * Preparamter: number of columns, rows, and bombs in
 *              boardProp dictionary
 * Purpose: Prompts user to give dimensions of game board
 *          with some suggestions and calculates number of
 *          bombs used on board based on percentage of the
 *          the board's area.
 * Postparamter: Returns values to boardProp dictionary for
 *               rows, columns, and bombs
 *
'''
def setSize(boardProp):

    print("\n")
    print("        -----New Game selected-----")
    print("Choose your game board dimensions between")
    print("7 - 18 rows and columns.")

    # get input for rows and columns
    rows = getInput(7, 18, "Rows: ")
    columns = getInput(7, 18, "Columns: ")

    # calculate number of bombs
    percentage = 0
    area = rows * columns

    # set percentage based on area of board
    if area <= 100:
        percentage = 0.125
    if area > 100 and area <= 196:
        percentage = 0.14
    if area > 196:
        percentage = 0.16

    # calculate number of bombs (rounded to be whole number)
    bombs = int(area * percentage + 0.5)

    # return values to dictionary
    boardProp["rows"] = rows
    boardProp["columns"] = columns
    boardProp["bombs"] = bombs

# ============================================================
'''
 * Function: make_gameArray
 * Preparamter: empty array, and int parameters for the number
 *              of rows and columns
 * Purpose: fills the gameArray with '@' to signify a covered
 *          cell.
 * Postparamter: gameArray by reference
 *
'''
def make_gameArray(gameArray, rows, columns):
    for r in range(0, rows):
        row = []
        for c in range(0, columns):
            row.append("@")
        gameArray.append(row)

# ============================================================
'''
 * Function: output_gameArray
 * Preparamter: filled array, and int parameters for the number
 *              of rows and columns
 * Purpose: prints the array in a grid with grid lines and such
 * Postparamter: none
 *
'''
def output_gameArray(gameArray, rows, columns):
    # open file
    with open("game_board.txt", "w") as f:
        # loop through columns
        for r in range(1, rows * 2 + 3):
            # print column (c) numbers
            if r == 1:
                f.write("     ")
                for c in range(1, columns + 1):
                    if c < 10:
                        f.write(str(c))
                        f.write("   ")
                    if c >= 10:
                        f.write(str(c))
                        f.write("  ")
                f.write("\n")

            # print row lines between cells
            if r % 2 == 0:
                f.write("   ")
                for c in range(1, columns + 1):
                    f.write("----")
                f.write("-\n")

            # print row numbers and rows
            row = 0
            if r % 2 == 1 and r != 1:
                # convert loop iteration number into number of
                # actual row in gameArray
                row = int((r - 1) / 2)
                if row < 10:
                    f.write(str(row))
                    f.write("  |")
                if row >= 10:
                    f.write(str(row))
                    f.write(" |")
                for c in range(1, columns + 1):
                    f.write(" ")
                    f.write(str(gameArray[row - 1][c - 1]))
                    f.write(" |")
                f.write("\n")
        

# ============================================================
'''
 * Function: getCoordinates
 * Preparamter: - gameArray passed by reference
 *              - dictionary guessInput that has r for row guess,
 *                c for column guess, and action for desired
 *                action
 *              - integers of gameboard number of rows and 
 *                columns passed by value.
 *              - counter int i to determine when to check if
 *                cell has already been inputted
 * Purpose: prompt user to uncover, flag, or unflag a cell based on 
 *          coordinates or save or quit game
 * Postparamter: none
 *
'''
def getCoordinates(gameArray, guessInput, rows, columns, i, welcomeChoice):
    invalid = True
    while invalid:
        invalid = False

        # get Action indicator
        action = getAction("Enter action:")

        if DEBUG:
            print("action in function:", action)

        # break out of function if action is not 'u' on first turn
        if ((action == "s" or action == "f" or action == "r") and
            i == 1 and welcomeChoice == 1):
            print("\nError: You must uncover a cell on your first turn.")
            invalid = True
            continue

        # if user wishes to save game or quit, break out of loop and function
        if action == "s" or action == "q":
            guessInput["action"] = action
            break

        # get row number
        r = getInput(1, rows, "Enter row number:")

        # get column number
        c = getInput(1, columns, "Enter column number:")

        # convert guesses from row numbers into index numbers
        r -= 1
        c -= 1

        # if user tries to remove a flag where there isn't one
        if action == "r" and gameArray[r][c] != "X":
            print("\nError: There isn't a flag there to uncover.")
            invalid = True

        # check to see if square has already been uncovered or flagged
        if gameArray[r][c] != "@" and i != 1 and action == "u":
            if gameArray[r][c] == "X":
                print("\nError: You have a flag on this square.")
                print("       Remove the flag to uncover the cell.")
                invalid = True
            else:
                print("\nError: You already uncovered this square! Try again!")
                invalid = True

        # transfer variables into dictionary
        guessInput["r"] = r
        guessInput["c"] = c
        guessInput["action"] = action

        if DEBUG:
            print("end of loop")

# ============================================================
'''
 * Function: getAction
 * Preparamter: - and string to display the prompt
 * Purpose: checks input for type and range errors
 * Postparamter: Returns a value from input once it
 *               has been checked.
 *
'''
def getAction(prompt):
    invalid = True

    while invalid:
        invalid = False
        try:
            userInput = input(prompt)
            if not(userInput == "u" or userInput == "f" or
                   userInput == "s" or userInput == "q" or
                   userInput == "r"):
                print("\nError: Please enter proper input.")
                invalid = True
        except(ValueError):
            print("\nError: Please enter proper input.")
            invalid = True

    return userInput

# ============================================================
'''
 * Function: make_answerArray
 * Preparamter: - empty array with max number of columns 
 *              - number of rows, columns, row guess number, column
 *                guess number, and number of bombs.
 * Purpose: Fills in array with bombs and numbers on cells
 *          around the bombs based on the first guess
 * Postparamter: answerArray by reference
 *
'''
def make_answerArray(answerArray, rows, columns, guessR, guessC, bombs):
    import random

    # used to hold random row and column value
    row = 0
    column = 0

    # fill answerArray with appropriate number of zeros
    for r in range(0, rows):
        row = []
        for c in range(0, columns):
            row.append(0)
        answerArray.append(row)

    # set bombs in array
    for i in range(0, bombs):
        row = random.randint(0, rows - 1)
        column = random.randint(0, columns - 1)

        # massive if statement to ensure first cell clicked is '0'
        if (answerArray[row][column] != "X" and
            # cell in center
           not(row == guessR and column == guessC) and
            # upper left
           not(row == guessR - 1 and column == guessC - 1) and
            # upper mid
           not(row == guessR - 1 and column == guessC) and
            # upper right
           not(row == guessR - 1 and column == guessC + 1) and
            # mid left
           not(row == guessR and column == guessC - 1) and
            # mid right
           not(row == guessR and column == guessC + 1) and
            # bottom left
           not(row == guessR + 1 and column == guessC - 1) and
            # bottom mid
           not(row == guessR + 1 and column == guessC) and
            # bottom right
           not(row == guessR + 1 and column == guessC + 1)):

           answerArray[row][column] = "X"

        else:
            # used to go back an iteration and try again
            i -= 1
            continue

    # fill in array with numbers
    for r in range(0, rows):
        for c in range(0, columns):

            # top left corner
            if r == 0 and c == 0:
                if answerArray[r][c] == "X":
                    if answerArray[r + 1][c] != "X":
                        answerArray[r + 1][c] += 1
                    if answerArray[r + 1][c + 1] != "X":
                        answerArray[r + 1][c + 1] += 1
                    if answerArray[r][c + 1] != "X":
                        answerArray[r][c + 1] += 1

            # top row
            if r == 0 and c > 0 and c < columns - 1:
                if answerArray[r][c] == "X":
                    if answerArray[r][c - 1] != "X":
                        answerArray[r][c - 1] += 1
                    if answerArray[r][c + 1] != "X":
                        answerArray [r][c + 1] += 1
                    if answerArray[r + 1][c - 1] != "X":
                        answerArray[r + 1][c - 1] += 1
                    if answerArray[r + 1][c] != "X":
                        answerArray[r + 1][c] += 1
                    if answerArray[r + 1][c + 1] != "X":
                        answerArray[r + 1][c + 1] += 1

            # top right corner
            if r == 0 and c == columns - 1:
                if answerArray[r][c] == "X":
                    if answerArray[r + 1][c] != "X":
                        answerArray[r + 1][c] += 1
                    if answerArray[r + 1][c - 1] != "X":
                        answerArray[r + 1][c - 1] += 1
                    if answerArray[r][c - 1] != "X":
                        answerArray[r][c - 1] += 1

            # left-most column
            if r > 0 and r < rows - 1 and c == 0:
                if answerArray[r][c] == "X":
                    if answerArray[r - 1][c] != "X":
                        answerArray[r - 1][c] += 1
                    if answerArray[r + 1][c] != "X":
                        answerArray[r + 1][c] += 1
                    if answerArray[r - 1][c + 1] != "X":
                        answerArray[r - 1][c + 1] += 1
                    if answerArray[r][c + 1] != "X":
                        answerArray[r][c + 1] += 1
                    if answerArray[r + 1][c + 1] != "X":
                        answerArray[r + 1][c + 1] += 1

            # Whole middle section
            if r > 0 and r < rows - 1 and c > 0 and c < columns - 1:
                if answerArray[r][c] == "X":
                    if answerArray[r - 1][c - 1] != "X":
                        answerArray[r - 1][c - 1] += 1
                    if answerArray[r - 1][c] != "X":
                        answerArray[r - 1][c] += 1
                    if answerArray[r - 1][c + 1] != "X":
                        answerArray[r - 1][c + 1] += 1
                    if answerArray[r][c + 1] != "X":
                        answerArray[r][c + 1] += 1
                    if answerArray[r + 1][c + 1] != "X":
                        answerArray[r + 1][c + 1] += 1
                    if answerArray[r + 1][c] != "X":
                        answerArray[r + 1][c] += 1
                    if answerArray[r + 1][c - 1] != "X":
                        answerArray[r + 1][c - 1] += 1
                    if answerArray[r][c - 1] != "X":
                        answerArray[r][c - 1] += 1

            # Right-most column
            if r > 0 and r < rows - 1 and c == columns - 1:
                if answerArray[r][c] == "X":
                    if answerArray[r - 1][c] != "X":
                        answerArray[r - 1][c] += 1
                    if answerArray[r - 1][c - 1] != "X":
                        answerArray[r - 1][c - 1] += 1
                    if answerArray[r][c - 1] != "X":
                        answerArray[r][c - 1] += 1
                    if answerArray[r + 1][c - 1] != "X":
                        answerArray[r + 1][c - 1] += 1
                    if answerArray[r + 1][c] != "X":
                        answerArray[r + 1][c] += 1

            # Bottom, left corner
            if r == rows - 1 and c == 0:
                if answerArray[r][c] == "X":
                    if answerArray[r - 1][c] != "X":
                        answerArray[r - 1][c] += 1
                    if answerArray[r - 1][c + 1] != "X":
                        answerArray[r - 1][c + 1] += 1
                    if answerArray[r][c + 1] != "X":
                        answerArray[r][c + 1] += 1

            # Bottom row
            if r == rows - 1 and c > 0 and c < columns - 1:
                if answerArray[r][c] == "X":
                    if answerArray[r][c - 1] != "X":
                        answerArray[r][c - 1] += 1
                    if answerArray[r - 1][c - 1] != "X":
                        answerArray[r - 1][c - 1] += 1
                    if answerArray[r - 1][c] != "X":
                        answerArray[r - 1][c] += 1
                    if answerArray[r - 1][c + 1] != "X":
                        answerArray[r - 1][c + 1] += 1
                    if answerArray[r][c + 1] != "X":
                        answerArray[r][c + 1] += 1

            # Bottom, right corner
            if r == rows - 1 and c == columns - 1:
                if answerArray[r][c] == "X":
                    if answerArray[r][c - 1] != "X":
                        answerArray[r][c - 1] += 1
                    if answerArray[r - 1][c - 1] != "X":
                        answerArray[r - 1][c - 1] += 1
                    if answerArray[r - 1][c] != "X":
                        answerArray[r - 1][c] += 1

    # replace zeros with spaces
    for r in range(0, rows):
        for c in range(0, columns):
            if answerArray[r][c] == 0:
                answerArray[r][c] = " "


# ============================================================
'''
 * Function: output_answerArray
 * Preparamter: filled answerArray with bombs and numbers,
 *              and number of rows and columns
 * Purpose: exports the answerArray game board to an external
 *          file.
 * Postparamter: none
 *
'''
def output_answerArray(answerArray, rows, columns):
    # open file
    with open("answer_game_board.txt", "w") as f:
        # loop through columns
        for r in range(1, rows * 2 + 3):
            # print column (c) numbers
            if r == 1:
                f.write("     ")
                for c in range(1, columns + 1):
                    if c < 10:
                        f.write(str(c))
                        f.write("   ")
                    if c >= 10:
                        f.write(str(c))
                        f.write("  ")
                f.write("\n")

            # print row lines between cells
            if r % 2 == 0:
                f.write("   ")
                for c in range(1, columns + 1):
                    f.write("----")
                f.write("-\n")

            # print row numbers and rows
            row = 0
            if r % 2 == 1 and r != 1:
                # convert loop iteration number into number of
                # actual row in gameArray
                row = int((r - 1) / 2)
                if row < 10:
                    f.write(str(row))
                    f.write("  |")
                if row >= 10:
                    f.write(str(row))
                    f.write(" |")
                for c in range(1, columns + 1):
                    f.write(" ")
                    f.write(str(answerArray[row - 1][c - 1]))
                    f.write(" |")
                f.write("\n")


# ============================================================
'''
 * Function: update_gameArray
 * Preparamter: - answerArray current state by reference.
 *              - gameArray current state by reference.
 *              - int number of rows and columns for both 
 *                arrays.
 *              - int row number and column number guessed
 *                by user.
 *              - action chosen by user
 * Purpose: uncover cell if requested and trigger function to 
 *          check adjacent cells
 *          Also, flag or unflag cell if requested
 * Postparamter: boolean value to indicate if the game has been lost
 *               gameArray by reference
 *
'''
def update_gameArray(answerArray, gameArray, rows, columns, r, c, action):
    # if user wishes to uncover a cell
    if action == "u":
        if answerArray[r][c] != " ":
            gameArray[r][c] = answerArray[r][c]
            if answerArray[r][c] == "X":
                # fills game board with "X"s to show where the bombs were
                for i in range(0, rows):
                    for j in range(0, columns):
                        if gameArray[i][j] == "@" and answerArray[i][j] == "X":
                            gameArray[i][j] = "X"
                        # removes false flags after loss
                        if gameArray[i][j] == "X" and answerArray[i][j] != "X":
                            gameArray[i][j] = "@"
                return True

        if answerArray[r][c] == " ":
            gameArray[r][c] = answerArray[r][c]
            answerArray[r][c] = 0
            check_adjacent_cells(answerArray, gameArray, rows, columns, r, c)

    # if user wishes to flag a cell
    if action == "f":
        gameArray[r][c] = "X"

    # if user wishes to remove a flag
    if action == "r":
        gameArray[r][c] = "@"

    return False

# ============================================================
'''
 * Function: check_adjacent_cells
 * Preparamter: - answerArray current state by reference.
 *              - gameArray current state by reference.
 *              - int number of rows and columns for both 
 *                arrays.
 *              - int row number and column number guessed
 *                by user.
 * Purpose: check adjacent cells if a cell is zero and then
 *          check adjacent cells of adjacent cell if it is zero
 * Postparamter: none directly, but the function it calls
 *               returns arrays by reference
 *
'''
def check_adjacent_cells(answerArray, gameArray, rows, columns, r, c):

    # check middle section not on any edge
    if r > 0 and r < rows - 1 and c > 0 and c < columns - 1:
        for i in range(-1, 1 + 1):
            for j in range(-1, 1 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)

    # check top left corner
    if r == 0 and c == 0:
        for i in range(0, 1 + 1):
            for j in range(0, 1 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)

    # top row
    if r == 0 and c > 0 and c < columns - 1:
        for i in range(0, 1 + 1):
            for j in range(-1, 1 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)

    # top right corner
    if r == 0 and c == columns - 1:
        for i in range(0, 1 + 1):
            for j in range(-1, 0 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)

    # left-most column
    if r > 0 and r < rows - 1 and c == 0:
        for i in range(-1, 1 + 1):
            for j in range(0, 1 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)

    # right-most column
    if r > 0 and r < rows - 1 and c == columns - 1:
        for i in range(-1, 1 + 1):
            for j in range(-1, 0 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)

    # Bottom, left corner
    if r == rows - 1 and c == 0:
        for i in range(-1, 0 + 1):
            for j in range(0, 1 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)

    # Bottom row
    if r == rows - 1 and c > 0 and c < columns - 1:
        for i in range(-1, 0 + 1):
            for j in range(-1, 1 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)

    # Bottom, right corner
    if r == rows - 1 and c == columns - 1:
        for i in range(-1, 0 + 1):
            for j in range(-1, 0 + 1):
                check(answerArray, gameArray, rows, columns, r, c, i, j)


# ============================================================
'''
 * Function: check
 * Preparamter: - answerArray current state by reference.
 *              - gameArray current state by reference.
 *              - int number of rows and columns for both 
 *                arrays.
 *              - int row number and column number guessed
 *                by user.
 *              - int i and j to indicate address of cell being checked
 * Purpose: Check single adjacent cell with address passed by value
 *          given ints i and j.
 *          updates gameArray with info in answerArray if it is
 *          not a bomb. Updates answerArray cell with 0 if 
 *          its info has been used
 * Postparamter: gameArray and answerArray by reference
 *
'''
def check(answerArray, gameArray, rows, columns, r, c, i, j):
    # if cell is " " or a number > 0
    if answerArray[r + i][c + j] != "X" and answerArray[r + i][c + j] != 0:
        gameArray[r + i][c + j] = answerArray[r + i][c + j]

        # move on to next step if cell is " "
        if answerArray[r + i][c + j] == " ":
            # set " " cell to 0 so it is not checked again
            answerArray[r + i][c + j] = 0
            # re-call function to check this new cell
            check_adjacent_cells(answerArray, gameArray, rows, columns, r + i, c + j)

# ============================================================
'''
 * Function: check_victory
 * Preparamter: - answerArray passed by reference
 *              - gameArray passed by reference
 *              - two int parameters with number of rows
 *                and columns.
 * Purpose: checks each cell in answerArray with the corresponding
 *          cell in gameArray to see if all cells without bombs
 *          have been uncovered.
 *          Also checks to see if all bombs have been flagged
 * Postparamter: returns true if all cells without bombs are
 *               uncovered and bombs are flagged.
 *               returns false otherwise
 *
'''
def check_victory(answerArray, gameArray, rows, columns):

    # loop through each cell to see if all bombs are marked
    # in gameArray
    for r in range(0, rows):
        for c in range(0, columns):
            if answerArray[r][c] == "X":
                if answerArray[r][c] != gameArray[r][c]:
                    return False

    # loop through each cell to see if all cells are
    # uncovered
    for r in range(0, rows):
        for c in range(0, columns):
            if gameArray[r][c] == "@":
                return False

    return True
# ============================================================
'''
 * Function: save_game
 * Preparamter: - answerArray passed by reference
 *              - gameArray passed by reference
 *              - three int parameters with number of rows
 *                and columns and bombs.
 * Purpose: saves both arrays to file "savegame.txt" to be
 *          loaded later when user wants to continue game
 *          also saves row, column, and bomb info to
 *          "savegame.txt"
 * Postparamter: none
 *
'''
def save_game(answerArray, gameArray, rows, columns, bombs):
    # open file
    with open("savegame.txt", "w") as f:
        # output number of rows and columns and bombs
        f.write(str(rows))
        f.write("a")
        f.write(str(columns))
        f.write("b")
        f.write(str(bombs))
        f.write("c")
        f.write("\n")

        # output answerArray
        for r in range(0, rows):
            for c in range(0, columns):
                # if current location is " ", change to 0
                if answerArray[r][c] == " ":
                    answerArray[r][c] = 0

                # output current location
                f.write(str(answerArray[r][c]))
            f.write("\n")

        # output gameArray
        for r in range(0, rows):
            for c in range(0, columns):
                # if current location is " ", change to 0
                if gameArray[r][c] == " ":
                    gameArray[r][c] = 0

                # output current location
                f.write(str(gameArray[r][c]))
            f.write("\n")

# ============================================================
'''
 * Function: get_array_info
 * Preparamter: - number of rows, columns, and bombs passed
 *                by reference in boardProp dictionary.
 * Purpose: imports "savegame.txt" into string savegame
 *          and gets row and column info from first line and
 *          enters them into dictionary.
 * Postparamter: returns savegame, which is the rest of the
 *               file without row, column, and bomb info
 *
'''
def get_array_info(boardProp):
    savegame = 0

    try:
        with open("savegame.txt", "r") as f:
            savegame = f.read()

    except(FileNotFoundError):
        print("\n")
        print("Error: There is no game to load.")
        print("You must create and save a game first.")
        return 0

    # find indices of letters between rows, columns, and bombs
    a = savegame.index("a")
    b = savegame.index("b")
    c = savegame.index("c")

    # extract row, column, and bomb info
    rows = int(savegame[0:a])
    columns = int(savegame[a + 1:b])
    bombs = int(savegame[b + 1:c])

    # take off top row of savegame
    savegame = savegame.split("c")[1]
    savegame = savegame[1:len(savegame) - 1]

    # return values to dictionary
    boardProp["rows"] = rows
    boardProp["columns"] = columns
    boardProp["bombs"] = bombs

    return savegame


# ============================================================
'''
 * Function: load_game
 * Preparamter: - answerArray passed by reference
 *              - gameArray passed by reference
 *              - number of rows and columns passed by
 *                variable.
 *              - string savegame which will be extracted
 * Purpose: splices string savegame into two answerArray and
 *          gameArray 2D lists
 * Postparamter: returns 0 if file couldn't be opened, returns
 *               1 otherwise.
 *
'''
def load_game(answerArray, gameArray, rows, columns, savegame):
    # take all the "\n"s out of savegame
    savegame = "".join(savegame.split("\n"))

    try:
        # enter info into answerArray
        for r in range(0, rows):
            row = []
            for c in range(0, columns):
                row.append(savegame[c + r * columns])
            answerArray.append(row)

        # enter info into gameArray
        for r in range(0, rows):
            row = []
            for c in range(0, columns):
                row.append(savegame[rows * columns + c + r * columns])
            gameArray.append(row)

    except(IndexError):
        print("\n")
        print("Error loading file. Please make sure a game is saved first.")
        return 0

    # change all zeros to " " in each array and string numbers to int numbers
    for r in range(0, rows):
        for c in range(0, columns):
            if gameArray[r][c] == "0":
                gameArray[r][c] = " "
            if gameArray[r][c] > "0" and gameArray [r][c] < "9":
                gameArray[r][c] = int(gameArray[r][c])

    for r in range(0, rows):
        for c in range(0, columns):
            if answerArray[r][c] == "0":
                answerArray[r][c] = " "
            if answerArray[r][c] > "0" and answerArray [r][c] < "9":
                answerArray[r][c] = int(answerArray[r][c])

    return 1

# ============================================================
'''
 * Function: display_choice
 * Preparamter: none
 * Purpose: displays options for how to display the game
 *          board and gets appropriate input
 * Postparamter: returns user's choice of 1 or 2
 *
'''
def display_choice():
    print("\nHow would you like the game board displayed?")
    print("1. in a separate file")
    print("2. right here in this terminal")
    print("===============================================")
    return getInput(1, 2, "Your Choice:")


# ============================================================
'''
 * Function: display_gameArray
 * Preparamter: - gameArray passed by reference
 *              - number of rows and columns passed by
 *                variable.
 *              - color variable that is a boolean
 *                true means on, false means off
 * Purpose: creates new list of gameArray info with board
 *          lines, row numbers, and column numbers and prints
 *          this new list
 * Postparamter: none
 *
'''
def display_gameArray(gameArray, rows, columns, color):

    display = []

    # loop through columns
    for r in range(1, rows * 2 + 3):
        line = ""
        # print column (c) numbers
        if r == 1:
            line += "     "
            for c in range(1, columns + 1):
                if c < 10:
                    line += str(c)
                    line += "   "
                if c >= 10:
                    line += str(c)
                    line += "  "
            display.append(line)

        # print row lines between cells
        if r % 2 == 0:
            line += "   "
            for c in range(1, columns + 1):
                line += "----"
                if c == columns:
                    line += "-"
            display.append(line)

        # print row numbers and rows
        row = 0
        if r % 2 == 1 and r != 1:
            # convert loop iteration number into number of
            # actual row in gameArray
            row = int((r - 1) / 2)
            if row < 10:
                line += str(row)
                line += "  |"
            if row >= 10:
                line += str(row)
                line += " |"
            for c in range(1, columns + 1):
                line += " "
                if color and (gameArray[row - 1][c - 1] == "X" or
                             (str(gameArray[row - 1][c - 1]) > "0" and
                              str(gameArray[row - 1][c - 1]) < "9")):
                    # "X" in red
                    if gameArray[row - 1][c - 1] == "X":
                        line += str('\033[31m' + str(gameArray[row - 1][c - 1]) + '\033[0m')
                    # numbers in blue
                    if (str(gameArray[row - 1][c - 1]) > "0" and
                        str(gameArray[row - 1][c - 1]) < "9"):
                        line += str('\033[34m' + str(gameArray[row - 1][c - 1]) + '\033[0m')
                else:
                    line += str('\033[38m' + str(gameArray[row - 1][c - 1]) + '\033[0m')
                line += " |"
            display.append(line)

    # print display list
    for r in range(0, rows * 2 + 2):
        print(display[r])
    if DEBUG:
        print("Color is on:", color)


# ============================================================
'''
 * Function: ask_color
 * Preparamter: none
 * Purpose: asks user if they would like game board in color
 *          or black and white, and then changes global
 *          variable accordingly
 * Postparamter: color boolean value
 *
'''
def ask_color():
    # print prompt
    print("\nWould you like your game board to be in:")
    print("1. Black and White")
    print("2. Color")
    print("===============================================")
    choice = getInput(1, 2, "Your Choice:")

    # change global variable
    if choice == 1:
        color = False
    if choice == 2:
        color = True

    return color

# ============================================================
# TESTS # TESTS # TESTS # TESTS # TESTS # TESTS # TESTS
# ============================================================


def test_save_game():
    answerArray = []

    gameArray = []

    rows = 7
    columns = 7
    guessR = 5
    guessC = 5
    bombs = 6

    make_answerArray(answerArray, rows, columns, guessR, guessC, bombs)
    make_gameArray(gameArray, rows, columns)

    for i in range(0, rows):
        print("answerArray:", answerArray[i])
    for i in range(0, rows):
        print("gameArray:", gameArray[i])

    save_game(answerArray, gameArray, rows, columns, bombs)

# ============================================================

def test_get_array_info():
    boardProp = {"rows": 0,
                 "columns": 0,
                 "bombs": 0}

    savegame = get_array_info(boardProp)
    print("savegame after get array info:")
    print(savegame)

    rows = boardProp["rows"]
    columns = boardProp["columns"]
    bombs = boardProp["bombs"]

    print("rows:", rows * 2)
    print("columns:", columns * 2)
    print("bombs", bombs * 2)

    answerArray = []
    gameArray = []

    load_game(answerArray, gameArray, rows, columns, savegame)

    output_answerArray(answerArray, rows, columns)
    output_gameArray(gameArray, rows, columns)


# ============================================================

# run test functions
if DEBUG:
    test_save_game()
    test_get_array_info()



