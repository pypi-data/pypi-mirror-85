"""
Copyright (C) JheysonDev ~ All right reserved
"""
from colorama import init, Fore, Style


class Error:
    def __init__(self, msg: str = "Undefined error message"):
        self.msg: str = msg

    def run(self):
        print(
            Fore.RED
            + Style.BRIGHT
            + "Error: "
            + Fore.RESET
            + Style.RESET_ALL
            + self.msg
        )
