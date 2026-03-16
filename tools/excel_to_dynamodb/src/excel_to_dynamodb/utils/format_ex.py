import re
from typing import Union, List, Dict

def format_ex(format:Union[str, List, Dict], *args, **kwargs):

    if isinstance(format, str):
        if m:= re.fullmatch(pattern=r"\{([^\:}]*)\}", string=format):
            expr:str = m.group(1)
            if expr == "":
                return args[0]
            if re.fullmatch("\d+", expr):
                return args[int(expr)]
            return eval(expr, {}, kwargs)
        else:
            return format.format(*args, **kwargs)
    elif isinstance(format, list):
        return [ format_ex(v, *args, **kwargs) for v in format ]
    elif isinstance(format, dict):
        return { k:format_ex(v, *args, **kwargs) for k,v in format.items() }
    else:
        return format


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
        [" {1} {0}", "{aaa}/{bbb.name}"],
        {"AAA:": " {1} {0}", "BBB": "{aaa}/{bbb.name}"},
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
        print(str(fmt).ljust(30) + f"-> {type(ret)} : {ret}")

