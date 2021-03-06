# -*- coding:utf-8 -*-
#!/usr/bin/python
# Install the Python Requests library:
# `pip install requests`

import json
import unittest
import time
import paramunittest
import uuid
from random import choice
import string
from common.Log import MyLog
from common import commontest
from common import url
from common import configHttp
from common import jikeToken

usersRegister_xls = commontest.get_xls_case("userCase.xlsx", "usersRegister")
configHttp = configHttp.ConfigHttp()

@paramunittest.parametrized(*usersRegister_xls)
class TestUsersRegister(unittest.TestCase):
    def setParameters(self, case_name, method,result):

        self.case_name = str(case_name)
        self.method = str(method)
        self.response = None
        self.result = str(result)


    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def random_password(self):
        """
        生成16位随机密码
        :return: 返回密码
        """
        length=16
        chars = string.ascii_letters + string.digits
        paw=''.join([choice(chars) for _ in range(length)])
        return paw


    def testUsersRegister(self):
        """
        test body
        :return:
        """
        # set url
        self.url = url.users_register
        configHttp.set_url(self.url)

        # set headers
        configHttp.set_local_headers()

        # set data
        data = json.dumps({
                    "username": str(uuid.uuid4()).upper(),
                    "password": self.random_password()
                })
        configHttp.set_data(data)

        # test interface
        self.response = configHttp.post()

        # check result
        self.checkResult()


    def tearDown(self):
        time.sleep(1)
        if self.response.status_code == 200:
            token = {
                "x-jike-access-token": self.response.headers.get('x-jike-access-token'),
                "x-jike-refresh-token": self.response.headers.get('x-jike-refresh-token')
            }
            jikeToken.save_token(token)
        else:
            pass

        self.log.build_case_line(self.case_name, str(self.response))
        print("测试结束，输出log完结\n\n")


    def checkResult(self):
        """
        检查测试结果
        :return:
        """
        self.info = self.response.json()#返回json数据
        commontest.show_return_msg(self.response)#显示返回消息


        if self.result == '1':
            self.assertEqual(self.response.status_code,200)




if __name__ == '__main__':
      unittest.main()