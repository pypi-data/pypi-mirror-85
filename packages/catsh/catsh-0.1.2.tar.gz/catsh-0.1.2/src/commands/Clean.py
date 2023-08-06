"""
Copyright (C) JheysonDev ~ All right reserved
"""
import os
import platform


class CleanCommand:
    def __init__(self):
        self.command: str = ""

    def run(self):
        platform_name = platform.system()
        if platform_name == "Linux":
            self.command = "clear"
        elif platform_name == "Windows":
            self.command = "cls"
        elif platform_name == "Darwin":
            self.command = "clear"
        else:
            self.command = "clear"
        os.system(self.command)
