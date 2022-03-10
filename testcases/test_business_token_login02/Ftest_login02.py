"""
----------------------------------------------------
@Time  :  2022/3/2 17:30
@Author  :  shina
@File  :  test_login01.PY
----------------------------------------------------
"""
"""
自动化步骤：
1、把接文档的接口放在postman调一遍。没有稳定就抓包，调不通就找开发
2、开始写case
3、开始写写代码：
    
"""
"""
1、自动化主流程
    第一步：引pytest包，创建一个pytest框架的TestLogin类和test_login()方法
    第二步：引入excel表格的封装方法，读取excel的表头数据
    第三步：引入路径，再excel读取方法里面需要使用
    第四步:引入requests库，模拟接口测试工具,把数据参数化
    第五步：给case增加夹具
    第六步：数据回滚和数据验证，
"""
import pytest
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
import requests
from comms.log_utils import logger
from comms.db_utils import DBUtils


class TestLogin:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_pl(DATA_FILE, 'business_token_login', 1, 1)

    @pytest.mark.parametrize('case', cases)
    def test_login(self, case):

        # 正确流程
        if case.case_id == 1:
            uname = eval(case.case_data)['username']
            pwd = eval(case.case_data)['password']
            self.db.cud('DELETE FROM tb_user WHERE name=%s;', (uname,))
            self.db.cud('INSERT INTO tb_user(name,passwd,email,phone) VALUES(%s,%s,%s,%s);',
                        (uname, pwd, 'tester24@163.com', '13112331233'))
        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()

        try:
            if case.case_id == 1:
                assert case.expect in str(res)
            else:
                assert eval(case.expect) == res
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_login', case.case_id, 7, '失败')
            logger.error('测试编号{}，测试标题{}，执行失败，实际结果{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_login', case.case_id, 7, '成功')
            logger.info('测试编号{}，测试标题{}，执行成功'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', './Ftest_login02.py'])
