"""
----------------------------------------------------
@Time  :  2022/2/22 16:07
@Author  :  shina
@File  :  python_senior010.PY
----------------------------------------------------
"""
"""
flask框架介绍：该框架为后端服务能够部署服务，这样我们的接口、代码就能扣使用http协议来调用
json.dumps 是把字典格式转换为json格式
json.loads 是把json格式转换为字典格式
"""
# 第一步：通过pip install 导入该库
import flask
import json
from comms.db_utils import DBUtils

# 创建app对象，把当前的python文件当成一个服务，__name__代表当前文件
app = flask.Flask(__name__)


# 第三步：我们将接口发布成服务，route是路由的意思
# 登录接口
@app.route('/user_login', methods=['post', 'get'])
def login():
    data = flask.request.values  # 接受请求发送过来的数据
    print(data)  # 打印出来的是一个字典CombinedMultiDict([ImmutableMultiDict([('username', 'huahua1'), ('password', 'a123456')])])
    uname = data.get("username")  # 获取请求中username对应的值
    pwd = data.get("password")  # 获取请求中password
    if len(uname) == 0:
        return json.dumps({"code": 1001, "msg": "用户名不能为空"}, ensure_ascii=False)
    elif len(pwd) == 0:
        return json.dumps({"code": 1002, "msg": "密码不能为空"}, ensure_ascii=False)
    else:  # 查询数据库，看看用户传入的用户名和密码再数据中是否存
        db = DBUtils()
        # 从数据库查询用户名等于接口传入的用户名并且密码等于传入的密码
        count = db.find_count("SELECT * FROM tb_user WHERE name=%s AND passwd=%s;", (uname, pwd))
        db.close()
        if count == 0 or count == -1:
            return json.dumps({"code": 1003, "msg": "用户名或密码错误"}, ensure_ascii=False)
        else:
            return json.dumps({"code": 9999, "msg": "登录成功"}, ensure_ascii=False)


# 注册接口
@app.route('/user_register', methods=('post', 'get'))
def register():
    data = flask.request.values
    uname = data.get('username')
    pwd = data.get('password')
    re_pwd = data.get('re_password')
    email = data.get('email')
    phone = data.get('phone')
    if len(uname) == 0:
        return json.dumps({"code": 1001, "msg": "用户名不能为空"}, ensure_ascii=False)
    elif len(pwd) == 0:
        return json.dumps({"code": 1002, "msg": "密码不能为空"}, ensure_ascii=False)
    elif pwd != re_pwd:
        return json.dumps({"code": 1003, "msg": "两次密码输入不一致"}, ensure_ascii=False)
    elif not (6 <= len(uname) <= 18 and 6 <= len(pwd) <= 18):
        return json.dumps({"code": 1004, "msg": "用户名和密码必须在6-18位之间"}, ensure_ascii=False)
    elif len(email) == 0:
        return json.dumps({"code": 1005, "msg": "邮箱不能为空"}, ensure_ascii=False)
    elif len(phone) == 0:
        return json.dumps({"code": 1006, "msg": "手机号不能为空"}, ensure_ascii=False)
    elif not ('@' in email and '.com' in email):
        return json.dumps({"code": 1007, "msg": "邮箱格式错误"}, ensure_ascii=False)
    else:
        db = DBUtils()
        count = db.find_count("SELECT * FROM tb_user WHERE name=%s;", (uname,))
        count1 = db.find_count("SELECT * FROM tb_user WHERE phone=%s;", (phone,))
        if count != 0:
            db.close()
            return {"code": 1007, "msg": "该用户已存在"}
        elif count1 != 0 and count == 0:
            db.close()
            return {"code": 1008, "msg": "该手机号已被注册"}
        else:
            count3 = db.cud("INSERT INTO tb_user(name,passwd,email,phone) VALUES(%s,%s,%s,%s);",
                            (uname, pwd, email, phone))
            db.close()
            if count3 == 1:
                return json.dumps({"code": 9999, "msg": "注册成功"}, ensure_ascii=False)
            else:
                return json.dumps({"code": 0000, "msg": "注册失败，环境异常，请联系管理员"}, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
