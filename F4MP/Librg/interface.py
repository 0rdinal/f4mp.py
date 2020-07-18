import os
import ctypes
from F4MP.Librg.classes import Address

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dll = ctypes.cdll.LoadLibrary(os.path.join(BASE_DIR, "bin/librg.dll"))


class Interface:
    @staticmethod
    def network_start(ctx, address: bytes, port: int):
        address = Address(port, address)
        return bool(dll.librg_network_start(ctx, address))


def dll_func(attr, cast=bool):
    def predicate(*args, **kwargs):
        return cast(dll.__getattr__(attr)(*args, **kwargs))
    return predicate


func_map = {
    "init": ("librg_init",),
    "is_client": ("librg_is_client",),
    "is_connected": ("librg_is_connected",),
    "event_add": ("librg_event_add",),
    "tick": ("librg_tick",),
}
func_map.update(
    {func: getattr(Interface, func) for func in dir(Interface)
     if callable(getattr(Interface, func)) and not func.startswith("__")})

__all__ = tuple(func_map.keys())


def __getattr__(item):
    try:
        res = func_map[item]
    except KeyError:
        return dll.__getattr__(item)
    else:
        if callable(res):
            return res
        else:
            return dll_func(*res)
