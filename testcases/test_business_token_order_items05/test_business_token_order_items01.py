"""
----------------------------------------------------
@Time  :  2022/3/5 15:53
@Author  :  shina
@File  :  test_business_token_order_items01.PY
----------------------------------------------------
"""
"""
主流程
"""
import pytest
import requests
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.db_utils import DBUtils
from comms.public_api import replace_data, get_token
from comms.log_utils import logger
import allure


@allure.feature('订单信息查询模块')
class TestOrderItems:
    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        one = self.db.find_one("SELECT * FROM tb_order ORDER BY RAND();")
        self.orderId = one[0]
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, 'business_token_order_items')

    @allure.severity('critical')
    @allure.description("订单信息查询接口测试用例")
    @pytest.mark.parametrize('case', cases)
    def test_order_items(self, case):
        allure.dynamic.title(case.case_title)

        if '#token#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())
            if case.case_id == 3:
                case.case_data = replace_data(case.case_data, 'token', get_token().upper())
            if case.case_id == 4:
                token = get_token()
                get_token()
                case.case_data = replace_data(case.case_data, 'token', token)

        if '#orderId#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'orderId', self.orderId)
        if case.case_id == 7:  # orderId不存在的场景
            self.db.cud('DELETE FROM tb_order WHERE orderId=%s;', (eval(case.case_data)['orderId']), )

        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name='请求参数')
        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()
        allure.attach(body=str(res), name='响应结果')

        try:
            # 四表连接查询orderId数据，如果查询多条和goods_times比较，如何查询数据断言响应报文包含查询成功，如果没有查询到数据，断言包含查询无结果
            if case.case_id == 1:
                sql = 'SELECT * FROM tb_user u,tb_order o,tb_order_goods og,tb_goods g WHERE u.userId=o.userId AND ' \
                      'o.orderId=og.orderId AND og.goodsId=g.goodsId AND o.orderId=%s;'
                count = self.db.find_count(sql, (self.orderId,))
                if count > 0:
                    assert '查询成功' in str(res)
                    assert count == len(res["goods_tiems"])
                elif count == 0:
                    assert '查询无结果' in str(res)
            else:
                assert eval(case.expect) == res
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_order_items', case.case_id, 7, '失败')
            logger.error('测试编号{}，测试标题{}，测试失败，实际结果{}'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_order_items', case.case_id, 7, '成功')
            logger.info('测试编号{}，测试标题{}，测试成功'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', "--tb=line", './test_business_token_order_items01.py'])
