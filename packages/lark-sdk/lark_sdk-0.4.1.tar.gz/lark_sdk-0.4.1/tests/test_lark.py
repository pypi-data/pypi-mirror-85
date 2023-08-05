#!/usr/bin/env python

import os
import unittest
from unittest import TestCase

import pytest

from lark_sdk import Lark, LarkSender

from .utils import *

# 需要的 config 信息
APP_ID = "APP_ID"
APP_SECRET = "SECRET"
USER_EMAIL = "EMAIL"
OPEN_ID = "OPEN_ID"


class LarkUtilTestCase(TestCase):
    def setUp(self):
        self.APP_ID = get_config(APP_ID)
        self.SECRET = get_config(APP_SECRET)

    def test_lark_sdk_init(self):
        """测试初始化
        """
        lark = Lark(self.APP_ID, self.SECRET)
        self.assertTrue(lark.app_access_token)

    def test_lark_get_bot_info(self):
        lark = Lark(self.APP_ID, self.SECRET)
        bot_info = lark.get_bot_info()
        print(bot_info)
        self.assertTrue(bot_info)
