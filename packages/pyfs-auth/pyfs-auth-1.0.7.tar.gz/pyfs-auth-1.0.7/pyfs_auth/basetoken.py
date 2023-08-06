# -*- coding: utf-8 -*-

import time

from pyfs_base import BaseFeishu
from pywe_storage import MemoryStorage


class BaseToken(BaseFeishu):
    def __init__(self, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600, token_type=''):
        super(BaseToken, self).__init__()
        self.appid = appid
        self.secret = secret
        self.ticket = ticket
        self.tenant_key = tenant_key
        self.token = token
        self.storage = storage or MemoryStorage()
        self.token_fetched_func = token_fetched_func
        self.refresh_left_seconds = refresh_left_seconds
        self.token_type = token_type

        if self.token:
            expires_in = 7200
            access_info = {
                'access_token': self.token,
                'expires_in': expires_in,
                'expires_at': int(time.time()) + expires_in,
            }
            self.storage.set(self.access_info_key, access_info, expires_in)

    @property
    def access_info_key(self):
        return 'feishu:{0}:{1}:info'.format(self.appid, self.token_type)

    def update_params(self, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None, token_fetched_func=None, refresh_left_seconds=6600, token_type=''):
        self.appid = appid or self.appid
        self.secret = secret or self.secret
        self.ticket = ticket or self.ticket
        self.tenant_key = tenant_key or self.tenant_key
        self.token = token or self.token
        self.storage = storage or self.storage
        self.token_fetched_func = token_fetched_func or self.token_fetched_func
        self.refresh_left_seconds = refresh_left_seconds or self.refresh_left_seconds
        self.token_type = token_type or self.token_type
