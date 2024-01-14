from colorama import Fore, Back, Style
from src.error import error
import sys

class _global:
    tokens = []
    mode = []
    current = {}

    line = 1
    pos = 0
    char = ""

def lexerMakeNumber(number: str) -> int:
    try: result = int(number)
    except: error(\
f"""{Fore.RED}[Error: Invalid Integer Literal!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
'{number}' is not a valid Integer literal.""", sys.exit)
        
    return result

def lexerMainLoop(src: str, index: int) -> int: # tokens, mode, current, pos, line, val1
    if len(src) - index != 1:
        CURRENT_INDEX = index + 1
        _global.char = src[CURRENT_INDEX]

        _global.pos += 1
        _global.line += (1 if _global.char == "\n" else 0)

        if _global.mode == []:
            if _global.char in "1234567890":
                _global.mode.append("Integer")
                _global.current["Integer"] = f"{_global.char}"
                return lexerMainLoop(src, CURRENT_INDEX)
        elif "Integer" in _global.mode:
            if _global.char in "1234567890":
                _global.current["Integer"] += f"{_global.char}"
                return lexerMainLoop(src, CURRENT_INDEX)
            else:
                number = lexerMakeNumber(_global.current["Integer"])
                if "Tuple" not in _global.mode: _global.tokens.append(["Integer", number])
                else: _global.current["Tuple"].append(["Integer", number])

                _global.current["Integer"] = ""
                return lexerMainLoop(src, CURRENT_INDEX)
        return lexerMainLoop(src, CURRENT_INDEX)
    
    return _global.tokens

def lex(src: str) -> list:
    return lexerMainLoop(src, -1)

# Todo!: keywords, id's, brackets, curly brackets, tuples, operators