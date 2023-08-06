from colorama import init, Fore, Style


class Warning:
    def __init__(self, msg="Undefined warning message"):
        self.msg = msg

    def run(self):
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "Warning: "
            + Fore.RESET
            + Style.RESET_ALL
            + self.msg
        )
