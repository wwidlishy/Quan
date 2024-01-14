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
        self.index = -1

        while self.index in range(len(self.src))[:len(self.src)-1] or self.index == -1:
            self.index += 1
            self.char = self.src[self.index]
            self.pos += 1

            if self.char == "\n":
                self.pos = 0
                self.line += 1

            if self.mode == "":
                if self.char == ";":
                    self.tokens.append("EOS")
                if self.char == "(":
                    self.tokens.append("LPAREN")
                if self.char == ")":
                    self.tokens.append("RPAREN")
                if self.char == "[":
                    self.tokens.append("OPENLIST")
                if self.char == "]":
                    self.tokens.append("CLOSELIST")
                if self.char == "{":
                    self.tokens.append("OPENBLOCK")
                if self.char == "}":
                    self.tokens.append("CLOSEBLOCK")

                self.num_logic("WhenFirst")
                self.op_logic("WhenFirst")
                self.keyword_logic("WhenFirst")
            if self.mode == "Id":
                self.keyword_logic("WhenMode")
                continue
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
            if self.char in DIGITS and self.char != "\n":
                self.current += self.char
            if ((self.char not in DIGITS) or (len(self.src) == self.index + 1)) or self.char == "\n":
                number = int(self.current)

                self.tokens.append(["Integer", number])
                self.current = ""
                self.mode = ""
                self.index -= 1

    def keyword_logic(self, where):
        QWERTY = "qwertyuiopasdfghjklzxcvbnm_QWERTYUIOPASDFGHJKLZXCVBNM"
        QWERTY_NUMS = QWERTY + "1234567890"
        if where == "WhenFirst":
            if self.char in QWERTY:
                self.mode = "Id"
        if where == "WhenMode":
            if self.char in QWERTY_NUMS and self.char != "\n":
                self.current += self.char
            if ((self.char not in QWERTY_NUMS) or (len(self.src) == self.index + 1)) or self.char == "\n":
                self.tokens.append(["Id", self.current])
                self.current = ""
                self.mode = ""
                self.index -= 1

    def op_logic(self, where):
        CHARS = "+-/*=<>:|&!.,"
        # : Type Assigment, := is a type of
        OPS = ["+", "++", "+=", "-", "--", "-=", "/", "/=", "*", "**", "*=", "=", "==", "!=", ">=", "<=", ">", "<", ":", ":=", "|", "&", "!", ".", ","]
        if where == "WhenFirst":
            if self.char in CHARS:
                self.mode = "Operator"
        if where == "WhenMode":
            if self.char in CHARS and self.char != "\n":
                self.current += self.char
            if ((self.char not in CHARS) or (len(self.src) == self.index + 1)) or self.char == "\n":
                operator = self.current if self.current in OPS else error(\
f"""{Fore.RED}Line: {self.line}, Position: {self.pos-len(self.current)} :: [Error: Invalid Operator!]{Style.RESET_ALL}    {Back.RED}[COMPILATION TERMINATED: -1]{Style.RESET_ALL}
'{self.current}' is an Invalid Operator.""", sys.exit)

                self.tokens.append(["Operator", operator])
                self.current = ""
                self.mode = ""
                self.index -= 1

def lex(src: str) -> list:
    lexer = Lexer()
    tokens = lexer.lex(src)

    return tokens