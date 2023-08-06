"""
Copyright (C) JheysonDev ~ All right reserved
"""


class PrintCommand:
    def __init__(self, msg):
        self.msg = msg

    def run(self):
        print(self.msg)