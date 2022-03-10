"""
----------------------------------------------------
@Time  :  2022/3/8 16:11
@Author  :  shina
@File  :  test_business_regist_json01.PY
----------------------------------------------------
"""
import json

import pytest
import requests
from comms.constants import DATA_FILE
from comms.excel_utils import ReadExcel
import json
from comms.log_utils import logger
from comms.db_utils import DBUtils


class TestRegistJson:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_pl(DATA_FILE, 'business_regist_json', 1, 1)

    @pytest.mark.parametrize('case', cases)
    def test_regist_json(self, case):
        uname = eval(case.case_data)['username']
        email = eval(case.case_data)['email']
        phone = eval(case.case_data)['phone']
        if case.case_id == 1:
            self.db.cud('DELETE FROM tb_user WHERE name=%s or email=%s or phone=%s;', (uname, email, phone,))

        response = requests.post(url=case.url, data=json.dumps(eval(case.case_data)),
                                 headers={"Content-Type": "application/json"})
        res = response.json()

        try:

            assert eval(case.expect) == res
            if case.case_id == 1:
                count = self.db.find_count('SELECT * FROM tb_user WHERE name=%s;', (uname,))
                assert count == 1
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_regist_json', case.case_id, 7, '失败')
            logger.error("测试编号{}，测试标题{},执行失败，实际结果为{}".format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_regist_json', case.case_id, 7, '成功')
            logger.info("测试编号{}，测试标题{},执行成功".format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', '--tb=line', './test_business_regist_json01.py'])
