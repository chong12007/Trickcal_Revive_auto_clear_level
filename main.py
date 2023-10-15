import time
import utils
import ctypes
import webbrowser
import PySimpleGUI as sg
import pygetwindow as gw


def display_ui():
    # Set a Layout
    layout = [
        [sg.Text("Stay on the Page then activate", key="row1", text_color="#509296", font=("Helvetica", 14, "bold"),
                 background_color="#f0f0f0")],
        [sg.Text("Please Adjust the screen before using", key="row2", text_color="#509296",
                 font=("Helvetica", 12, "bold"), background_color="#f0f0f0")],
        [],
        [sg.Multiline('', key='_Multiline_', size=(48, 7), autoscroll=True)],
        [sg.Button("Adjust Screen", key="adjust_screen", button_color="#509296")],
        [sg.Button("Start Clear Level ", key="start", button_color="#509296")],
        [sg.Text("Please leave a star on my github if this script helps you T^T,Click me to github", key="github",
                 enable_events=True, text_color='blue', background_color="#f0f0f0")]
    ]

    # menu setting
    # Get the screen width and height

    screen_resolution_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_resolution_height = ctypes.windll.user32.GetSystemMetrics(1)

    menu_width = screen_resolution_width - 430
    menu_height = 30

    menu_popup_location = (menu_width, menu_height)  # Specify the desired coordinates of the menu
    menu_size = (400, 350)  # Width, Height
    menu_theme = "SystemDefaultForReal"  # Replace with the desired theme name
    sg.theme(menu_theme)

    menu = sg.Window("MHN", layout, location=menu_popup_location, keep_on_top=True, size=menu_size)

    # Infinite Loop
    while True:
        # Read user event
        event, values = menu.read()

        if event == "start":
            menu["row1"].update("Start Finding New Level...\n")
            clear_battle(menu)

        if event == "adjust_screen" and screen_resolution_height == 1080:
            if screen_resolution_height != 1080:
                utils.update_gui_msg("Only Screen Resolution 1920x1080 Work!!\n", menu)
                time.sleep(3)
                return

            menu["row1"].update("Adjust Screen...")
            menu.refresh()
            adjust_screen(menu)
            pass

        if event == "github":
            webbrowser.open("https://github.com/chong12007/Monster_Hunter_Now_auto_script")

        # Close app
        if event is None or event == sg.WINDOW_CLOSED:
            break


def adjust_screen(menu):
    def is_app_running():
        app_titles = ["BlueStacks", "MEmu", "Nox"]

        # Find the window with a matching title
        app_is_running = None
        # Test all title
        for title in app_titles:
            try:
                app_is_running = gw.getWindowsWithTitle(title)[0]
                break
            except IndexError:
                pass

        if app_is_running:
            return app_is_running
        else:
            return None

    app_window = is_app_running()

    if app_window is None:
        def app_not_found(menu):
            menu["row1"].update("Error :(", text_color="red", font=("Helvetica", 16, "bold"),
                                background_color="#f0f0f0")
            menu["row2"].update("Unable to detect Emulator", text_color="red", font=("Helvetica", 12, "bold"),
                                background_color="#f0f0f0")
            utils.update_gui_msg("Supported Emulator :\nBlueStacks(Tested)\nMEmu\nNox\n\n\n", menu)
            menu.refresh()

        app_not_found(menu)
        return

    # Resize the window
    app_window.resizeTo(998, 577)

    # Get Screen Center
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    window_width = app_window.width
    window_height = app_window.height

    screen_center_x = (screen_width - window_width) // 2
    screen_center_y = (screen_height - window_height) // 2

    app_window.activate()

    # Select app
    time.sleep(1)
    # Move the window to the center of the screen
    app_window.moveTo(screen_center_x, screen_center_y)

    menu["row1"].update("Screen Adjusted!!", text_color="#509296", font=("Helvetica", 16, "bold"),
                        background_color="#f0f0f0")
    menu["row2"].update("yay d >w< b yay", text_color="#509296", font=("Helvetica", 12, "bold"),
                        background_color="#f0f0f0")
    menu.refresh()


def start_battle_process(menu):
    max_error_count = 3
    error_count = 0

    while error_count < max_error_count:
        try:
            coordinate = utils.get_icon_coordinate("img/new_level.png")
            if coordinate is None:
                raise Exception

            utils.click(coordinate, "New Level detected\n", menu)
            coordinate = utils.get_icon_coordinate("img/battle_entry.png")
            utils.click(coordinate, "Entering battle\n", menu)
            coordinate = utils.get_icon_coordinate("img/start_battle.png")
            utils.click(coordinate, "Start battle\n", menu)
            error_count = 0
            return True

        except Exception as e:  # Increment the error count
            error_count += 1

            if error_count == max_error_count:
                utils.update_gui_msg("Error Occur on Starting battle\n", menu)
                return False


def clear_battle(menu):
    while True:
        is_battle_start = start_battle_process(menu)
        if is_battle_start is False:
            utils.update_gui_msg("Error Occur on Finding New Level\n", menu)
            utils.update_gui_msg("Please Press Start again...\n", menu)
            return

        try:
            is_battle_ended = False
            while not is_battle_ended:
                utils.update_gui_msg("Sleep 150 Seconds\n", menu)
                time.sleep(150)
                coordinate = utils.get_icon_coordinate("img/continue_battle.png")
                if coordinate is None:
                    utils.update_gui_msg("Battle still not ended yet\n", menu)
                    continue

                is_battle_ended = True
                utils.click(coordinate, "Continue to next level\n", menu)
                utils.click(coordinate, "Sleep 20 Seconds for animation", menu)
                time.sleep(20)
                utils.click(coordinate, "", menu)

        except Exception as e:
            pass


if __name__ == '__main__':
    display_ui()
