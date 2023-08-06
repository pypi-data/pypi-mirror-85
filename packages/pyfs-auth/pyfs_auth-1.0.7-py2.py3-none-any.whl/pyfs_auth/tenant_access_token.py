# -*- coding: utf-8 -*-

import time

from pywe_exception import WeChatException

from app_access_token import AppAccessToken, final_app_access_token


class TenantAccessToken(AppAccessToken):
    def __init__(self, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600, token_type='tenant_access_token'):
        super(TenantAccessToken, self).__init__(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage, token_fetched_func=token_fetched_func, refresh_left_seconds=refresh_left_seconds, token_type=token_type)
        # 获取 tenant_access_token（应用商店应用）, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uMjNz4yM2MjLzYzM
        self.TENANT_ACCESS_TOKEN = self.OPEN_DOMAIN + '/open-apis/auth/v3/tenant_access_token/'

    def __about_to_expires(self, expires_at, refresh_left_seconds=6600):
        return expires_at and expires_at - int(time.time()) < refresh_left_seconds

    def __fetch_access_token(self, appid=None, secret=None, ticket=None, tenant_key=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600):
        # Update Params
        self.update_params(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, storage=storage, token_fetched_func=token_fetched_func, refresh_left_seconds=refresh_left_seconds)
        # Access Info Request
        app_access_token = final_app_access_token(self, appid=self.appid, secret=self.secret, ticket=self.ticket, storage=self.storage)
        access_info = self.post(self.TENANT_ACCESS_TOKEN, data={'app_access_token': app_access_token, 'tenant_key': tenant_key}, authorization=False)
        # Request Error
        if 'expire' not in access_info:
            raise WeChatException(access_info)
        # Set Access Info into Storage
        expires_in = access_info.get('expire')
        access_info['expires_at'] = int(time.time()) + expires_in
        self.storage.set(self.access_info_key, access_info, expires_in)
        # If token_fetched_func, Call it with `appid`, `secret`, `ticket`, `access_info`
        if token_fetched_func:
            token_fetched_func(self.appid, self.secret, self.ticket, access_info)
        # Return Access Token
        return access_info.get('tenant_access_token')

    def access_token(self, appid=None, secret=None, ticket=None, tenant_key=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600):
        # Update Params
        self.update_params(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, storage=storage, token_fetched_func=token_fetched_func, refresh_left_seconds=refresh_left_seconds)
        # Fetch access_info
        access_info = self.storage.get(self.access_info_key)
        if access_info:
            access_token = access_info.get('tenant_access_token')
            if access_token and not self.__about_to_expires(access_info.get('expires_at'), refresh_left_seconds=refresh_left_seconds):
                return access_token
        return self.__fetch_access_token(self.appid, self.secret, self.ticket, self.tenant_key, self.storage, token_fetched_func=self.token_fetched_func, refresh_left_seconds=refresh_left_seconds)

    def refresh_access_token(self, appid=None, secret=None, ticket=None, tenant_key=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600):
        return self.__fetch_access_token(appid, secret, ticket, tenant_key, storage, token_fetched_func=token_fetched_func, refresh_left_seconds=refresh_left_seconds)

    def final_access_token(self, cls=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600):
        return token or self.access_token(appid or cls.appid, secret or cls.secret, ticket or cls.ticket, tenant_key or cls.tenant_key, storage=storage or cls.storage, token_fetched_func=token_fetched_func or cls.token_fetched_func, refresh_left_seconds=refresh_left_seconds or cls.refresh_left_seconds)


token = TenantAccessToken()
tenant_access_token = token.access_token
refresh_tenant_access_token = token.refresh_access_token
final_tenant_access_token = token.final_access_token
