init python:
    import random
    from collections import deque

    class Tile:
        def __init__(self):
            self.mine = False
            self.value = 0
            self.opened = False

    class BoardMinesweeper:
        def __init__(self, size, amount_mines):
            self.size = size
            self.amount_mines = amount_mines
            self.matrix_mines = [[Tile() for i in range(self.size)] for j in range(self.size)]
            self.playing_field = [[9 for i in range(self.size)] for j in range(self.size)] 
            self.adjacency_list = {}
            self.blown_up = False
            self.empty_tiles_remain = self.size * self.size - self.amount_mines


        def __fillAdjacencyList(self, r, c):
            for k in range(-1, 2):
                for l in range(-1, 2):
                    x = k + r
                    y = l + c
                    first_coord = "{} {}".format(r, c)
                    second_coord = "{} {}".format(x, y)
                    if (x < 0) or (x >= self.size) or (y < 0) or (y >= self.size):
                        continue
                    elif self.matrix_mines[x][y].value == 0:
                        if first_coord not in self.adjacency_list:
                            self.adjacency_list[first_coord] = set()
                        elif second_coord not in self.adjacency_list:
                            self.adjacency_list[second_coord] = set()
                        else:
                            if first_coord == second_coord:
                                continue
                            self.adjacency_list[first_coord].add(second_coord)
                            self.adjacency_list[second_coord].add(first_coord)


        def __putValues(self, r, c):
            n = 0 
            for k in range(-1, 2):
                for l in range(-1, 2):
                    x = k + r
                    y = l + c
                    if (x < 0) or (x >= self.size) or (y < 0) or (y >= self.size):
                        continue
                    elif self.matrix_mines[x][y].value < 0:
                        n += 1
            return n


        def fillField(self):
            amount = self.amount_mines
            while amount > 0:
                x = random.Random().randrange(self.size)
                y = random.Random().randrange(self.size)
                if self.matrix_mines[x][y].mine:
                    continue
                self.matrix_mines[x][y].value = -1
                self.matrix_mines[x][y].mine = True
                amount -= 1

            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix_mines[i][j].value == 0:
                        self.matrix_mines[i][j].value = self.__putValues(i, j)

            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix_mines[i][j].value == 0:
                        self.__fillAdjacencyList(i, j)
            

init python:
    def game():
        global board  
        global DIGITS  
        DIGITS = ("zero_minesweeper", "one_minesweeper", "two_minesweeper", "three_minesweeper", "four_minesweeper", "five_minesweeper", "sex_minesweeper", "seven_minesweeper", "eight_minesweeper")

        board = BoardMinesweeper(SIZE, AMOUNT_MINES)
        board.fillField()

        renpy.scene()
        renpy.show("bg bgshka")
        renpy.show_screen("grid_minesweeper")
        while board.empty_tiles_remain:
            result, i, j = [int(z) for z in ui.interact().split()]
            if result > 0 and result <= 8:
                board.playing_field[i][j] = result
                board.matrix_mines[i][j].opened = True
                board.empty_tiles_remain -= 1
            # Поиск в ширину, если что
            elif result == 0:
                start = "{} {}".format(i, j)
                queue = deque()
                queue += board.adjacency_list[start]
                checked = {start}
                while queue:
                    left = queue.popleft()
                    checked.add(left)
                    for neighbor in board.adjacency_list[left]:
                        if neighbor not in checked:
                            checked.add(neighbor)
                            queue += board.adjacency_list[neighbor]
                
                checked_around_tiles = set()
                for tile in checked:
                    r, c = [int(z) for z in tile.split()]
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            x = k + r
                            y = l + c
                            if (x < 0) or (x >= board.size) or (y < 0) or (y >= board.size):
                                continue
                            else:
                                if ("{} {}".format(x, y) not in checked_around_tiles) and (not board.matrix_mines[x][y].opened):
                                    board.playing_field[x][y] = board.matrix_mines[x][y].value
                                    board.matrix_mines[x][y].opened = True                                
                                    board.empty_tiles_remain -= 1
                                    checked_around_tiles.add("{} {}".format(x, y))
        renpy.jump("minesweeper_game_win")

screen grid_minesweeper():
    grid SIZE SIZE:
        align (.5, .5)
        for i in range(SIZE):
            for j in range(SIZE):
                button:
                    left_padding 0
                    right_padding 0
                    top_padding 0
                    bottom_padding 0
                    background None
                    
                    if board.playing_field[i][j] == 9:
                        add "leaf_minesweeper"
                    elif board.playing_field[i][j] >= 0 and board.playing_field[i][j] <= 8:
                        add "{}".format(DIGITS[board.playing_field[i][j]])
                    else:
                        add "bug_minesweeper"

                    action If(board.matrix_mines[i][j].mine, Jump("minesweeper_game_over"), If(not board.matrix_mines[i][j].opened, Return("{} {} {}".format(board.matrix_mines[i][j].value, i, j))))
    text "Осталось открыть клеток: {}".format(board.empty_tiles_remain) xalign .5 yalign 0.1 size 40

screen grid_minesweeper_results():
    grid SIZE SIZE:
        align (.5, .5)
        for i in range(SIZE):
            for j in range(SIZE):
                button:
                    left_padding 0
                    right_padding 0
                    top_padding 0
                    bottom_padding 0
                    background None
                    
                    if board.matrix_mines[i][j].value == -1:
                        add "bug_minesweeper"
                    elif board.matrix_mines[i][j].value >= 0 and board.matrix_mines[i][j].value <= 8:
                        add "{}".format(DIGITS[board.matrix_mines[i][j].value])
                    else:
                        add "err"