# coding: utf-8
#!/usr/bin/env python
import json
import unittest
from os import path
from pathlib import Path  # if you haven't already done so
from unittest import TestCase

if __name__ == "__main__":
    import sys

    file = Path(__file__).resolve()
    parent, root = file.parent, file.parents[1]
    sys.path.append(str(root))
    from utils import Config, get_config, set_config
else:
    from .utils import Config, set_config, get_config

from lark_sdk import Lark, LarkDocs, random_string

config = Config("lark_docs.json")
# 需要的 config 信息
APP_ID = "APP_ID"
SECRET = "SECRET"
SHEET_TOKEN = "SHEET_TOKEN"
SHEET_RANGE = "SHEET_RANGE"
DOCS_REFRESH_TOKEN = "DOCS_REFRESH_TOKEN"
DOCS_ACCESS_TOKEN = "DOCS_REFRESH_TOKEN"


def get_app_access_token():
    lark = Lark(config.APP_ID, config.SECRET)
    return lark.get_attr("app_access_token")


def set_attr(name, value):
    set_config(name, value, filename="lark_docs.json")


def get_attr(name):
    return get_config(name, filename="lark_docs.json")


class LarkUtilTestCase(TestCase):
    def setUp(self):
        self.SHEET_TOKEN = config.SHEET_TOKEN
        self.SHEET_RANGE = config.SHEET_RANGE
        self.refresh_token = config.refresh_token
        self.access_token = config.access_token
        lark = Lark(config.APP_ID, config.SECRET)
        self.lark_docs = LarkDocs(
            self.access_token,
            self.refresh_token,
            get_attr=get_attr,
            set_attr=set_attr,
            app_access_token=get_app_access_token(),
            is_lasted=True,
        )

    def test_get_sheet(self):
        response = self.lark_docs.get_sheet_info(config.SHEET_TOKEN)
        self.assertTrue(response)

    def test_get_sheet_by_range(self):
        response = self.lark_docs.get_sheet_by_range(
            config.SHEET_TOKEN, config.SHEET_RANGE
        )
        self.assertTrue(response)

    def test_copy_docs(self):
        copy_data = {
            "type": "sheet",
            "dstFolderToken": config.TEMPLATE_FOLDER_TOKEN,
            "dstName": random_string(),
            "permissionNeeded": False,
            "CommentNeeded": False,
        }
        response = self.lark_docs.copy_docs(config.SHEET_TOKEN, copy_data)
        self.assertTrue(response)
        self.assertTrue(response["folderToken"] == config.TEMPLATE_FOLDER_TOKEN)

    def test_create_permissions(self):
        member = [
            {"member_type": "email", "member_id": config.OTHER_EMAIL, "perm": "view"}
        ]
        response = self.lark_docs.create_permissions(
            config.SHEET_TOKEN, "sheet", member
        )
        self.assertTrue(response["is_all_success"])

    def test_get_folder_children(self):
        response = self.lark_docs.get_folder_children(config.TEMPLATE_FOLDER_TOKEN)
        self.assertTrue("parentToken" in response)

    def test_write_sheet_by_more_range(self):
        response = self.lark_docs.write_sheet_by_more_range(
            config.SHEET_TOKEN,
            [{"range": config.SHEET_ID + "!A1:B2", "values": [[1, 2]],}],
        )
        self.assertTrue(response)

    def test_lock_sheet(self):
        response = self.lark_docs.lock_sheet(config.SHEET_TOKEN, config.SHEET_ID)
        self.assertTrue(response)

    def test_unlock_sheet(self):
        response = self.lark_docs.unlock_sheet(config.SHEET_TOKEN, config.SHEET_ID)
        self.assertTrue(response)

    def test_get_root_folder_metadata(self):
        response = self.lark_docs.get_root_folder_metadata()
        self.assertTrue(response)

    def test_get_sheet_info_by_sheet_id(self):
        response = self.lark_docs.get_sheet_info_by_sheet_id(
            config.SHEET_TOKEN, config.SHEET_ID
        )
        print(response)
        self.assertTrue(response)

    def test_update_sheet_title_by_sheet_id(self):
        response = self.lark_docs.update_sheet_name(
            config.SHEET_TOKEN, config.SHEET_ID, random_string()
        )
        print(response)
        self.assertTrue(response)


if __name__ == "__main__":
    # 生成登录回调链接
    app_id = config.APP_ID
    app_secret = config.SECRET
    lark = Lark(app_id, app_secret)
    print(lark.get_redirect_uri("http://localhost.cn:3000/test"))
    # 访问该链接后需要手动获取 code
    code = input("请输入 code: ")
    userinfo = lark.code2userinfo(code)
    docs_access_token = userinfo["access_token"]
    docs_refresh_token = userinfo["refresh_token"]
    set_config("access_token", docs_access_token, filename="lark_docs.json")
    set_config("refresh_token", docs_refresh_token, filename="lark_docs.json")
