import tkinter as tk
import webbrowser
from utils.retroachievements import get_profile_data
from utils import get_config, save_config
from utils.exit import exit_program
from utils.logger import log

def text(input):
    return input

def ra_infos_prompt():
    def save_infos():
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

    def open_api_key_page():
        webbrowser.open("https://retroachievements.org/settings")

    def on_close():
        if config.get("ra_username") == "" or config.get("ra_api_key") == "":
            log.info("Prompt window closed without saving, RA infos not updated, exiting...")
            exit_program()
        else:
            log.info("Prompt window closed without saving, RA infos not updated.")
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
    
    api_key_entry = tk.Entry(frame, validate="key", width=10)
    api_key_entry.insert(0, config.get("ra_api_key"))  # Set default text field value to the current api key
    api_key_entry.grid(row=3, column=0, pady=5, sticky="w")
    
    find_api_key_button = tk.Button(frame, text=text("Find Key"), command=open_api_key_page)
    find_api_key_button.grid(row=3, column=0, padx=0, pady=5, sticky="e")
    
    save_button = tk.Button(frame, text=text("save"), command=save_infos)
    save_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

    # Key bindings
    prompt_window.bind("<Return>", lambda _: save_infos())
    prompt_window.bind("<Escape>", close_prompt)

    prompt_window.protocol("WM_DELETE_WINDOW", on_close)

    # Focus the window and the first text input
    prompt_window.lift()
    prompt_window.focus_force()
    username_entry.focus()

    prompt_window.mainloop()
    return
