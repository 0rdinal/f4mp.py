import ctypes
import glm
from F4MP import Librg, Handler
from F4MP.classes import User, Connection, Status, Attributes


class Server:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        self.ctx = ctypes.POINTER(Librg.Context)(Librg.Context())
        Librg.init(self.ctx)
        self.task_queue = []
        self.call_map = {}
        self.callback_hander = Handler.CallbackHandler(self)

        self.call_map["on_connection_request"].add(self._on_connection_request)

        self.users = {}

    def listener(self, name=None):
        def decorator(func):
            self.call_map[name or func.__name__].add(func)
            return func

        return decorator

    def is_client(self):
        return Librg.is_client(self.ctx)

    def is_connected(self):
        return Librg.is_connected(self.ctx)

    def start(self):
        Librg.network_start(self.ctx, self.address.encode(), self.port)

    def tick(self):
        Librg.tick(self.ctx)

    def run(self):
        self.start()
        while True:
            for task in self.task_queue:
                for func in self.call_map[task.type]:
                    func(task.event)
                self.task_queue.remove(task)
            self.tick()

    def _write(self, data, type, value):
        if type == 'str':
            Librg.data_write(data, 'u32', len(value))
            for ch in value:
                Librg.data_write(data, 'i8', ord(ch))
        else:
            Librg.data_write(data, type, value)

    def _read(self, data, type):
        offset = type.find('_arr_')
        if offset >= 0:
            result = []
            for _ in range(int(type[offset + 5:])):
                result.append(self._read(data, type[:offset]))
            return result

        if type == 'str':
            length = Librg.data_read(data, 'u32')
            return ''.join([chr(Librg.data_read(data, 'i8')) for _ in range(length)])

        return Librg.data_read(data, type)

    def _on_connection_request(self, event):
        name = self._read(event.contents.data, 'str')
        position = self._read(event.contents.data, 'f32_arr_3')
        special = self._read(event.contents.data, 'i32_arr_7')
        status = self._read(event.contents.data, 'f32_arr_4')

        self.users[event.contents.entity.contents.id] = User(event.contents.entity.contents.id, name, glm.vec3(*position), Connection(""), Status(*status), Attributes(*special), [])

        print(self.users)
