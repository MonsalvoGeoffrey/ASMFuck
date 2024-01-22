from typing import Optional, List
import shlex

code: Optional[str] = None
with open("code.asmb") as file:
    code = file.read()


class Token:
    def collapse(self):
        pass


output: str = ""
block_stack: List[Token] = []
heap = []
tokens: List[Token] = []


class Raw(Token):
    def __init__(self, code: str):
        self.code: str = code

    def collapse(self):
        return self.code


class Function(Token):
    def __init__(self, name: str):
        self.name: str = name
        self.tokens: List[Token] = []

    def append(self, token: Token):
        self.tokens.append(token)

    def collapse(self):
        # return ""
        res = ""
        for token in self.tokens:
            res += token.collapse()
        return res


class Until(Token):
    def __init__(self, target):
        self.target = target
        self.tokens: List[Token] = []

    def append(self, token: Token):
        self.tokens.append(token)

    def collapse(self):
        code = ""
        for token in self.tokens:
            code += token.collapse()
        return (
            ("-" * self.target)
            + "["
            + ("+" * self.target)
            + (code)
            + ("-" * self.target)
            + "]"
            + ("+" * self.target)
        )


class Unless(Token):
    def __init__(self, target):
        self.target = target
        self.tokens: List[Token] = []

    def append(self, token: Token):
        self.tokens.append(token)

    def collapse(self):
        code = ""
        for token in self.tokens:
            code += token.collapse()
        return (
            ("-" * self.target)
            + "["
            # + ("+" * self.target)
            + (code)
            # + ("-" * self.target)
            + "]"
            + ("+" * self.target)
        )


functions: List[Function] = []


def parse_line(line):
    global tokens
    global block_stack
    global functions
    # print(line)
    # print(shlex.split(line))
    args = shlex.split(line)

    if len(args) == 0:
        return
    cmd = args.pop(0)
    # print(args)
    # print(cmd)

    block = tokens
    if len(block_stack) > 0:
        block = block_stack[len(block_stack) - 1]

    match cmd:
        case "add":
            block.append(Raw("+" * int(args[0] if len(args) > 0 else 1)))
        case "sub":
            block.append(Raw("-" * int(args[0] if len(args) > 0 else 1)))
        case "set":
            block.append(Raw("[-]"))
            block.append(Raw("+" * int(args[0] if len(args) > 0 else 0)))
        case "set_char":
            block.append(Raw("[-]"))
            block.append(Raw("+" * ord(args[0])))
        case "move_right":
            block.append(Raw(">" * int(args[0] if len(args) > 0 else 1)))
        case "move_left":
            block.append(Raw("<" * int(args[0] if len(args) > 0 else 1)))
        case "print":
            block.append(Raw("."))
        case "input":
            block.append(Raw(","))
        case "function":
            block_stack.append(Function(args[0]))
        case "until":
            block_stack.append(Until(int(args[0])))
        case "unless":
            block_stack.append(Unless(int(args[0])))
        case "end":
            current_block = block_stack.pop()
            block = tokens
            if len(block_stack) > 0:
                block = block_stack[len(block_stack) - 1]
            if isinstance(current_block, Function):
                functions.append(current_block)
            else:
                block.append(current_block)
        case "call":
            for func in functions:
                if func.name == args[0]:
                    block.append(Raw(func.collapse()))
                    break
        case _:
            pass


def collapse():
    global output
    for token in tokens:
        output += token.collapse() + "\n"


for line in code.split("\n"):
    parse_line(line)


collapse()
print(output)

with open("output.bf", "w") as file:
    file.write(output)
