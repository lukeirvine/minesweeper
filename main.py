DEBUG = False


def main():
    import functions

    print("\n")
    welcomeChoice = functions.welcome()

    # used for functions that need to return multiple variables
    boardProp = {"rows": 0,
                 "columns": 0,
                 "bombs": 0}


    # set size of board if new game
    if welcomeChoice == 1:
        functions.setSize(boardProp)
    # load existing game board if loading saved game
    else:
        # get row and column info from file
        # savegame is file info without row, column, and bomb info
        savegame = functions.get_array_info(boardProp)

        # if there is no file to load from, end program
        if savegame == 0:
            return 0

    # transfer dictionary values into variables
    rows = boardProp["rows"]
    columns = boardProp["columns"]
    bombs = boardProp["bombs"]

    # display board specs
    print("\nYour Game Board Has:")
    print("-", rows, "rows")
    print("-", columns, "columns")
    print("-", bombs, "bombs")

    # ask where game board should be displayed
    display = functions.display_choice()

    # ask if you would like it in color if displayed in terminal
    if display == 2:
        color = functions.ask_color()

    # initialize 2D lists
    answerArray = []
    gameArray = []

    # fill answerArray with data from file if choosing to load game
    if welcomeChoice == 2:
        fail = functions.load_game(answerArray, gameArray, rows, columns, savegame)
        if fail == 0:
            return 0
        # export answer game array
        functions.output_answerArray(answerArray, rows, columns)

    # fill gameArray if choosing to create new game
    if welcomeChoice == 1:
        functions.make_gameArray(gameArray, rows, columns)

    # export gameArray
    functions.output_gameArray(gameArray, rows, columns)

    # Explain where gameboard is and prompt input
    functions.instructions(display)

    # display gameArray if chosen
    if display == 2:
        functions.display_gameArray(gameArray, rows, columns, color)

    notDone = True  # used to continue through game play loop
    i = 1           # used as counter to only create answer board the first time

    # increment counter if game was loaded
    if welcomeChoice == 2:
        i += 1

    # initialize dictionary for user guess input
    guessInput = {"r": 0,          # used to store row number for guess
                  "c": 0,          # used to store column number for guess
                  "action": "E"}   # used to store action (flag or uncover)

    # main loop for gameplay
    while notDone:
        # display that 'u' must be chosen on first turn
        if i == 1 and welcomeChoice == 1:
            print("You must uncover a cell on your first turn.\n")

        # get coordinate input
        functions.getCoordinates(gameArray, guessInput, rows, columns, i, welcomeChoice)

        if DEBUG:
            print("left function")

        # extract values from dictionary
        r = guessInput["r"]
        c = guessInput["c"]
        action = guessInput["action"]

        if DEBUG:
            print("action out of function:", action)

        # save game if requested
        if action == "s":
            functions.save_game(answerArray, gameArray, rows, columns, bombs)
            if DEBUG:
                print("hit save game if statement")
            # output goodbye message
            print("\n")
            print("Have a nice day!")
            print("Your progress is saved in \"savegame.txt\".")
            return 0

        # quit without saving if requested
        if action == "q":
            print("\n")
            print("Have a nice day!")
            print("Progress was not saved.")
            return 0

        # fill answerArray only if first time through loop and user
        # chooses to create new game
        if i == 1 and welcomeChoice == 1:
            # fill answerArray based on coordinate input
            functions.make_answerArray(answerArray, rows, columns, r, c, bombs)

            # export answerARray to external file for reference
            functions.output_answerArray(answerArray, rows, columns)

        # update gameboard based off answer gameboard
        loss = functions.update_gameArray(answerArray, gameArray, rows, columns, r, c, action)

        # export gameArray after update
        functions.output_gameArray(gameArray, rows, columns)

        if display == 2:
            print("\n")
            functions.display_gameArray(gameArray, rows, columns, color)

        # if loss
        if loss:
            print("\n")
            print("BOOM!! You uncovered a bomb! You lose!")
            print("'X' marks where the bombs were.")
            print("Thanks for playing!")
            return 0

        # check for victory
        if functions.check_victory(answerArray, gameArray, rows, columns):
            print("\nCongratulations!! You win!!")
            return 0

        # increment counter
        i += 1

    return 0

    # ============================================================


main()
