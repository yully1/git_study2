"""
----------------------------------------------------
@Time  :  2022/2/25 11:46
@Author  :  shina
@File  :  test_runner.py.PY
----------------------------------------------------
"""
"""
使用allure生产测试报告
    1、官网下载地址：https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/，官网下载一个版本选择压缩包.zip
    2、解压到tools目录下，如：D:\Tools\allure-2.17.0
    3、增加allure到bin目录下到环境变量path中
    4、在cmd命令中输入allure回车，验证是否安装成功
    5、在cmd命令输入pip insatll allure-pytest 安装pytest框架的allure插件
    generate ：生产
    -o : 输出
    --clean:清除

"""
import pytest, os
from comms.constants import REPORT_JSON, REPORT_HTML, CASE_DIR

if __name__ == '__main__':
    pytest.main(["-vs", "--tb=line", '--alluredir', REPORT_JSON, CASE_DIR])
    os.system('allure generate %s -o %s --clean' % (REPORT_JSON, REPORT_HTML))
