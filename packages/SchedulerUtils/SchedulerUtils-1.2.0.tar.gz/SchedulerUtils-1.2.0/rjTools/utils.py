import json
from json import JSONDecodeError


def file2dict(path):
    # 读取配置文件
    with open(path) as f:
        try:
            rst = json.load(f)
        except JSONDecodeError as e:
            print(e.args)
            return None
        return rst


# 创建文件方法：
def create_file(filename):
    """
    创建日志文件夹和日志文件
    :param filename:
    :return:
    """
    path = filename[0:filename.rfind("/")]
    import os
    if not os.path.isdir(path):  # 无文件夹时创建
        os.makedirs(path)
    if not os.path.isfile(filename):  # 无文件时创建
        fd = open(filename, mode="w", encoding="utf-8")
        fd.close()
    else:
        pass
