# -*- coding: utf-8 -*-

from .app_access_token import AppAccessToken, final_app_access_token


class Authen(AppAccessToken):
    def __init__(self, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        super(Authen, self).__init__(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)
        # 获取登录用户身份, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uEDO4UjLxgDO14SM4gTN
        self.AUTHEN_V1_ACCESS_TOKEN = self.OPEN_DOMAIN + '/open-apis/authen/v1/access_token'

    def get_userinfo(self, code=None, grant_type='authorization_code', appid=None, secret=None, ticket=None, token=None, storage=None):
        # Update params
        self.update_params(appid=appid, secret=secret, ticket=ticket, storage=storage)
        # Fetch sessionInfo
        token = final_app_access_token(self, appid=appid, secret=secret, ticket=ticket, token=token, storage=storage)
        return self.post(self.AUTHEN_V1_ACCESS_TOKEN, data={
            'app_access_token': token,
            'grant_type': grant_type,
            'code': code,
        }).get('data', {})


authen = Authen()
get_userinfo = authen.get_userinfo
