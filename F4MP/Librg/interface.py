import os
import ctypes
from F4MP.Librg.classes import Address

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dll = ctypes.cdll.LoadLibrary(os.path.join(BASE_DIR, "bin/librg.dll"))


def init(ctx):
    dll.librg_init(ctx)


def is_client(ctx):
    return bool(dll.librg_is_client(ctx))


def is_connected(ctx):
    return bool(dll.librg_is_connected(ctx))


def event_add(ctx, event_id, callback):
    if not dll.librg_event_add(ctx, event_id, callback):
        raise


def network_start(ctx, address: bytes, port: int):
    address = Address(port, address)

    ret = dll.librg_network_start(ctx, address)


def tick(ctx):
    dll.librg_tick(ctx)
