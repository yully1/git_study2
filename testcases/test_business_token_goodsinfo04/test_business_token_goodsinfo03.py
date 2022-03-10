"""
----------------------------------------------------
@Time  :  2022/3/4 14:02
@Author  :  shina
@File  :  test_business_token_goodsinfo.PY
----------------------------------------------------
"""
import pytest
import requests
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.public_api import replace_data, get_token
from comms.log_utils import logger
from comms.db_utils import DBUtils
import allure

"""
主流程
数据回滚和数据验证
追加其他case和allure报告
"""


@allure.feature('商品信息查询模块')
class TestGoodsInfo:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, 'business_token_goodsinfo')

    @allure.severity('critical')
    @allure.description('商品信息查询模块接口测试用例')
    @pytest.mark.parametrize("case", cases)
    def test_goods_info(self, case):
        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name="接口参数")

        if "#token#" in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())
            if case.case_id == 3:  # token区分大小写
                case.case_data = replace_data(case.case_data, 'token', get_token().upper())
            if case.case_id == 4:  # token过期的场景
                token = get_token()  # 第一次的token
                get_token()
                case.case_data = replace_data(case.case_data, 'token', token)

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()
        allure.attach(body=str(res), name='响应结果')

        try:
            if case.case_id == 1:
                assert case.expect in str(res)
                # 判断查询商品条目数是否正确
                # 1、获取返回结果的条目数
                res_count = len(res["goods_tiems"])
                # 2、获取数据库的商品条目数
                db_count = self.db.find_count("select * from tb_goods;")
                assert res_count == db_count  # 响应体的商品条目数和数据库条目是否相等
            elif case.case_id in (5, 6):
                assert case.expect in str(res)  # 判断响应体包含查询成功
                res_count = len(res["goods_tiems"])
                db_count = self.db.find_count('SELECT * FROM tb_goods WHERE isOnSale=%s;',
                                              (eval(case.case_data)['isOnSale'],))
                assert res_count == db_count  # 响应体的商品条目数和数据库商品相比较

            elif case.case_id in (7, 8):
                assert case.expect in str(res)  # 判断响应体包含查询成功
                res_count = len(res["goods_tiems"])
                db_count = self.db.find_count('SELECT * FROM tb_goods WHERE isPromote=%s;',
                                              (eval(case.case_data)['isPromote'],))
                assert res_count == db_count  # 响应体的商品条目数和数据库商品相比较

            elif case.case_id in (9, 10, 11, 12):
                assert case.expect in str(res)  # 判断响应体包含查询成功
                res_count = len(res["goods_tiems"])
                db_count = self.db.find_count('SELECT * FROM tb_goods WHERE isPromote=%s and isOnSale=%s;',
                                              (eval(case.case_data)['isPromote'], eval(case.case_data)['isOnSale']))
                assert res_count == db_count  # 响应体的商品条目数和数据库商品相比较

            elif case.case_id in (13, 14, 15, 16, 17, 18, 19, 20, 23):
                assert case.expect in str(res)  # 判断响应体包含查询成功
                res_count = len(res["goods_tiems"])

                assert res_count == 1  # 响应体的商品条目数和数据库商品相比较

            else:
                assert eval(case.expect) == res

        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_goodsinfo', case.case_id, 7, "失败")
            logger.error("测试编号{}，测试标题{}，执行失败，实际结果为{}".format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_goodsinfo', case.case_id, 7, "成功")
            logger.info("测试编号{}，测试标题{}，执行成功".format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', "--tb=line", './test_business_token_goodsinfo03.py'])
