"""
Copyright (C) JheysonDev ~ All right reserved
"""
import os
import platform


class Config:
    def __init__(self):
        self.prompt: str
        self.prompt_color: str
        self.commands: dict
        self.config_file: str
        self.home_path: str = ""
        self.platform_name: str = ""

    def platform(self):
        self.platform_name = platform.system()
        print(self.platform_name)

    def paths(self):
        if self.platform_name == "Linux" or "Darwin":
            self.home_path = os.path.expanduser("~")
        elif self.platform_name == "Windows":
            self.home_path = os.path.expanduser("%USERPROFILE%")

    def prompt(self):
        self.prompt = "-| "


config = Config()
config.platform()