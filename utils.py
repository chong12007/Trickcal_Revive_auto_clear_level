import time
import pyautogui
import cv2

msg_history = ''


def update_gui_msg(msg, menu):
    global msg_history

    msg_history += msg
    menu.Element('_Multiline_').Update(msg_history, font=("Helvetica", 10, "bold"))
    menu.refresh()


def click(coordinate, msg, menu):
    update_gui_msg(msg, menu)
    menu.refresh()
    pyautogui.click(coordinate[0], coordinate[1], button="left")
    time.sleep(1)


def get_icon_coordinate(icon_path):
    screenshot = pyautogui.screenshot()
    screenshot.save("img/screenshot.png")
    screenshot_path = "img/screenshot.png"
    screenshot = cv2.imread(screenshot_path)

    # Load template image
    template = cv2.imread(icon_path)
    # Perform template matching on the ROI
    result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)

    # Get the matched location within the ROI
    # Set a threshold for the match
    threshold = 0.03

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val)

    if min_val < threshold:
        top_left = (min_loc[0], min_loc[1])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        click_coordinate = (center[0], center[1])
        print(click_coordinate)
        return click_coordinate
    else:
        return None


if __name__ == '__main__':
    coordinate = get_icon_coordinate("img/new_level.png")
