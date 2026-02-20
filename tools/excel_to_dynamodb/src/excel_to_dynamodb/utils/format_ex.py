import re

def format_ex(format:str, *args, **kwargs):
    if not isinstance(format, str):
        return format

    if m:= re.fullmatch(pattern=r"\{([^\:}]*)\}", string=format):
        expr:str = m.group(1)
        if expr == "":
            return args[0]
        if re.fullmatch("\d+", expr):
            return args[int(expr)]
        return eval(expr, {}, kwargs)
    else:
        return format.format(*args, **kwargs)


if __name__ == '__main__':

    formats = [
        "{}",
        "{0}",
        "{1}",
        "{aaa}",
        "{bbb}",
        "{bbb.id}",
        "{bbb.name}",
        "{len(bbb.name)}",
        "{aaa}{bbb}",
        "{aaa}/{bbb.id}",
        "{aaa}/{bbb.name}",
        "{aaa} ",
        " {aaa}",
        " {}",
        " {} {}",
        " {1}",
        " {1} {0}",
    ]

    class Dummy():
        def __init__(self):
            self.__setattr__("name", "-DUMMY-")

        @property
        def id(self) -> str:
            return 900000 + 123


    print("***************")
    for fmt in formats:
        ret = format_ex(fmt, "zero", ["one"], aaa="AAA", bbb=Dummy())
        print(fmt.ljust(18) + f"-> {type(ret)} : {ret}")

