import os
import sys
import pystray
import webbrowser
from PIL import Image
from utils import log, get_config, save_config
from utils.exit import exit_program
from utils.restart import restart_program
from utils.ui.prompt_window import ra_infos_prompt

icon = None

def update_menu():
    # Rebuild and apply the updated menu
    icon.menu = generate_menu()
    icon.update_menu()
    return

def set_sleeping_time(sleep_time: int) -> None:
    config = get_config()
    config["sleeping_time"] = sleep_time
    save_config(config)
    
    update_menu()
    return


activity_choices = {"retroachievements": 1337553980779266078, "retroarch": 1337553668148297818}

def get_config_choice() -> str:
    config = get_config()
    for choice, client_id in activity_choices.items():
        if client_id == config["discord_client_id"]:
            return choice
    return "retroachievements"

def set_config_choice(choice: str) -> None:
    choice = choice.lower()
    config = get_config()
    config["activity_title"] = choice
    config["discord_client_id"] = activity_choices[choice]
    save_config(config)
    
    update_menu()
    return


startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'RARPC.lnk')

def get_startup() -> bool:
    if not getattr(sys, 'frozen', False):
        return False

    return os.path.exists(startup_path)

def set_startup(startup: bool) -> None:
    if not getattr(sys, 'frozen', False):
        log.error("Cannot set startup option when not frozen.")
        return

    target_path = os.path.join(os.path.dirname(sys.executable), 'RARPC.exe')

    if startup:
        if not os.path.exists(startup_path):
            os.symlink(target_path, startup_path)
    else:
        if os.path.exists(startup_path):
            os.remove(startup_path)

    update_menu()
    return


def get_force_presence() -> bool:
    config = get_config()
    return config.get("force_presence", False)

def toggle_force_presence() -> None:
    config = get_config()
    config["force_presence"] = not config.get("force_presence", False)
    save_config(config)
    
    update_menu()
    return


def text(input):
    return input

def generate_menu() -> pystray.Menu:
    config = get_config()
    
    return pystray.Menu(
        pystray.MenuItem(text('Options'), pystray.Menu(
            
            pystray.MenuItem(text('Edit RA infos'), ra_infos_prompt),
            pystray.MenuItem(text('Activity title'), pystray.Menu(
                pystray.MenuItem(text('RetroAchievements'), lambda: set_config_choice('retroachievements'), checked=lambda item: get_config_choice() == 'retroachievements'),
                pystray.MenuItem(text('RetroArch'), lambda: set_config_choice('retroarch'), checked=lambda item: get_config_choice() == 'retroarch'),
            )),
            pystray.MenuItem(text('Change sleeping time'), pystray.Menu(
                pystray.MenuItem(text('2s'), lambda: set_sleeping_time(2), checked=lambda item: config.get('sleeping_time', 10) == 2),
                pystray.MenuItem(text('5s'), lambda: set_sleeping_time(5), checked=lambda item: config.get('sleeping_time', 10) == 5),
                pystray.MenuItem(text('10s'), lambda: set_sleeping_time(10), checked=lambda item: config.get('sleeping_time', 10) == 10),
                pystray.MenuItem(text('15s'), lambda: set_sleeping_time(15), checked=lambda item: config.get('sleeping_time', 10) == 15),
                pystray.MenuItem(text('20s'), lambda: set_sleeping_time(20), checked=lambda item: config.get('sleeping_time', 10) == 20),
                pystray.MenuItem(text('25s'), lambda: set_sleeping_time(25), checked=lambda item: config.get('sleeping_time', 10) == 25),
                pystray.MenuItem(text('30s'), lambda: set_sleeping_time(30), checked=lambda item: config.get('sleeping_time', 10) == 30),
                pystray.MenuItem(text('40s'), lambda: set_sleeping_time(40), checked=lambda item: config.get('sleeping_time', 10) == 40),
                pystray.MenuItem(text('50s'), lambda: set_sleeping_time(50), checked=lambda item: config.get('sleeping_time', 10) == 50),
                pystray.MenuItem(text('60s'), lambda: set_sleeping_time(60), checked=lambda item: config.get('sleeping_time', 10) == 60),
            )),
            pystray.MenuItem(text('Force presence'), lambda: toggle_force_presence(), checked=lambda item: get_force_presence()),
            pystray.MenuItem(text('Start on Startup'), lambda: set_startup(not get_startup()), checked=lambda item: get_startup),
        )),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(text('Report an Issue'), lambda: webbrowser.open('https://github.com/Lenochxd/RetroAchievements-DiscordRPC/issues')),
        pystray.MenuItem(text('Restart'), restart_program),
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
