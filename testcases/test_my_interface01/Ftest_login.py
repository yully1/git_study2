"""
----------------------------------------------------
@Time  :  2022/2/25 20:28
@Author  :  shina
@File  :  test_login04.PY
----------------------------------------------------
"""
"""
feature：特征
@allure.feature ：用于allure 的模块分层
@allure.story ： 用于allure 的子模块分层，即上面模块的子层
@allure.title ：为case静态修改名字，它会被动态修改名字覆盖
@allure.severity('critical') 为allure修改case的优先等级：
    blocker　 阻塞缺陷（功能未实现，无法下一步）
    critical　　严重缺陷（功能点缺失） 核心主流程
    normal　　 一般缺陷（边界情况，格式错误）
    minor　 次要缺陷（界面错误与ui需求不符）
    trivial　　 轻微缺陷（必须项无提示，或者提示不规范）
allure.dynamic.feature  动态获取每个case的名字，需要放在获取case/函数里面
allure.attach ：输出内容 ,显示详细的测试步骤,里面必须有参数，body=body, name=name
"""
# 主流程(1、先创建类和case框架，2、读取excel文件数据并参数化
# #3、使用requests请求模拟接口工具并断言结果  4、使用try如果错误写入excel表格和日期，抛出错误日志的堆栈回溯和异常，如果成功也写出报个和info日志)
# 数据回滚再请求数据前和验证再请求断言后  其他case和allure报告

import pytest
import requests
from comms.excel_utils import ReadExcel
import allure
from comms.log_utils import logger
from comms.constants import DATA_FILE
from comms.db_utils import DBUtils


@allure.feature('登录的模块')  # 用于allure 的模块分层
class TestLogin:  # 类要以Test开头
    @pytest.fixture(autouse=True)  # 增加数据库操作的夹具
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, "user_login")  # 读取excel的user_login的sheet页的所有测试用例对象返回列表

    @allure.severity('critical')  # 为allure报告修改case优先级
    @allure.description('京东小程序入口登录接口')  # 为allure报告增加case描述
    @pytest.mark.parametrize('case', cases)  # 把返回的列表中的成员赋值给case，每赋值一次就执行一次case
    def test_login(self, case):  # 接受case测试用例的对象参数

        allure.dynamic.title(case.case_title)  # 动态获取allure报告的case标题
        allure.attach(body=case.url, name='接口路径')  # 在allure报告的测试步骤显示接口路径
        allure.attach(body=case.case_data, name='接口参数')  # 在allure报告的测试步骤显示接口参数

        # 正确流程 如果里面有数据，先删除，再插入一条需要登录的正确数据，叫数据回滚，为了确保数据库或表格里永远有我们需要的登录数据
        if case.case_id == 1:
            uname = eval(case.case_data)['username']
            pwd = eval(case.case_data)['password']

            self.db.cud('DELETE FROM tb_user WHERE name = %s;', (uname,))  # 删除数据
            self.cud('INSERT INTO tb_user(name,passwd,email,phone) VALUES(%s,%s,%s,%s);',  # 插入数据
                     (uname, pwd, 'test@163.com', '18656034444'))

        response = requests.post(url=case.url, data=eval(case.case_data))  # 大气post请求，url和请求体时对象的2个实例属性
        res = response.json()  # 把响应体转换为json格式
        allure.attach(body=str(res), name='响应结果')  # allure报告显示响应结果

        try:
            assert eval(case.expect) == res  # 断言测试用例的预期结果和实际结果是否一致
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, "user_login", case.case_id, 7, '失败')  # 如果失败把断言失败把结果写入excel
            logger.error('测试编号{}，测试用例标题{}，执行失败，实际结果是{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            logger.info('测试编号{}，测试用例标题{}，执行成功，'.format(case.case_id, case.case_title))
            ReadExcel.write_data(DATA_FILE, "user_login", case.case_id, 7, '成功')  # 如果实际结果符合预期把成功写入excel
