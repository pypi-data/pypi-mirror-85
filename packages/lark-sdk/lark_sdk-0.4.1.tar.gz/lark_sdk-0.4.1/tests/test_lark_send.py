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


class larkSenderTest(TestCase):
    def setUp(self):
        self.APP_ID = get_config(APP_ID)
        self.SECRET = get_config(APP_SECRET)
        self.EMAIL = get_config(USER_EMAIL)
        self.open_ids = [get_config(OPEN_ID)]
        self.lark_sender = LarkSender(self.APP_ID, self.SECRET, {"email": self.EMAIL})
        self.message_id = self.lark_sender.send_text("Hey")["message_id"]

    def test_lark_send_test_to_email(self):
        response = self.lark_sender.send_text("Hey")
        self.assertTrue(response["message_id"])

    def test_lark_send_post_to_email(self):
        response = self.lark_sender.send_post(
            "Hey", [[{"tag": "text", "un_escape": True, "text": "Hey&nbsp;"}]]
        )
        self.assertTrue(response["message_id"])

    def test_lark_read_info(self):
        read_info = self.lark_sender.read_info(self.message_id)
        self.assertTrue(read_info)

    def test_lark_recall(self):
        response = self.lark_sender.recall_message(self.message_id)
        self.assertTrue(response["code"] == 0)

    def test_lark_urgent(self):
        lark_sender = LarkSender(
            self.APP_ID, self.SECRET, {"email": self.EMAIL, "open_ids": self.open_ids}
        )
        message = lark_sender.urgent(self.message_id)
        self.assertTrue(message)
