import pystray
import sys
import webbrowser
from PIL import Image
from utils.exit import exit_program
from utils.restart import restart_program

icon = None

def text(input):
    return input

def generate_menu() -> pystray.Menu:
    return pystray.Menu(
        pystray.MenuItem(text('Options'), pystray.Menu(
            pystray.MenuItem(text('Restart the app'), restart_program),
        )),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(text('Report an Issue'), lambda: webbrowser.open('https://github.com/Lenochxd/RetroAchievements-DiscordRPC/issues')),
        pystray.MenuItem(text('Quit'), lambda: exit_program()),
    )

def generate_tray_icon():
    global icon
    image = Image.open("ra-icon.ico")

    menu = generate_menu()

    # Create the Tray Icon
    if getattr(sys, 'frozen', False):
        icon = pystray.Icon("name", image, "RetroRPC", menu)
    else:
        icon = pystray.Icon("name", image, "RetroRPC DEV", menu)
    return icon

def create_tray_icon():
    global icon
    if icon is None:  # Only create the icon if it doesn't already exist
        icon = generate_tray_icon()
        icon.run()
