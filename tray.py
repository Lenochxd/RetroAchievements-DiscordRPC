import pystray
import sys
import webbrowser
import tkinter as tk
from PIL import Image
from utils.retroachievements import get_profile_data
from utils.exit import exit_program
from utils.restart import restart_program
from utils.save_config import save_config
from utils.get_config import get_config

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
    

def ra_infos_prompt():
    def save_port():
        new_username = username_entry.get()
        new_api_key = api_key_entry.get()
        
        if not validate_inputs(new_username, new_api_key):
            prompt_window.geometry("300x190")
            error_label.config(text="Invalid username or API key", fg="red")
            return
        
        prompt_window.destroy()  # Close the window if save is successful
        
        config = get_config()
        config['ra_username'] = new_username
        config['ra_api_key'] = new_api_key
        save_config(config)
        return

    def validate_inputs(new_username: str, new_api_key: str) -> bool:
        return bool(new_username and new_api_key and get_profile_data(new_username, new_api_key))

    def close_prompt(event=None):
        prompt_window.destroy()

    config = get_config()
    
    prompt_window = tk.Tk()
    prompt_window.title(text('Edit RetroAchievements Infos'))
    prompt_window.geometry("300x180")
    prompt_window.resizable(False, False)
    prompt_window.iconbitmap("ra-icon.ico")

    frame = tk.Frame(prompt_window, padx=10, pady=10)
    frame.pack(expand=True)
    
    error_label = tk.Label(frame, text="", fg="red")
    error_label.grid(row=5, column=0, pady=0, sticky="w")

    username_label = tk.Label(frame, text=text("Username:"))
    username_label.grid(row=0, column=0, pady=5, sticky="w")
    
    username_entry = tk.Entry(frame, validate="key")
    username_entry.insert(0, config.get("ra_username"))  # Set default text field value to the current username
    username_entry.grid(row=1, column=0, pady=5, sticky="ew")
    
    api_key_label = tk.Label(frame, text=text("API Key:"))
    api_key_label.grid(row=2, column=0, pady=5, sticky="w")
    
    api_key_entry = tk.Entry(frame, validate="key")
    api_key_entry.insert(0, config.get("ra_api_key"))  # Set default text field value to the current api key
    api_key_entry.grid(row=3, column=0, pady=5, sticky="ew")
    
    save_button = tk.Button(frame, text=text("save"), command=save_port)
    save_button.grid(row=4, column=0, pady=5, sticky="ew")

    # Key bindings
    prompt_window.bind("<Return>", lambda event: save_port())
    prompt_window.bind("<Escape>", close_prompt)

    # Focus the window and the first text input
    prompt_window.lift()
    prompt_window.focus_force()
    username_entry.focus()

    prompt_window.mainloop()

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
