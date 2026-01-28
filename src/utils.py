import os
import platform
import pwinput
from colorama import init, Fore, Style

init(autoreset=True)

class Utils:
    
    @staticmethod
    def clear_screen():
        command = 'cls' if platform.system() == 'Windows' else 'clear'
        os.system(command)

    @staticmethod
    def pause():
        input(f"\n{Style.DIM}>> Press Enter to continue...{Style.RESET_ALL}")

    @staticmethod
    def input_password(prompt="Password: "):
        return pwinput.pwinput(prompt=f"{Fore.CYAN}{prompt}{Style.RESET_ALL}", mask="*")

    @staticmethod
    def print_success(message):
        print(f"{Fore.GREEN} SUCCESS: {message}")

    @staticmethod
    def print_error(message):
        print(f"{Fore.RED} ERROR: {message}")

    @staticmethod
    def print_warning(message):
        print(f"{Fore.YELLOW}  WARNING: {message}")
        
    @staticmethod
    def print_header(message):
        print(f"\n{Fore.BLUE}{Style.BRIGHT}=== {message.upper()} ==={Style.RESET_ALL}")