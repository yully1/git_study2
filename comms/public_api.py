"""
--------------------------------
@Time    :  2022/3/2 - 9:46
@Author  :  chen
@File    :  public_api
--------------------------------
"""
from configparser import ConfigParser
from comms.constants import CONF_FILE
import requests


# 从ini文件读取数据
def get_ini_data(section, option):
    try:
        cnp = ConfigParser()  # 填写核心代码
        cnp.read(CONF_FILE, encoding='utf-8')
        return cnp.get(section, option)
    except Exception as e:
        print('从ini文件读取测试数据失败!', e)


# 数据替换
def replace_data(my_dict, key, value):
    """
    :param my_dict: 需要替换的字符串类型的字典
    :param key: 需要替换的key
    :param value: 替换的数据
    :return: 替换后的字符串类型的字典
    """
    try:
        dict1 = eval(my_dict)  # 先转换字符串为字典类型
        dict1[key] = value
        return str(dict1)
    except Exception as e:  # 如果出现异常，就执行except下的代码
        print('替换数据失败！！')
        print(e)


if __name__ == '__main__':
    print(get_ini_data('mysql', 'host'))
    print(replace_data('{"name":"xiaohua"}', 'name', '小牛'))


def get_token():
    try:
        response = requests.post(url="http://127.0.0.1:6666/business/token_login", data=
        {'username': get_ini_data("users1", "username"),
         'password': get_ini_data("users1", "password"),
         'typeId': '101'})
        res = response.json()
        return res["token"]
    except Exception as e:
        print("获取token值失败", e)


print(get_token())
