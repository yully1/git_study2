"""
----------------------------------------------------
@Time  :  2022/3/8 14:36
@Author  :  shina
@File  :  test_business_token_goods_delete01.PY
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


@allure.feature('商品删除模块')
class TestGoodsDelete:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, 'business_token_goods_delete')

    @allure.severity('critical')
    @allure.description('商品删除模块几口测试用例')
    @pytest.mark.parametrize('case', cases)
    def test_goods_delete(self, case):
        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name="接口路径")
        allure.attach(body=case.case_data, name='请求参数')

        if '#token#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())
        if "#goodsId#" in case.case_data:
            case.case_data = replace_data(case.case_data, 'goodsId', get_ini_data('goodsId2', 'goodsId'))

        if case.case_id == 1:
            self.db.cud(
                "INSERT INTO `businessdb`.`tb_goods` (`goodsId`, `goodsName`, `goodsTypeId`, `descp`, `num`, `onTime`, `offTime`, `shopPrice`, `promotePrice`, `promoteStartTime`, `promoteEndTime`, `isOnSale`, `isPromote`, `givePoints`) VALUES (%s ,'nananananan', '10001', NULL, '100', '2022-03-08 21:17:44', '2099-12-31', '200.00', '0.00', NULL, NULL, '1', '1', '10');",
                (get_ini_data('goodsId2', 'goodsId'),))

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()
        allure.attach(body=str(res), name='响应结果')

        try:
            assert eval(case.expect) == res
            if case.case_id == 1:
                count = self.db.find_count("SELECT * FROM tb_goods WHERE goodsId=%s;",
                                           (get_ini_data('goodsId2', 'goodsId'),))
                assert count == 0

        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_delete', case.case_id, 7, '失败')
            logger.error('测试编号{},测试标题{}，执行失败，实际结果{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_delete', case.case_id, 7, '成功')
            logger.info('测试编号{},测试标题{}，执行成功'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', '--tb=line', './test_business_token_goods_delete01.py'])
