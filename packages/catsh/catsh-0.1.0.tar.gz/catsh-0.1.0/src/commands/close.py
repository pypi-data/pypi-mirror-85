import sys


class CloseCommand:
    def __init__(self, code=0, msg=""):
        self.exit_code: int = code
        self.msg: str = msg

    def run(self):
        print(f"Exit: {self.exit_code}, {self.msg}")
        sys.exit(self.exit_code)