###########
#     Imports     #
###########

import sys
import os

from colorama import init, Fore, Back, Style
from colorama import just_fix_windows_console

from src.lexer import lex
from src.error import error
from src._ast import ast

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
    try:
        result = __import__(f"builders.{platform}")
    except:
        nl = "\n"
        error(\
f"""{Fore.RED}[Error: Builder Not Found!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
'{platform}' is an Invalid Builder.

--- Valid Builders ---
{nl.join([i[::-1][3:][::-1] for i in os.listdir("builders/")])}""", sys.exit)

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

def printAst(ast: list, indent="") -> None:
    for line in ast:
        for token in line:
            if isinstance(token, list):
                print(f"{indent}{token[0]}")
                if isinstance(token[1], list):
                    printAst(token[1], f"{indent}\t")
                else:
                    print(f"{indent}\t{token[1]}")
            else:
                print(f"{indent}{token}")
        print()

def run() -> None:
    result: None = None
    just_fix_windows_console()
    init()

    fcontent: str = getFile(handleArgv(sys.argv)[0])
    platform: str = checkPlatform(handleArgv(sys.argv)[1])

    if fcontent.strip() == "": return

    tokens: list = lex(fcontent)
    _ast: list   = ast(tokens)

    printAst(_ast)
    return result

if __name__ == "__main__":
    run()