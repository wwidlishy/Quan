from colorama import Fore, Back, Style
from src.error import error
import sys

class Lexer:
    def __init__(self) -> None:
        self.tokens = []
        self.current = ""
        self.mode = ""

        self.pos = 0
        self.line = 1
    def lex(self, src: str) -> list:
        self.src = src

        for self.index in range(len(self.src)):
            self.char = self.src[self.index]
            self.pos += 1

            if self.char == "\n":
                self.pos = 0
                self.line += 1
                continue

            if self.mode == "":
                self.num_logic("WhenFirst")
                self.op_logic("WhenFirst")

            if self.mode == "Operator":
                self.op_logic("WhenMode")
                continue
            if self.mode == "Integer":
                self.num_logic("WhenMode")
                continue

        return self.tokens
    
    def num_logic(self, where):
        DIGITS = "1234567890"

        if where == "WhenFirst":
            if self.char in DIGITS:
                self.mode = "Integer"
        if where == "WhenMode":
            if self.char in DIGITS:
                self.current += self.char
            if self.char not in DIGITS or len(self.src) == self.index + 1:
                number = int(self.current)

                self.tokens.append(["Integer", number])
                self.current = ""
                self.mode = ""
    
    def op_logic(self, where):
        CHARS = "+-/*=<>:|&!."
        # : Type Assigment, := is a type of
        OPS = ["+", "++", "+=", "-", "--", "-=", "/", "//", "/=", "*", "**", "*=", "=", "==", "!=", ">=", "<=", ">", "<", ":", ":=", "|", "&", "!", "."]
        if where == "WhenFirst":
            if self.char in CHARS:
                self.mode = "Operator"
        if where == "WhenMode":
            if self.char in CHARS:
                self.current += self.char
            if self.char not in CHARS or len(self.src) == self.index + 1:
                operator = self.current if self.current in OPS else error(\
f"""{Fore.RED}Line: {self.line}, Position: {self.pos-len(self.current)} :: [Error: Invalid Operator!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
'{self.current}' is an Invalid Operator.""", sys.exit)

                self.tokens.append(["Operator", operator])
                self.current = ""
                self.mode = ""
def lex(src: str) -> list:
    lexer = Lexer()
    tokens = lexer.lex(src)

    return tokens