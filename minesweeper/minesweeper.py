import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count != 0 and len(self.cells) == self.count:
            return self.cells
        # this is actually not needed outside of check50 requirements, which checks for an empty set if no elements are found
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if len(self.cells) != 0 and self.count == 0:
            return self.cells
        # this is actually not needed outside of check50 requirements, which checks for an empty set if no elements are found
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        # If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, 
        # but still represents a logically correct sentence given that cell is known to be a mine.
        # If cell is not in the sentence, then no action is necessary.
        
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)
        # If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence,
        # but still represents a logically correct sentence given that cell is known to be safe.
        # If cell is not in the sentence, then no action is necessary.


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # a "move" and a "count" are being passed to the the add_knowledge method. move is a touple of two values as coordinates for a cell on the board
        # while count it is an integer which indicates how many neighbouring mines there are for that cell.
        # mark the cell as a move that has been made
        self.moves_made.add(cell)
        # mark the cell as safe
        self.safes.add(cell)
        # add a new sentence to the AI's knowledge base
        # map out all the possible neighbouring cells for the cell being passed to add_knowledge
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update if cell in bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    cells.add((i, j))
        # instatiate a Sentence object which associates said cells with the count of mines. ex. of a sentence: {A, B, C} = 2
        sentence = Sentence(cells, count)
        # isdisjoint Returns True if the set has no elements in common with other. Sets are disjoint if and only if their intersection is the empty set.
        if not sentence.cells.isdisjoint(self.mines):
            # Return a new set with elements common to the set and all *others. then counts the element for that set, which are all the mines
            n_mines = len(sentence.cells.intersection(self.mines))
            # Update the set, removing elements found in *others.
            sentence.cells.difference_update(self.mines)
            # Update the count to reflect known mines found in the cells
            sentence.count -= n_mines

        # Update the set, removing elements found in *others.
        sentence.cells.difference_update(self.safes, self.moves_made)
        # adds the sentence to the 'knowledge' list of sentences 
        self.knowledge.append(sentence)
        # mark any additional cells as safe or as mines
        for info in self.knowledge:
            if cell in info.cells:
                info.cells.discard(cell)
        done = False
        while not done:
            done = True
            # loops through the items of knowledge, so sentence type objects, uses the instance methods known_mines 
            # which return self.cells if self.count != 0 and len(self.cells) == self.count. 
            # this means that if the count it's not 0 and it is equal as the number of cells in the sentence, therefore each cell is a mine ex. {A, B, C} = 3
            for info in self.knowledge:
                if info.known_mines():
                    done = False
                    # self.cells is returned, it loops through each individual cell of which the sentence it is composed
                    for cell in info.cells.copy():
                        # it marks each as a mine, using the minesweeperai instance method. which works as follows:
                            # self.mines.add(cell)                  it adds each cell to the mines instance variable
                            # for sentence in self.knowledge:       loops through the knowledge list again and 
                                # sentence.mark_mine(cell)          calls the sentence method mark_mine for each cell        
                                    # self.cells.remove(cell)
                                    # self.count -= 1
                        self.mark_mine(cell)
                # if the count is 0 it means each cell in the sentence is not a mine ex. {A, B, C} = 0
                if info.known_safes():
                    done = False
                    for cell in info.cells.copy():
                        self.mark_safe(cell)

        for sentence in self.knowledge:
            sentence.cells.difference_update(self.safes, self.mines)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # check for the existance of a subset of safes, subtracting from it elements of moves already made and mines. if so it returns a new set
        # then pick a random element from said set and returns it with .pop()
        if safe_move := self.safes.difference(self.moves_made, self.mines):
            return safe_move.pop()
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                all_moves.add((i, j))
        not_moves = self.moves_made | self.mines
        if possible_moves := all_moves - not_moves:
            return possible_moves.pop()

