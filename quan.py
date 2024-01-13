###########
#     Imports     #
###########

import sys
import os

from colorama import init, Fore, Back, Style
from colorama import just_fix_windows_console

from src.lexer import lex
from src.error import error

from src.linux_builder import build_linux
from src.windows_builder import build_windows

########
#     Run     #
########

def handleArgv(argv: list) -> list:
    result = []
    if len(argv) == 3:
        result = [argv[1], argv[2]]
    else:
        error(\
f"""{Fore.RED}[Error: Invalid usage!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
Proper usage: quan [input.quan] [platform => (linux, windows)]""", sys.exit)
        
    return result

def checkPlatform(platform):
    if platform in ["linux", "windows"]:
        result = platform
    else:
        error(\
f"""{Fore.RED}[Error: Invalid usage!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
Proper usage: quan [input.quan] [platform => (linux, windows)]""", sys.exit)

    return result

def getFile(path: str) -> str:
    result = ""
    if os.path.exists(path):
        result = open(path, "r", encoding="utf-8").read()
    else:
        error(\
f"""{Fore.RED}[Error: Invalid usage!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
Proper usage: quan [input.quan] [platform => (linux, windows)]""", sys.exit)
        
    return result

def run() -> None:
    result: None = None
    just_fix_windows_console()
    init()

    fcontent: str = getFile(handleArgv(sys.argv)[0])
    platform: str = checkPlatform(handleArgv(sys.argv)[1])

    tokens: list = lex(fcontent)
    print(tokens)

    return result

if __name__ == "__main__":
    run()