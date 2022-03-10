"""
----------------------------------------------------
@Time  :  2022/3/3 14:01
@Author  :  shina
@File  :  test_business_register01.PY
----------------------------------------------------
"""
import pytest
from comms.excel_utils import ReadExcel
import requests
from comms.constants import DATA_FILE
from comms.log_utils import logger
from comms.db_utils import DBUtils
import allure

"""
1、主流程
2、数据回滚和数据验证
    1，增加夹具，再读取数据之前
    2、再请求之前回滚，请求之后验证
3、增加其他case和allure报告
    
"""


@allure.feature("商品注册模块")
class TestRegister:
    @pytest.fixture(autouse=True)  # 因为总是需要操作数据库，所有写个数据库创建对象和关闭的夹具
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, 'business_register01', )

    @allure.severity('critical')
    @allure.description('商品注册模块接口测试用例')
    @pytest.mark.parametrize('case', cases)
    def test_register(self, case):
        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name='接口参数')

        uname = eval(case.case_data)['username']
        email = eval(case.case_data)['email']
        phone = eval(case.case_data)['phone']

        # 正确流程数据回滚
        if case.case_id in (1, 3, 13, 28, 31, 36, 38):
            self.db.cud('DELETE FROM tb_user WHERE name=%s or email=%s or phone=%s;', (uname, email, phone,))
        if case.case_id == 6:  # 用户名已注册
            self.db.cud('DELETE FROM tb_user WHERE email=%s or phone=%s;', (email, phone,))
        if case.case_id == 27:  # 手机已注册
            self.db.cud('DELETE FROM tb_user WHERE uname=%s or email=%s', (uname, email,))
        if case.case_id == 40:  # 邮箱已注册
            self.db.cud('DELETE FROM tb_user WHERE uname=%s or phone=%s', (uname, phone,))

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()
        allure.attach(body=str(res), name='响应结果')

        try:
            assert eval(case.expect) == res
            # 数据验证
            if case.case_id in (1, 3, 13, 28, 31, 36, 38):
                count = self.db.find_count('SELECT * FROM tb_user WHERE name=%s;', (uname,))
                assert count == 1

        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_register01', case.case_id, 7, '失败')
            logger.error('测试标号{}，测试标题{}，执行失败，实际结果为{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_register01', case.case_id, 7, '成功')
            logger.info('测试标号{}，测试标题{}，执行成功'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', '--tb=line', './test_business_register03.py'])
