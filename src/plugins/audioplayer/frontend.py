from colorama import Fore, Style

class Terminal():
    def __init__(self) -> None:
        self.clear_screen = lambda: print("\033c\033[3J", end='')
        self.spacer = " " * 80

    def write_line(self, text) -> None:
        self.clear_sreen()
        print("{}{}{}{}".format(Style.BRIGHT, Fore.GREEN, text, Style.RESET_ALL))

    def write_line2(self, text1, text2) -> None:
        print("{}{}{} {}{}{}{}".format(Style.BRIGHT, Fore.YELLOW,text1), Style.RESET_ALL, Style.BRIGHT, Fore.WHITE, text2, Style.RESET_ALL)

