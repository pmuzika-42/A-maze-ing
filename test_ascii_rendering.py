class Fore:
    GREY = "\x1b[1;30m"
    RED = "\x1b[1;31m"
    GREEN = "\x1b[1;32m"
    YELLOW = "\x1b[1;33m"
    BLUE = "\x1b[1;34m"
    MAGENTA = "\x1b[1;35m"
    CYAN = "\x1b[1;36m"
    WHITE = "\x1b[1;37m"
    RESET = "\x1b[0m"


class Back:
    GREY = "\x1b[1;40m"
    RED = "\x1b[1;41m"
    GREEN = "\x1b[1;42m"
    YELLOW = "\x1b[1;43m"
    BLUE = "\x1b[1;44m"
    MAGENTA = "\x1b[1;45m"
    CYAN = "\x1b[1;46m"
    WHITE = "\x1b[1;47m"
    RESET = "\x1b[0m"


def cprint(text: str, color: str) -> None:
    print(color + text + Fore.RESET)


cprint("Hola cyan", Back.CYAN)
print("Hola normal")
cprint("Hola rojo", Fore.RED)
cprint("Hola azul", Fore.BLUE)

# for i in range(30, 38):
#     print(f"\x1b[1;{i}mColor {i}\x1b[0m")

# print("\x1b[41mHola\x1b[0m")

# print('\x1b[1;31merror:\x1b[0m permission denied')
