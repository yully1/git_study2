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
import allure
from comms.public_api import get_ini_data, replace_data


@allure.feature('商品登录模块')
class TestLogin:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        one = self.db.find_one('SELECT * FROM tb_user ORDER BY RAND() LIMIT 1;')  # 捞数据
        self.name, self.pwd = one[1], one[2]
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, 'business_token_login01')

    @allure.severity('critical')
    @allure.description('商品登录模块接口测试用例')
    @pytest.mark.parametrize('case', cases)
    def test_login(self, case):
        if "#name#" in case.case_data:  # 读取配置文件的方法
            case.case_data = replace_data(case.case_data, 'username', self.name)
            if case.case_id == 6:  # 用户名区分大小写
                case.case_data = replace_data(case.case_data, 'username', self.name.upper())

        if "#pwd#" in case.case_data:
            case.case_data = replace_data(case.case_data, 'password', self.pwd)
            if case.case_id == 5:  # 密码区分大小写
                case.case_data = replace_data(case.case_data, 'password', self.pwd.upper())

        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name="接口路径")
        allure.attach(body=case.case_data, name='请求参数')

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()
        allure.attach(body=str(res), name='响应结果')

        try:
            if case.case_id == 1:
                assert case.expect in str(res)
            else:
                assert eval(case.expect) == res
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_login01', case.case_id, 7, '失败')
            logger.error('测试编号{}，测试标题{}，执行失败，实际结果{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_login01', case.case_id, 7, '成功')
            logger.info('测试编号{}，测试标题{}，执行成功'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', './test_login05.py'])
