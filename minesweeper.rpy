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
    image flag_minesweeper = "images/flag.png"

    image btn_left_music = "images/btn_left_music.png"
    image btn_right_music = "images/btn_right_music.png"
    image btn_music_off = "images/btn_music_off.png"

    image amount_mines = "images/amount_mines.png"
    image btn_plus = "images/plus_btn.png"
    image btn_minus = "images/minus_btn.png"
    image btn_plus_three = "images/plus_three_btn.png"
    image btn_minus_three = "images/minus_three_btn.png"
    image btn_start = "images/start_btn.png"

    image bg bgshka = "images/bgshka.png"


label everlasting_minesweeper:
    $ day_time()
    $ persistent.sprite_time = "day"
    $ DEV = False
    $ AMOUNT_MINES = 20  # Кол-во мин
    $ SIZE = 10  # Размер сетки


label everlasting_minesweeper_start:
    scene bg ext_path2_day

    $ music_lst_minesweeper = ("everyday_theme", "i_want_to_play", "miku_song_voice", "a_promise_from_distant_days", "afterword", "always_ready", "confession_oboe", "dance_of_fireflies", "eat_some_trouble", "eternal_longing", "gentle_predator", "get_to_know_me_better", "glimmering_coals", "goodbye_home_shores", "heather", "into_the_unknown", "kostry", "lightness", "lets_be_friends", "memories", "miku_song_flute", "my_daily_life", "raindrops", "reminiscences", "she_is_kind", "silhouette_in_sunset")
    $ cnt_music = 0
    
    $ renpy.block_rollback()
    $ renpy.call_screen("select_amount_mines")


label everlasting_minesweeper2:
    $ renpy.block_rollback()
    $ renpy.scene("ext_path2_day")
    $ renpy.show_screen("music_player_minesweeper")

    $ game()


##### Концовки


label minesweeper_game_win:
    $ Show("grid_minesweeper_results", transition=Dissolve(1.0))()
    $ renpy.hide_screen("grid_minesweeper")
    if AMOUNT_MINES >= 40:
        us "Надо же, везения тебе не занимать..."
    us "Надо же, ты победил!"
    jump minesweeper_end


label minesweeper_game_over:
    $ Show("grid_minesweeper_results", transition=Dissolve(1.0))()
    $ renpy.hide_screen("grid_minesweeper")
    us "Ты проиграл!"
    jump minesweeper_end


label minesweeper_end:
    $ Hide("grid_minesweeper_results", transition=Dissolve(1.0))()
    $ Hide("music_player_minesweeper", transition=Dissolve(1.0))()
    $ renpy.scene()
    $ renpy.show("ext_path2_day")
    show us smile pioneer close at center with dissolve
    us "Ну что, еще разок?"
    menu:
        "Да!":
            jump everlasting_minesweeper_start
        "Хватит с меня...":
            jump minesweeper_exit

label minesweeper_exit:
    show us grin pioneer close at center with dissolve
    us "Пока!"
