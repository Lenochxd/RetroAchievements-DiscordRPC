# Source: https://github.com/Lenochxd/WebDeck/blob/master/app/utils/restart.py

import os
import sys
from .exit import exit_program
from .logger import log


def restart_program():
    """Restarts the program, ensuring compatibility with frozen environments."""
    try:
        if getattr(sys, 'frozen', False):  # Check if the script is frozen
            os.startfile(sys.executable)
        else:
            # If not frozen, restart the Python interpreter
            python = sys.executable
            os.execl(python, f'"{python}"', *sys.argv)
        exit_program()
    except Exception as e:
        log.exception(e, "Error while restarting the program")