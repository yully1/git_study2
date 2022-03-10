"""
--------------------------------
@Time  :  2022/1/24 - 20:08 
@Author  :  shina
@File  :  constants 常量
--------------------------------
"""
"""
使用常量对路径进行管理
好处: 代码使用非绝对路径,可移植性高
"""
import os

# 获取项目路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # 获取当前文件的父目录
# print(BASE_DIR)  # D:/PythonWorkSpace/autotest

# 测试用例文件所在的路径
CASE_DIR = os.path.join(BASE_DIR, 'testcases')
print(CASE_DIR)

# 测试数据所在的路径
DATA_DIR = os.path.join(BASE_DIR, 'datas')
DATA_FILE = os.path.join(DATA_DIR, 'cases.xlsx')
# print(DATA_FILE)  # D:/PythonWorkSpace/autotest\cases.xlsx

# log路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')  # D:/PythonWorkSpace/autotest\logs
INFO_FILE = os.path.join(LOG_DIR, 'info.log')
ERROR_FILE = os.path.join(LOG_DIR, 'error.log')
# print(LOG_DIR)

# 获取配置文件所在路径
CONF_DIR = os.path.join(BASE_DIR, 'conf')
CONF_FILE = os.path.join(CONF_DIR, 'config.ini')
# print(CONF_DIR)

# 获取测试报告所在路径

REPORT_DIR = os.path.join(BASE_DIR, 'report')
REPORT_JSON = os.path.join(REPORT_DIR, 'allure_json')
REPORT_HTML = os.path.join(REPORT_DIR, 'allure_html')
# print(REPORT_DIR)
