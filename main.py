import time
import utils
import ctypes
import webbrowser
import PySimpleGUI as sg

battle_timer_seconds = 120
number_of_levels_clear = 0
menu = sg.Window("Trickcal Revive")


def create_menu_gui():
    # Set a Layout
    layout = [
        [sg.Text("Stay on the Page then activate", key="row1", text_color="#509296", font=("Helvetica", 14, "bold"),
                 background_color="#f0f0f0")],
        [sg.Text("Please Adjust the screen before using", key="row2", text_color="#509296",
                 font=("Helvetica", 12, "bold"), background_color="#f0f0f0")],
        [sg.Multiline('', key='_Multiline_', size=(48, 7), autoscroll=True)],

        [sg.Button("Adjust Screen", key="adjust_screen", button_color="#509296")] +
        [sg.Button("Edit Battle Timer", key="battle_timer", button_color="#509296")],
        [sg.Button("Clear MQ or Event ", key="main_story_or_event", button_color="#509296")] +
        [sg.Button("How To Use ", key="help_mq", button_color="#509296")],
        [sg.Button("Clear Dungeon      ", key="dungeon", button_color="#509296")] +
        [sg.Button("How To Use ", key="help_dungeon", button_color="#509296")],

        [sg.Text("Please leave a star on my github if it helps ><", key="github",
                 enable_events=True, text_color='blue', background_color="#f0f0f0")]
    ]

    # menu setting
    # Get the screen width and height

    screen_resolution_width = ctypes.windll.user32.GetSystemMetrics(0)

    menu_width = screen_resolution_width - 430
    menu_height = 30

    menu_popup_location = (menu_width, menu_height)  # Specify the desired coordinates of the menu
    menu_size = (420, 400)  # Width, Height
    menu_theme = "SystemDefaultForReal"  # Replace with the desired theme name
    sg.theme(menu_theme)

    global menu
    menu = sg.Window("Trickcal Revive", layout, location=menu_popup_location, keep_on_top=True, size=menu_size)


def menu_function():
    global menu
    # Get screen resolution
    screen_resolution_height = ctypes.windll.user32.GetSystemMetrics(1)

    while True:
        # Read user event
        event, values = menu.read()

        # Close app
        if event is None or event == sg.WINDOW_CLOSED:
            break

        # Screen resolution only accept 1920x1080
        if screen_resolution_height != 1080:
            utils.update_gui_msg("Only Screen Resolution 1920x1080 Work!!\n", menu)
            time.sleep(3)
            return

        if event == "adjust_screen" and screen_resolution_height == 1080:
            menu["row1"].update("Adjust Screen...")
            menu.refresh()
            utils.adjust_screen(menu)

        if event == "main_story_or_event":
            menu["row1"].update("Level Clear : 0\n")
            menu["row2"].update("Finding New Level...", text_color="#509296", font=("Helvetica", 12, "bold"),
                                background_color="#f0f0f0")
            clear_mq_event()

        if event == "help_mq":
            sg.popup_no_buttons("", title="Start the program over here ", keep_on_top=True,
                                image="img/help_demo1.png")

        if event == "dungeon":
            menu["row1"].update("Level Clear : 0\n")
            menu["row2"].update("Looking for Level", text_color="#509296", font=("Helvetica", 12, "bold"),
                                background_color="#f0f0f0")
            clear_dungeon()

        if event == "help_dungeon":
            sg.popup_no_buttons("", title="Start the program over here, Works for other as well ", keep_on_top=True,
                                image="img/help_demo2.png")

        if event == "battle_timer":
            global battle_timer_seconds

            battle_timer_seconds = sg.popup_get_text("Enter Battle Timer in Seconds: (Default is 120 seconds)")

        if event == "github":
            webbrowser.open("https://github.com/chong12007/Trickcal_Revive_auto_clear_level")


def clear_mq_event():
    while True:
        def is_battle_start():
            global menu
            max_error_count = 3
            error_count = 0

            while error_count < max_error_count:
                try:
                    coordinate = utils.get_icon_coordinate("img/new_level_icon.png")
                    if coordinate is None:
                        raise Exception

                    utils.click(coordinate, "New Level detected\n", menu)
                    coordinate = utils.get_icon_coordinate("img/enter_level_icon.png")
                    utils.click(coordinate, "Entering New Level\n", menu)
                    coordinate = utils.get_icon_coordinate("img/start_level.png")
                    utils.click(coordinate, "Start battle\n", menu)
                    error_count = 0
                    return True

                except Exception:  # Increment the error count
                    error_count += 1
                    coordinate = utils.get_icon_coordinate("img/start_level.png")

                    if coordinate is not None:
                        utils.click(coordinate, "Start battle\n", menu)
                        return True

                    if error_count == max_error_count:
                        return False

        battle_started = is_battle_start()

        if battle_started is False:
            global menu
            utils.update_gui_msg("Error Occur on Finding New Level\n", menu)
            utils.update_gui_msg("Please Select Task again...\n", menu)
            return

        battle_process()


def battle_process():
    is_battle_ended = False
    global number_of_levels_clear
    global battle_timer_seconds
    battle_timer_seconds = int(battle_timer_seconds)

    try:
        while not is_battle_ended:
            # Sleep to wait battle to end
            msg = f"Sleep {battle_timer_seconds} Seconds\n"
            utils.update_gui_msg(msg, menu)
            time.sleep(battle_timer_seconds)

            # Check is battle ended
            coordinate = utils.get_icon_coordinate("img/continue_to_next_level_icon.png")
            # Battle not ended yet, wait again
            if coordinate is None:
                utils.update_gui_msg("Battle still not ended yet\n", menu)
                continue

            is_battle_ended = True

            number_of_levels_clear += 1
            msg = f"Level Clear : {number_of_levels_clear}\n"
            menu["row1"].update(msg)

            utils.click(coordinate, "Continue to next level\n", menu)
            utils.click(coordinate, "Sleep 25 Seconds for animation\n", menu)
            time.sleep(25)

            coordinate = (coordinate[0] - 300, coordinate[1])
            utils.click(coordinate, "", menu)
            time.sleep(2)

    except Exception as e:
        pass


def clear_dungeon():
    global menu

    coordinate = get_dungeon_level_entry_coordinate()
    if coordinate is None:
        utils.update_gui_msg("Error Occur on Finding Entry\n", menu)
        utils.update_gui_msg("Please Select Task again...\n", menu)
        return

    utils.click(coordinate, "Entering Level\n", menu)

    error_count = 0

    while True:
        try:
            coordinate = utils.get_icon_coordinate("img/start_level.png")
            utils.click(coordinate, "Start battle\n", menu)
            battle_process()
            error_count = 0

        except TypeError:
            error_count += 1
            if error_count == 3:
                utils.update_gui_msg("Error Occur on Starting Level\n", menu)
                utils.update_gui_msg("Please Select Task again...\n", menu)
                return


def get_dungeon_level_entry_coordinate():
    i = 1
    while i < 6:
        image_to_find_name = f"img/enter_level_icon{i}.png"
        coordinate = utils.get_icon_coordinate(image_to_find_name)
        if coordinate is None:
            i += 1
            continue
        return coordinate
    return None


if __name__ == '__main__':
    create_menu_gui()
    menu_function()
