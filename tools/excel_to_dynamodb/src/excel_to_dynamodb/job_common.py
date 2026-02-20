from typing import Any
import importlib



def import_config_module(config_name:str):
        # module.function を読み込み
    config_mod = importlib.import_module(config_name) 
    return config_mod


def import_config_attr(config_name:str, attr_name:str):
        # module.function を読み込み
    config_mod = import_config_module(config_name=config_name)
    config_attr:Any = getattr(config_mod, attr_name)
    return config_attr

