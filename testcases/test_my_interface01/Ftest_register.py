"""
----------------------------------------------------
@Time  :  2022/2/25 20:29
@Author  :  shina
@File  :  test_register05.PY
----------------------------------------------------
"""
import pytest
import requests
from comms.excel_utils import ReadExcel
import allure
from comms.log_utils import logger
from comms.constants import DATA_FILE
from comms.db_utils import DBUtils


@allure.feature('注册的模块')
class TestRegister:
    @pytest.fixture(autouse=True)  # 为case增加夹具
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, "user_register")

    @allure.severity('critical')
    @allure.description('京东小程序入口注册接口')
    @pytest.mark.parametrize('case', cases)
    def test_register(self, case):
        allure.dynamic.title(case.case_title)  # 动态获取allure报告的case标题
        allure.attach(body=case.url, name='接口路径')  # allure报告显示接口路径
        allure.attach(body=case.case_data, name='接口参数')  # allure报告显示接口参数

        uname = eval(case.case_data)['username']
        phone = eval(case.case_data)['phone']
        # 正确流程
        if case.case_id == 1:
            self.db.cud('DELETE FROM tb_user WHERE name=%s or phone=%s;', (uname, phone))

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()
        allure.attach(body=str(res), name='响应结果')  # allure报告显示响应结果

        try:
            assert eval(case.expect) == res  # 断言测试用例的预期结果和实际结果是否一致
            # 数据验证 验证我们有没有注册成功，如果再数据库的条目数位1，就是注册成功了
            if case.case_id == 1:
                count = self.db.find_count('SELECT * FROM tb_user WHERE name=%s;', (uname,))
                assert count == 1
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, "user_register", case.case_id, 7, '失败')  # 如果失败把断言失败把结果写入excel
            logger.error('测试编号{}，测试用例标题{}，执行失败，实际结果是{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, "user_register", case.case_id, 7, '成功')  # 如果实际结果符合预期把成功写入excel
            logger.info('测试编号{}，测试用例标题{}，执行成功，'.format(case.case_id, case.case_title))
