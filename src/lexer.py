from colorama import Fore, Back, Style
from src.error import error
import sys

def lexerMainLoop(src: str, index: int, loc=[[], "", "", 1, 1]) -> int: # tokens, mode, current, pos, line
    result = index + 1

    if len(src) - result >= 1:
        char = src[result]
    else:
        return -1
    
    tokens = loc[0]
    mode = loc[1]
    current = loc[2]
    pos = loc[3]
    line = loc[4]

    if char == "\n":
        return lexerMainLoop(src, result, [tokens, "", "", 1, line+1])
    elif char.isspace():
        return lexerMainLoop(src, result, [tokens, mode, current, pos+1, line])
    
    if mode == "":
        if char == "(":
            return lexerMainLoop(src, result, [tokens, "parentheses", "", pos+1, line])
        if char == ")":
            error(\
f"""{Fore.RED}[Error({line}:{pos}): Parentheses Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
')' was unexpected.""", sys.exit)
    return lexerMainLoop(src, result, [tokens, mode, current, pos+1, line])

def lex(src: str) -> list:
    lexerMainLoop(src, -1)