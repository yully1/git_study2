"""
----------------------------------------------------
@Time  :  2022/3/7 10:12
@Author  :  shina
@File  :  test_business_token_goods_input01.PY
----------------------------------------------------
"""
import pytest
import requests
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.log_utils import logger
from comms.public_api import replace_data, get_token, get_ini_data
from comms.db_utils import DBUtils
import allure

"""
主流程
数据回滚和验证，allure报告
"""


@allure.feature('商品信息录入模块')
class TestGoodsInput:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, 'business_token_goods_input')

    @allure.severity('normal')
    @allure.description('商品信息录入接口测试用例')
    @pytest.mark.parametrize('case', cases)
    def test_goods_input(self, case):
        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name='请求参数')
        goodsname = eval(case.case_data)['goodsName']

        if case.case_id in (1, 6, 11, 12, 15, 20):
            self.db.cud('DELETE FROM tb_goods WHERE goodsName=%s;', (goodsname,))

        if '#token#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())
            if case.case_id == 3:
                case.case_data = replace_data(case.case_data, 'token', get_token().upper())
            if case.case_id == 4:
                token = get_token()
                get_token()
                case.case_data = replace_data(case.case_data, 'token', token)

        if '#goodsTypeId#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'goodsTypeId', get_ini_data('users2', 'goodsTypeId'))
        if '#number#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'number', get_ini_data('users2', 'number'))
        if '#shopPrice#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'shopPrice', get_ini_data('users2', 'shopPrice'))

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()
        allure.attach(body=str(res), name="响应结果")

        try:

            assert eval(case.expect) == res
            if case.case_id in (1, 6, 11, 12, 15, 20):
                count = self.db.find_count('SELECT * FROM tb_goods WHERE goodsName=%s;', (goodsname,))
                assert count == 1

        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_input', case.case_id, 7, '失败')
            logger.error('测试编号{}，测试标题{}，执行失败，实际结果为{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_input', case.case_id, 7, '成功')
            logger.info('测试编号{}，测试标题{}，执行成功'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', "--tb=line", './test_business_token_goods_input01.py'])
