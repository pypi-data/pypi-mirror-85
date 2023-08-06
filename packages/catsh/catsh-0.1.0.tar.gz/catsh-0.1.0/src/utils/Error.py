from colorama import init, Fore, Style


class Error:
    def __init__(self, msg="Undefined error message"):
        self.msg = msg

    def run(self):
        print(
            Fore.RED
            + Style.BRIGHT
            + "Error: "
            + Fore.RESET
            + Style.RESET_ALL
            + self.msg
        )
