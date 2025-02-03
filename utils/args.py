# Source: https://github.com/Lenochxd/WebDeck/blob/master/app/utils/args.py

import sys
import argparse
from .logger import log
from utils.get_config import get_config

config = get_config()
args = {}
raw_args = [arg for arg in sorted(sys.argv[1:]) if not (arg.endswith('.pyc') or arg.endswith('library.zip'))]
# log.debug(f"{raw_args=}")

available_args = {
    "--debug": {
        "aliases": ["-d"],
        "help": "Print debug information",
        "action": "store_true"
    },
    "-t": {
        "aliases": ["--fetch", "--time"],
        "help": "Time to sleep before fetches in seconds",
        "type": int,
        "default": config.get('sleeping_time', 10),
        "action": "store"
    },
}

parser, parsed_args = None, None
def parse_args():
    global parser, parsed_args
    
    # Set up argument parser
    parser = argparse.ArgumentParser()
    
    # Add arguments to the parser
    for arg, arg_params in available_args.items():
        if not arg_params.get("condition", True):
            continue
        
        if "type" in arg_params:
            parser.add_argument(
                arg,
                *arg_params.get("aliases", []),
                help=arg_params.get("help"),
                type=arg_params["type"],
                default=arg_params.get('default'),
                action=arg_params.get("action", None),
            )
        else:
            parser.add_argument(
                arg,
                *arg_params.get("aliases", []),
                help=arg_params.get("help"),
                action=arg_params.get("action", None),
            )
    
    
    try:
        # Parse the arguments
        parsed_args = parser.parse_args(raw_args)
        if get_arg('debug'):
            log.debug(f'All args: {parsed_args}')
    except Exception as e:
        log.error(f"Error parsing arguments: {e}")
    
    handle_startup_arguments()
    
    return parsed_args


def load_args():
    """
    Load arguments from the temporary file if available, otherwise return an empty dictionary.
    
    Returns:
        dict: A dictionary containing the loaded arguments.
    """
    global parsed_args
    if parsed_args:
        return vars(parsed_args)
    return {}

def get_arg(arg):
    """
    Retrieve the value of a specified argument from the loaded arguments.
    Args:
        arg (str): The name of the argument to retrieve.
    Returns:
        Union[str, bool, None]: The value of the specified argument if it exists, otherwise None.
    """
    
    return load_args().get(arg, None)


def handle_startup_arguments():
    # --debug
    if not get_arg('debug'):
        log.disable_debug()
