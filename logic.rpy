init python:
    import random
    from collections import deque

    class Tile:
        def __init__(self):
            self.mine = False
            self.value = 0
            self.opened = False
            self.flag = False

            
    class BoardMinesweeper:
        def __init__(self, size, amount_mines):
            self.size = size
            self.amount_mines = amount_mines
            self.matrix_mines = [[Tile() for i in range(self.size)] for j in range(self.size)]
            self.playing_field = [[9 for i in range(self.size)] for j in range(self.size)]
            self.adjacency_list = {}
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


        def fillField(self, flag=False, first_x=0, first_y=0):
            amount = self.amount_mines
            while amount > 0:
                x = random.Random().randrange(self.size)
                y = random.Random().randrange(self.size)
                if flag and x == first_x and y == first_y:
                    continue
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
        renpy.show("bg ext_path2_day")
        renpy.show("bgshka")
        renpy.show_screen("grid_minesweeper")
        if DEV:
            renpy.show_screen("otladka")

        first = True
        while board.empty_tiles_remain:
            result, i, j = [int(z) for z in ui.interact().split()]
            if result == 79857480:
                board.matrix_mines[i][j].flag = True
            elif result == 79857481:
                board.matrix_mines[i][j].flag = False
            if first and result == -1: 
                board = BoardMinesweeper(SIZE, AMOUNT_MINES)
                board.fillField(True, i, j)
                result = board.matrix_mines[i][j].value
            first = False
            renpy.pause(0.1, hard=True)
            if result > 0 and result <= 8:
                board.playing_field[i][j] = result
                board.matrix_mines[i][j].opened = True
                board.empty_tiles_remain -= 1
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
            elif result == -1:
                renpy.jump("minesweeper_game_over")
            renpy.pause(0.1, hard=True)
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
                    
                    if board.matrix_mines[i][j].flag and not board.matrix_mines[i][j].opened:
                        add "flag_minesweeper"
                    elif board.playing_field[i][j] == 9:
                        add "leaf_minesweeper"
                    elif board.playing_field[i][j] >= 0 and board.playing_field[i][j] <= 8:
                        add "{}".format(DIGITS[board.playing_field[i][j]])
                    else:
                        add "bug_minesweeper"

                    alternate If(board.matrix_mines[i][j].flag, Return("79857481 {} {}".format(i, j)), Return("79857480 {} {}".format(i, j)))
                    # Прям регулярка какая-то
                    action If(board.matrix_mines[i][j].flag, Return("79857481 {} {}".format(i, j)), If(board.matrix_mines[i][j].mine, Return("{} {} {}".format(board.matrix_mines[i][j].value, i, j)), If(not board.matrix_mines[i][j].opened or board.matrix_mines[i][j].flag, Return("{} {} {}".format(board.matrix_mines[i][j].value, i, j)))))
   
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


screen music_player_minesweeper():
    button:
        xalign .5 yalign .96

        left_padding 0
        right_padding 0
        top_padding 0
        bottom_padding 0
        background None

        add "btn_music_off"
        action Stop("music")

    button:
        xalign .45 yalign .9

        left_padding 0
        right_padding 0
        top_padding 0
        bottom_padding 0
        background None
        
        add "btn_left_music"
        action [SetVariable("cnt_music", (cnt_music - 1)%len(music_lst_minesweeper)), Play("music", music_list[music_lst_minesweeper[cnt_music]])]

    button:
        xalign .55 yalign .9

        left_padding 0
        right_padding 0
        top_padding 0
        bottom_padding 0
        background None
        
        add "btn_right_music"
        action [SetVariable("cnt_music", (cnt_music + 1)%len(music_lst_minesweeper)), Play("music", music_list[music_lst_minesweeper[cnt_music]])]

    text "Музыка" xalign .5 yalign .9 


screen select_amount_mines():
    add "ext_path2_day"
    add "bgshka"
    add "amount_mines"
    text "{color=#25231f}{size=148}%s{/size}{/color}" % AMOUNT_MINES xalign .5 yalign .43

    button:
        xalign .47 yalign .6

        left_padding 0
        right_padding 0
        top_padding 0
        bottom_padding 0
        background None

        add "btn_minus"

        action If(AMOUNT_MINES > 10, SetVariable("AMOUNT_MINES", AMOUNT_MINES - 1))

    button:
        xalign .41 yalign .6

        left_padding 0
        right_padding 0
        top_padding 0
        bottom_padding 0
        background None

        add "btn_minus_three"

        action If(AMOUNT_MINES > 12, SetVariable("AMOUNT_MINES", AMOUNT_MINES - 3))

    button:
        xalign .53 yalign .6

        left_padding 0
        right_padding 0
        top_padding 0
        bottom_padding 0
        background None

        add "btn_plus"

        action If(AMOUNT_MINES < 50, SetVariable("AMOUNT_MINES", AMOUNT_MINES + 1))

    button:
        xalign .59 yalign .6

        left_padding 0
        right_padding 0
        top_padding 0
        bottom_padding 0
        background None

        add "btn_plus_three"

        action If(AMOUNT_MINES < 48, SetVariable("AMOUNT_MINES", AMOUNT_MINES + 3))

    button:
        xalign .5 yalign .71

        left_padding 0
        right_padding 0
        top_padding 0
        bottom_padding 0
        background None

        add "btn_start"

        action Jump("everlasting_minesweeper2")


#####


screen otladka():
    grid SIZE SIZE:
        align (0, .5)
        for i in range(SIZE):
            for j in range(SIZE):
                button:
                    left_padding 0
                    right_padding 0
                    top_padding 0
                    bottom_padding 0
                    background None
                    
                    if board.matrix_mines[i][j].value == -1:
                        text "-1"
                    elif board.matrix_mines[i][j].value >= 0 and board.matrix_mines[i][j].value <= 8:
                        text str(board.matrix_mines[i][j].value)
                    else:
                        add "err"

    grid SIZE SIZE:
        align (0, .9)
        for i in range(SIZE):
            for j in range(SIZE):
                button:
                    left_padding 0
                    right_padding 0
                    top_padding 0
                    bottom_padding 0
                    background None
                    
                    if board.matrix_mines[i][j].opened:
                        text "o"
                    elif not board.matrix_mines[i][j].opened:
                        text "c"
                    else:
                        add "err"


    grid SIZE SIZE:
        align (.9, 0)
        for i in range(SIZE):
            for j in range(SIZE):
                button:
                    left_padding 0
                    right_padding 0
                    top_padding 0
                    bottom_padding 0
                    background None
                    
                    if board.matrix_mines[i][j].flag:
                        text "t"
                    else:
                        text "f"

    textbutton "Retry" action Jump("everlasting_minesweeper")
