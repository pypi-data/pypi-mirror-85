import os
import pandas as pd
from spongebox.rebox import filter_list
import spongebox.timebox as timebox
import logging

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option("display.unicode.east_asian_width", True)
pd.set_option("display.float_format", lambda x: "%.4f" % x)


class log:
    def __init__(self, output="console", log_file_path=None, mode="a", level=logging.DEBUG,
                 formatter=logging.Formatter(
                     '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')):

        self.output = output
        self.log_file_path = log_file_path
        self.mode = mode
        self.level = level
        self.formatter = formatter

        # 创建一个logger
        self.logger = logging.getLogger('spongelogger{}'.format(timebox.stamp()))
        self.logger.setLevel(self.level)

        # 添加handler
        if self.output == "console":
            self._add_handler(logging.StreamHandler())
        elif self.output == "file":
            self._add_handler(logging.FileHandler(self.log_file_path, mode=self.mode))
        elif self.output == "both":
            self._add_handler(logging.StreamHandler())
            self._add_handler(logging.FileHandler(self.log_file_path))

    def _add_handler(self, logging_handler):
        logging_handler.setLevel(self.level)
        logging_handler.setFormatter(self.formatter)
        self.logger.addHandler(logging_handler)


def list_dir(dir_path, exp=None):
    if exp is None:
        return os.listdir(dir_path)
    else:
        return filter_list(os.listdir(dir_path), exp=exp)

def read_overwrite(path,text_process_func,encoding="utf-8"):
    with open(path,"r+",encoding=encoding) as f:
        content = text_process_func(f.read())
        f.seek(0)
        f.truncate()
        f.write(content)


@timebox.timeit
def list_all_files(dir_path):
    lst = []
    for root, dir, flst in os.walk(dir_path):
        # print(root)
        # print(dir)
        # print(flst)
        lst.extend([root + "\\" + f for f in flst])
    return lst


if __name__ == "__main__":
	mylog = log()
	mylog.logger.debug("haha")
    # print(list_dir("../", exp=".*md$"))
    # lst = []
    # lst1=[]
    # print(list_all_files("C:\\Users\\LuoJi\\Downloads\\test",lst))
    # print(list_all_files("C:\\Users\\LuoJi\\Downloads\\test",lst1))
    # print(walk_all_files("C:\\Users\\LuoJi\\Downloads\\test"))
    # list_all_files("C:\\Users\\LuoJi\\Documents\\05照片")
    # print(list_all_files("C:\\Users\\LuoJi\\Downloads\\test"))

