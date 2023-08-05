# coding=utf-8
import functools
import json
import random
import sys
from string import ascii_uppercase
from time import time

if sys.version_info < (3, 1):
    from urllib import urlencode
else:
    from urllib.parse import urlencode

import requests

from .lib import post_request, pre_request


def random_string():
    return "".join(
        [random.choice(ascii_uppercase) for _ in range(random.randint(2, 6))]
    )


class getTokenError(Exception):
    pass


class LarkError(Exception):
    pass


class LarkRequestError(LarkError):
    pass


class LarkValueError(LarkError):
    pass


class LarkInitError(LarkError):
    pass


class InitTokenError(LarkError):
    pass


class Lark:
    """Lark Sdk 

    Raises:
        InitTokenError: 获取 Token 失败

    Returns:
        lark: lark 的基础实例 在这里完成获取 SDK 等任务
    """

    TOKEN_INIT_URL = (
        "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
    )
    AUTH_STRING = "https://open.feishu.cn/open-apis/authen/v1/index"
    CALLBACK_URL = "http://retrace.bytedance.net/research/callback/"
    CODE2TOKEN_URL = "https://open.feishu.cn/open-apis/authen/v1/access_token"

    def set_attr(cls, key, value):
        setattr(cls, key, value)

    def get_attr(cls, key):
        return getattr(cls, key, None)

    def __init__(self, app_id, secret, set_attr=None, get_attr=None):
        """初始化 Lark 的 SDK 

        Args:
            app_id (string): app_id
            secret (string): app_secrete
            set_attr (func, optional): 给类绑定值，可以进行修改用于使用 redis 来创建变量. Defaults to None.
            get_attr (fucn, optional): 用于从实例中获取变量. Defaults to None.
        """
        self.set_attr = set_attr if set_attr else self.set_attr
        self.get_attr = get_attr if get_attr else self.get_attr
        # TODO: 使用 getter 和 setter 进行封装
        self.set_attr("app_id", app_id)
        self.set_attr("secret", secret)
        self.init_token()

    @staticmethod
    def data_parser(data, fields, use_dict=False):
        """用于数据过滤 避免存储不合规的数据

        Args:
            data (dict): 数据类型
            fields (list): 要保存的字段
            use_dict (bool): 返回的数据对象是否为 dict
        Return:
            data (list): value 的 列表 
        """
        return (
            {field: data[field] for field in fields}
            if use_dict
            else [data[field] for field in fields]
        )

    @pre_request
    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs)

    @pre_request
    def post(self, *args, **kwargs):
        return requests.post(*args, **kwargs)

    @pre_request
    def put(self, *args, **kwargs):
        return requests.put(*args, **kwargs)

    def init_token(self):
        """使用 APP_ID + SECRET 获取 Token

        Raises:
            getTokenError: 获取 用户信息 失败
        """
        response = self.post(
            self.TOKEN_INIT_URL, json={"app_id": self.app_id, "app_secret": self.secret}
        )
        if response["msg"] != "ok":
            raise getTokenError(response["msg"])
        app_access_token, expire = response["app_access_token"], response["expire"]
        self.set_attr("app_access_token", app_access_token)

    @post_request(LarkRequestError, parse_func=lambda response: response["bot"])
    def get_bot_info(self):
        """获取机器人自身信息
        https://open.feishu.cn/document/ukTMukTMukTM/uAjMxEjLwITMx4CMyETM
        
        Returns:
            Bot:{
                "activate_status": 2,
                "app_name": "name",
                "avatar_url": "https://sf1-ttcdn-tos.pstatp.com/obj/lark.avatar/da5xxxx14b16113",
                "ip_white_list": [],
                "open_id": "ou_xxx"  
            }
        """
        URL = "https://open.feishu.cn/open-apis/bot/v3/info/"
        return self.get(URL)

    def get_access_token(self):
        return self.get_attr("app_access_token")

    def code2userinfo(self, code):
        """使用 Code 获取用户信息

        Args:
            code (string): 回调获取到的 code

        Returns:
            userinfo: 获取的 userinfo 结构体 其中包含了 userToken，refreshToken，以及 openid 等用户信息

        userinfo: {
            "access_token": string,
            "en_name": string,
            "expires_in": int,
            "name": string,
            "open_id": string,
            "refresh_expires_in": int,
            "refresh_token": string,
            "tenant_key": string,
            "token_type": string
            "email": string
        }
        """
        response = self.post(
            self.CODE2TOKEN_URL,
            json={
                "app_access_token": self.get_access_token(),
                "grant_type": "authorization_code",
                "code": code,
            },
        )
        if response["code"] != 0:
            raise LarkError(response["msg"])
        return self.data_parser(
            response["data"],
            fields=[
                "access_token",
                "en_name",
                "name",
                "open_id",
                "expires_in",
                "refresh_token",
                "tenant_key",
            ],
            use_dict=True,
        )

    def get_redirect_uri(self, callback_url=None, state=None):
        """生成 SSO 登录回调链接 （ docs 需要）

        Args:
            callback_url (str, optional): callback_url. Defaults to None.
            state (str, optional): state. Defaults to None.

        Returns:
            uri: str,构造的回调链接
        """
        callback_url = callback_url if callback_url else self.CALLBACK_URL
        state = state if state else random_string()
        return (
            self.AUTH_STRING
            + "?"
            + urlencode(
                {"redirect_uri": callback_url, "app_id": self.app_id, "state": state,}
            )
        )
