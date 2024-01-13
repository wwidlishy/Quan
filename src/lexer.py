from colorama import Fore, Back, Style
from src.error import error
import sys

def lexerMainLoop(src: str, index: int, loc=[[], "", "", 1, 1, 0, "", ""]) -> int: # tokens, mode, current, pos, line, val1
    result = index + 1
    
    tokens = loc[0]
    mode = loc[1]
    current = loc[2]
    pos = loc[3]
    line = loc[4]
    val1 = loc[5]
    mode2 = loc[6]
    current2 = loc[7]

    if len(src) - result >= 1:
        char = src[result]
    else:
        return tokens
    
    if char == "\n" and mode2 != "":
        if mode not in ["", "comment", "number"]:
            error(\
f"""{Fore.RED}[Error({line}:{pos}): Data Structure EOL Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
A {mode} token was not ended.""", sys.exit)
        return lexerMainLoop(src, result, [tokens, "", "", 1, line+1, val1, "", ""])
    
    if mode in ["", "parentheses"] and mode2 == "":
        if char == "(" and mode != "parentheses":
            return lexerMainLoop(src, result, [tokens, "parentheses", [], pos, line, 1, mode2, current2])
        if char == ")" and mode != "parentheses":
            error(\
f"""{Fore.RED}[Error({line}:{pos}): Parentheses Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
')' was unexpected.""", sys.exit)
        
        if char in "1234567890":
            mode2 = "number"
            current2 = ""
            return lexerMainLoop(src, result-1, [tokens, mode, current, pos, line, val1, mode2, current2])

    if mode2 == "number":
        if char in ".0123456789":
            current2 += char
            if len(src) - result == 1:
                try: number = eval(current2)
                except: error(\
    f"""{Fore.RED}[Error({line}:{pos}): Invalid Number Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
    '{current2}' is an invalid number token.""", sys.exit)
                return tokens+[[mode2, number]]
            return lexerMainLoop(src, result, [tokens, mode, current, pos+1, line, val1, mode2, current2])
        else:
            try: number = eval(current2)
            except: error(\
f"""{Fore.RED}[Error({line}:{pos}): Invalid Number Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
'{current2}' is an invalid number token.""", sys.exit)
            if mode != "parentheses":
                return lexerMainLoop(src, result-1, [tokens+[[mode2, number]], mode, current, pos, line, val1, "", ""])
            else:
                return lexerMainLoop(src, result-1, [tokens, mode, current+[[mode2, number]], pos, line, val1, "", ""])
    if mode == "parentheses":
        if char == "(":
            val1 += 1
        if char == ")":
            val1 -= 1
        
        if val1 == 0:
            return lexerMainLoop(src, result, [tokens+[[mode, current]], "", "", pos, line, 0, mode2, current2])

        if len(src) - result == 0:
            error(\
f"""{Fore.RED}[Error({line}:{pos}): Parentheses Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
')' was expected.""", sys.exit)
        return lexerMainLoop(src, result, [tokens, mode, current, pos+1, line, val1, mode2, current2])
    
    return lexerMainLoop(src, result, [tokens, mode, current, pos+1, line, val1, mode2, current2])

def lex(src: str) -> list:
    return lexerMainLoop(src, -1)

# Todo!: keywords, ids, brackets, curly brackets, operators
#!!! Make this into a class or use a fucking loop, fp in python sucks