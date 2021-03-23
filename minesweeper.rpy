init:
    $ mods['everlasting_minesweeper'] = u'Бесконечный сапёр'

    image err = "images/numbers/err.png"
    image zero_minesweeper = "images/numbers/zero.png"
    image one_minesweeper = "images/numbers/one.png"
    image two_minesweeper = "images/numbers/two.png"
    image three_minesweeper = "images/numbers/three.png"
    image four_minesweeper = "images/numbers/four.png"
    image five_minesweeper = "images/numbers/five.png"
    image sex_minesweeper = "images/numbers/sex.png"
    image seven_minesweeper = "images/numbers/seven.png"
    image eight_minesweeper = "images/numbers/eight.png"

    image bug_minesweeper = "images/bug.png"
    image leaf_minesweeper = "images/leaf.png"

    image bg bgshka = "images/bgshka.png"

label everlasting_minesweeper:
    $ SIZE = 10  # Размер сетки
    $ AMOUNT_MINES = 20  # Кол-во мин
    $ game()

label minesweeper_game_win:
    $ Show("grid_minesweeper_results", transition=Dissolve(1.0))()
    $ renpy.hide_screen("grid_minesweeper")
    us "Надо же, ты победил!"
    jump minesweeper_end

label minesweeper_game_over:
    $ Show("grid_minesweeper_results", transition=Dissolve(1.0))()
    $ renpy.hide_screen("grid_minesweeper")
    us "Ты проиграл!"
    jump minesweeper_end

label minesweeper_end:
    $ Hide("grid_minesweeper_results", transition=Dissolve(1.0))()
    $ renpy.scene()
    $ renpy.show("black")
    show us smile pioneer close at center with dissolve
    us "Ну что, еще разок?"
    menu:
        "Да!":
            jump everlasting_minesweeper
        "Хватит с меня...":
            jump minesweeper_exit

label minesweeper_exit:
    show us grin pioneer close at center with dissolve
    us "Пока!"
