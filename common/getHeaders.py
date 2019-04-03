# -*- coding:utf-8 -*-
#!/usr/bin/python
import requests
import json
from common import jikeToken


class GetHeaders():

    def localHeaders():
        """
        本地Headers
        :return:local_headers
        """
        local_headers = {
            "OS": "ios",
            "OS-Version": "Version 12.1.4 (Build 16D57)",
            "App-Version": "5.7.0",
            "App-BuildNo": "1314",
            "Manufacturer": "Apple",
            "Model": "iPhone11,6",
            "BundleID": "com.ruguoapp.jike",
            "x-jike-device-id": "4DA0BE6A-69D6-4C3B-BCD3-A77310872F36",
            "WifiConnected": "true",
            "King-Card-Status": "unknown",
            "Notification-Status": "OFF",
            "User-Agent": "%E5%8D%B3%E5%88%BB/1341 CFNetwork/976 Darwin/18.2.0",
            "Content-Type": "application/json; charset=utf-8",
        }
        return local_headers


    def getHeaders():
        """
        正式Headers
        :return:headers
        """
        access_token={
            "x-jike-access-token": jikeToken.getToken().get('x-jike-access-token')
        }
        headers = GetHeaders.localHeaders()
        headers.update(access_token)

        return headers



    def refreshTokens():
        """
        app_auth_tokens.refresh刷新token，保存到本地
        :return:
        """
        try:
            response = requests.post(
                url="https://app.jike.ruguoapp.com/1.0/app_auth_tokens.refresh",
                headers={
                    "x-jike-device-id": "4DA0BE6A-69D6-4C3B-BCD3-A77310872F36",
                    "x-jike-refresh-token": jikeToken.getToken().get('x-jike-refresh-token')
                },
            )

            token = {
                "x-jike-access-token": response.headers.get('x-jike-access-token'),
                "x-jike-refresh-token": response.headers.get('x-jike-refresh-token')
            }
            jikeToken.saveToken(token)

        except requests.exceptions.RequestException:
            print('HTTP Request failed')


    def getRefreshToken():
        """
        登录刷新token保存到本地
        :return:
        """
        try:
            response = requests.post(
                url="https://app-beta.jike.ruguoapp.com/1.0/users/loginWithPhoneAndPassword",
                headers=self.loginHeaders(),
                data=json.dumps({
                    "mobilePhoneNumber": "16666666666",
                    "password": "111111",
                    "areaCode": "+86"
                })
            )

            token = {
                "x-jike-access-token": response.headers.get('x-jike-access-token'),
                "x-jike-refresh-token": response.headers.get('x-jike-refresh-token')
            }
            jikeToken.saveToken(token)

        except requests.exceptions.RequestException:
            print('HTTP Request failed')


if __name__ == '__main__':
    GetHeaders.getHeaders()