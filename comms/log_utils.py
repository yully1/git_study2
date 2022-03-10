"""
----------------------------------------------------
@Time  :  2022/2/28 16:33
@Author  :  shina
@File  :  log_utils.PY
----------------------------------------------------
"""
import logging
from comms.constants import INFO_FILE, ERROR_FILE


def get_logger():
    # 第二步：创建日志对象
    logger = logging.getLogger()
    logger.setLevel('DEBUG')  # 给对象分级别，级别是DEBUG及DEBUG以上的内容

    # 第三步：设置输出方法：方向可以有很多种：比如控制台，文件，邮件等
    # 1、日志输出到控制台方向，定义级别为DEBUG和DEBUG以上级别的内容
    sh1 = logging.StreamHandler()
    sh1.setLevel('DEBUG')

    # 2、日志输出文件方向，里面要加文件名，内容追加的方式：读：r 追加写入：a  覆盖写入：W,定义级别是INFO及以上内容
    sh2 = logging.FileHandler(filename=INFO_FILE, mode='a', encoding='utf-8')
    sh2.setLevel('INFO')  # 级别是INFO级别即以上的内容

    # 3、输出。./error.log 文件，并且追加内容写入，级别是error级别及以上的内容
    sh3 = logging.FileHandler(filename=ERROR_FILE, mode='a', encoding='utf-8')
    sh3.setLevel('ERROR')

    # 增加输出方向到logger对象里

    logger.addHandler(sh1)
    logger.addHandler(sh2)
    logger.addHandler(sh3)

    # 指定日志的输出格式
    # formatter，定义了最终log信息的顺序,结构和内容
    # %(asctime)s 时间
    # %(filename)s 调用日志输出函数的模块的文件名
    # %(lineno)d 调用日志输出函数的语句所在的代码行
    # %(levelno)s 日志级别
    # %(message)s 输出的消息内容
    fmt_str = '%(asctime)s - [%(filename)s - %(lineno)d] - %(levelno)s:%(message)s'
    my_fmt = logging.Formatter(fmt_str)  # 创建实例对象，设置输出日志的格式，把自己定义的格式传进去
    sh1.setFormatter(my_fmt)
    sh2.setFormatter(my_fmt)
    sh3.setFormatter(my_fmt)
    return logger


logger = get_logger()
