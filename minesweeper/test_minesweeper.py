from minesweeper import MinesweeperAI, Minesweeper, Sentence

N_MOVES = 52

moves = {}

def print_board(moves):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(8):
            print("--" * 8 + "-")
            for j in range(8):
                if (i, j) in moves:
                    print(f"|{moves[(i, j)]}", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * 8 + "-")

def new_init(self, height=8, width=8, mines=8):
     # Set initial width, height, and number of mines
        self.plant_mines = {(0, 1), (0, 3), (0, 6), (1, 6), (3, 2), (6, 0), (6, 4), (7, 4)}
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
            i, j = self.plant_mines.pop()
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

# monkey patch for planting set mines 
Minesweeper.__init__ = new_init
     

ai = MinesweeperAI(8, 8)
game = Minesweeper()
for _ in range(N_MOVES):
    move = ai.make_safe_move()    
    if move is None:
        move = ai.make_random_move()
        if move is None:
            flags = ai.mines.copy()
            print("No moves left to make.")
        else:
            print("No known safe moves, AI making random move.")
    else:
        print("AI making safe move.") 
    if move:
            if game.is_mine(move):
                print("LOST GAME")
                break
            else:
                nearby = game.nearby_mines(move)
                ai.add_knowledge(move, nearby)
                moves[move] = nearby 
                print_board(moves)
                     