from typing import Optional
import shlex

code: Optional[str] = None
with open("code.asmb") as file:
    code = file.read()


output = ""


for line in code.split("\n"):
    # print(line)
    # print(shlex.split(line))
    args = shlex.split(line)

    if len(args) == 0:
        continue
    cmd = args.pop(0)
    # print(args)
    # print(cmd)

    match cmd:
        case "add":
            output += "+" * int(args[0] if len(args) > 0 else 1)
        case "sub":
            output += "-" * int(args[0] if len(args) > 0 else 1)
        case "set":
            output += "[-]"
            output += "+" * int(args[0] if len(args) > 0 else 0)
        case "set_char":
            output += "[-]"
            output += "+" * ord(args[0])
        case "move_right":
            output += ">" * int(args[0] if len(args) > 0 else 1)
        case "move_left":
            output += "<" * int(args[0] if len(args) > 0 else 1)
        case "print":
            output += "."
        case "input":
            output += ","
        case _:
            pass


with open("output.bf", "w") as file:
    file.write(output)
