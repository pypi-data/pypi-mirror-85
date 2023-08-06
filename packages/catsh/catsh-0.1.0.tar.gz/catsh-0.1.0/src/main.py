from commands import close, clean, Print
from utils import Error
from colorama import Fore


class Main:
    def __init__(self, prompt="-| "):
        self.prompt = prompt
        self.cli = input(self.prompt)

    def shell(self):
        while self.cli:
            command = self.cli
            if command.startswith("print"):
                command = command.split(" ", 1)
                Print.PrintCommand(command[1]).run()
            else:
                Error.Error("Command no found").run()
            self.cli = input(self.prompt)


if __name__ == "__main__":
    main = Main()
    main.shell()
