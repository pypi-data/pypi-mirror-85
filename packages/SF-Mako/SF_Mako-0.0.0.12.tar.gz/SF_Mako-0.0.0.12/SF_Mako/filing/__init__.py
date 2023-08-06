from essentials import file_ops
import os, threading, time

os.makedirs("mako_data", exist_ok=True)

class Updating_Dict_File(dict):

    def __init__(self, path):
        self.path = path
        data = __biz_File__(path)
        for item in data:
            self.__setitem__(item, data[item], False)

    def __save_on_change__(self):
        time.sleep(0.5)
        __biz_File__(self.path, self)

    def __setattr__(self, name, value):
        return super().__setattr__(name, value)

    def __setitem__(self, key, value, save=True):
        if save:
            threading.Thread(target=self.__save_on_change__).start()
        return super().__setitem__(key, value)

class Appender_File(dict):

    def __init__(self, path):
        self.path = path
        self.data = __biz_File__(path, append_txt=True)
        
    def append(self, data):
        self.data += data + "\n"
        __biz_File__(self.path, data + "\n", True)


__busy_files__ = {}
def __biz_File__(path, data=None, append_txt=False):
    global __busy_files__
    if path not in __busy_files__:
        __busy_files__[path] = False
    while __busy_files__[path] == True:
        time.sleep(0.01)
    __busy_files__[path] = True
    if data is not None:
        if append_txt:
            file_ops.write_file(path, data, True)
        else:
            file_ops.write_json(path, data)
        __busy_files__[path] = False
        return
    if append_txt:
        try:
            data = file_ops.read_file(path)
        except:
            data = ""
    else:
        try:
            data = file_ops.read_json(path)
        except:
            data = {}
    __busy_files__[path] = False
    return data