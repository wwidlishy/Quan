from colorama import Fore, Back, Style
from src.error import error
import sys

# this class encapsulates parentheses, and splits into statements
class StatementOrganize:
    def __init__(self) -> None:
        pass
    def splitlines(self, tokens: list) -> list:
        result: list = []
        current: list = []

        for tok in tokens:
            if tok == "EOS":
                result.append(current)
                current = []
            elif isinstance(tok, list) and tok[0] == "Block":
                current.append([tok[0], StatementOrganize().splitlines(tok[1])])
            else:
                current.append(tok)

        return result
    def encapsulate(self, tokens: list) -> list:
        mode: str = ""
        result: list = []
        current: list = []
        num: int = 0

        if  tokens.count("LPAREN") == tokens.count("RPAREN")\
        and tokens.count("OPENLIST") == tokens.count("CLOSELIST")\
        and tokens.count("OPENBLOCK") == tokens.count("OPENBLOCK"):
            pass
        else:
            error(\
f"""{Fore.RED}[Error: Enclosment Missmatch Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
Enclosure count missmatch: please check if all parentheses / lists / blocks are properly enclosed.""", sys.exit)

        for tok in tokens:
            if mode == "":
                if tok == "LPAREN":
                    mode = "Tuple"
                    current = []
                    num = 1
                    continue
                elif tok == "RPAREN": error(\
f"""{Fore.RED}[Error: Enclosment Missmatch Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
Enclosure count missmatch: please check if all parentheses are properly enclosed.""", sys.exit)
                elif tok == "OPENLIST":
                    mode = "List"
                    current = []
                    num = 1
                    continue
                elif tok == "CLOSELIST": error(\
f"""{Fore.RED}[Error: Enclosment Missmatch Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
Enclosure count missmatch: please check if all lists are properly enclosed.""", sys.exit)
                elif tok == "OPENBLOCK":
                    mode = "Block"
                    current = []
                    num = 1
                    continue
                elif tok == "CLOSEBLOCK": error(\
f"""{Fore.RED}[Error: Enclosment Missmatch Error!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
Enclosure count missmatch: please check if all parentheses / lists / blocks are properly enclosed.""", sys.exit)
                else:
                    result.append(tok)
            if mode == "Tuple":
                if tok == "LPAREN":
                    num += 1
                    current.append(tok)
                elif tok == "RPAREN":
                    num -= 1
                    if num != 0: current.append(tok)
                else:
                    current.append(tok)
                
                if num == 0:
                    val = StatementOrganize().encapsulate(current)
                    result.append([mode, val])
                    mode = ""
                    current = []
                    continue
            if mode == "List":
                if tok == "OPENLIST":
                    num += 1
                    current.append(tok)
                elif tok == "CLOSELIST":
                    num -= 1
                    if num != 0: current.append(tok)
                else:
                    current.append(tok)
                
                if num == 0:
                    val = StatementOrganize().encapsulate(current)
                    result.append([mode, val])
                    mode = ""
                    current = []
                    continue
            if mode == "Block":
                if tok == "OPENBLOCK":
                    num += 1
                    current.append(tok)
                elif tok == "CLOSEBLOCK":
                    num -= 1
                    if num != 0: current.append(tok)
                else:
                    current.append(tok)
                
                if num == 0:
                    val = StatementOrganize().encapsulate(current)
                    result.append([mode, val])
                    mode = ""
                    current = []
                    continue
        return result
def ast(tokens: list) -> list:
    SO = StatementOrganize()
    result: list = SO.splitlines(SO.encapsulate(tokens))
    return result