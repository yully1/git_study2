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

"""
主流程
数据回滚和数据验证
    1，增加夹具，再读取数据之前
    2、再请求之前回滚，请求之后验证
"""


class TestRegister:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_pl(DATA_FILE, 'business_register00', 1, 1)

    @pytest.mark.parametrize('case', cases)
    def test_register(self, case):
        uname = eval(case.case_data)['username']
        email = eval(case.case_data)['email']
        phone = eval(case.case_data)['email']

        # 正确流程
        if case.case_id == 1:
            self.db.cud('DELETE FROM tb_user WHERE name=%s or email=%s or phone=%s;', (uname, email, phone,))

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()

        try:
            assert eval(case.expect) == res
            # 数据验证
            if case.case_id == 1:
                count = self.db.find_count('SELECT * FROM tb_user WHERE name=%s;', (uname,))
                assert count == 1

        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_register00', case.case_id, 7, '失败')
            logger.error('测试标号{}，测试标题{}，执行失败，实际结果为{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_register00', case.case_id, 7, '成功')
            logger.info('测试标号{}，测试标题{}，执行成功'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', './ftest_business_register02.py'])
