# -*- coding: utf-8 -*-

import time

from pywe_exception import WeChatException

from .basetoken import BaseToken


class AppAccessTokenInternal(BaseToken):
    def __init__(self, appid=None, secret=None, ticket=None, token=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600, token_type='app_access_token_internal'):
        super(AppAccessTokenInternal, self).__init__(appid=appid, secret=secret, ticket=ticket, token=token, storage=storage, token_fetched_func=token_fetched_func, refresh_left_seconds=refresh_left_seconds, token_type=token_type)
        # 获取 app_access_token（企业自建应用）, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uADN14CM0UjLwQTN
        self.APP_ACCESS_TOKEN_INTERNAL = self.OPEN_DOMAIN + '/open-apis/auth/v3/app_access_token/internal/'

    def __about_to_expires(self, expires_at, refresh_left_seconds=6600):
        return expires_at and expires_at - int(time.time()) < refresh_left_seconds

    def __fetch_access_token(self, appid=None, secret=None, ticket=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600):
        # Update Params
        self.update_params(appid=appid, secret=secret, ticket=ticket, storage=storage, token_fetched_func=token_fetched_func, refresh_left_seconds=refresh_left_seconds)
        # Access Info Request
        access_info = self.post(self.APP_ACCESS_TOKEN_INTERNAL, data={'app_id': self.appid, 'app_secret': self.secret, 'app_ticket': self.ticket})
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
        return access_info.get('app_access_token')

    def access_token(self, appid=None, secret=None, ticket=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600):
        # Update Params
        self.update_params(appid=appid, secret=secret, ticket=ticket, storage=storage, token_fetched_func=token_fetched_func, refresh_left_seconds=refresh_left_seconds)
        # Fetch access_info
        access_info = self.storage.get(self.access_info_key)
        if access_info:
            access_token = access_info.get('app_access_token')
            if access_token and not self.__about_to_expires(access_info.get('expires_at'), refresh_left_seconds=refresh_left_seconds):
                return access_token
        return self.__fetch_access_token(self.appid, self.secret, self.ticket, self.storage, token_fetched_func=self.token_fetched_func, refresh_left_seconds=refresh_left_seconds)

    def refresh_access_token(self, appid=None, secret=None, ticket=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600):
        return self.__fetch_access_token(appid, secret, ticket, storage, token_fetched_func=token_fetched_func, refresh_left_seconds=refresh_left_seconds)

    def final_access_token(self, cls=None, appid=None, secret=None, ticket=None, token=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600):
        return token or self.access_token(appid or cls.appid, secret or cls.secret, ticket or cls.ticket, storage=storage or cls.storage, token_fetched_func=token_fetched_func or cls.token_fetched_func, refresh_left_seconds=refresh_left_seconds or cls.refresh_left_seconds)


token = AppAccessTokenInternal()
app_access_token_internal = token.access_token
refresh_app_access_token_internal = token.refresh_access_token
final_app_access_token_internal = token.final_access_token
