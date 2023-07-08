from colored import Fore, Back, Style
from sys import stderr

def log(message: str, level: str = "info"):
    if level == "info":
        print(f"{Fore.dark_gray}INFO: {message}{Style.reset}")
    elif level == "warn":
        print(f"{Fore.light_yellow}WARN: {message}{Style.reset}", file=stderr)
    elif level == "error":
        print(f"{Fore.red}ERROR: {message}{Style.reset}", file=stderr)
    elif level == "success":
        print(f"{Fore.green_3a}SUCCESS: {message}{Style.reset}")
