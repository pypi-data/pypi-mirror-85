# -*- coding: utf-8 -*-

from .basetoken import BaseToken


class AppTicket(BaseToken):
    def __init__(self, appid=None, secret=None):
        super(AppTicket, self).__init__(appid=appid, secret=secret)
        # 重新推送 app_ticket, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uQjNz4CN2MjL0YzM
        self.APP_TICKET_RESEND = self.OPEN_DOMAIN + '/open-apis/auth/v3/app_ticket/resend/'

    def resend(self, appid=None, secret=None):
        return self.post(self.APP_TICKET_RESEND, data={
            'app_id': appid or self.appid,
            'app_secret': secret or self.secret,
        })


app_ticket = AppTicket()
app_ticket_resend = app_ticket.resend
