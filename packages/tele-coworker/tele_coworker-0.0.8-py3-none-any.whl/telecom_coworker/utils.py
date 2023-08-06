import multiprocessing as mp
import socket
import traceback
from collections import defaultdict
from threading import Timer


def set_interval(func, interval=5, *args, **kwargs):
    def wrap_func():
        func(*args, **kwargs)
        Timer(interval, wrap_func).start()

    Timer(interval, wrap_func).start()


def search_dict_by_keys(source: dict, values):
    result = defaultdict(set)
    for k, vs in source.items():
        for v in vs:
            if v in values:
                result[k].add(v)
    return result


def get_hostname():
    try:
        name = socket.gethostname()
    except:
        name = 'Unknown'

    return name


def get_hostip():
    """依赖于/etc/hosts中本机hostname ip配置"""
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = '127.0.0.1'
    return ip


class Process(mp.Process):
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = mp.Pipe()
        self._exception = None

    def run(self):
        try:
            mp.Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))
            # raise e  # You can still rise this exception if you need to

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception


if __name__ == '__main__':
    def foo(*args, **kwargs):
        print(f"args: {args}, kwargs: {kwargs}")


    set_interval(foo, 1, 2, a='hello', b='world')

# if __name__ == '__main__':
#     d = defaultdict(set)
#     d['foo'].add('bar')
#     d['foo'].add('bar2')
#     d['bar'] = set()
#
#     result = search_dict_by_keys(d, ['bar'])
#     print(result)
#
#     print(f'hostname: {get_hostname()}')
#     print(f'host ip: {get_hostip()}')
