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

"""
主流程
数据回滚和数据验证
"""


class TestGoodsInfo:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_pl(DATA_FILE, 'business_token_goodsinfo', 1, 1)

    @pytest.mark.parametrize("case", cases)
    def test_goods_info(self, case):
        if "token" in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())
        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()

        try:
            if case.case_id == 1:
                assert case.expect in str(res)
                # 判断查询商品条目数是否正确
                # 1、获取返回结果的条目数
                res_count = len(res["goods_tiems"])
                # 2、获取数据库的商品条目数
                db_count = self.db.find_count("select * from tb_goods;")
                assert res_count == db_count  # 响应体的商品条目数和数据库条目是否相等
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
    pytest.main(['-vs', './Ftest_business_token_goodsinfo02.py'])
