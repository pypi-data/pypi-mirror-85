from .lark import *


class larkDockError(Exception):
    pass


class larkDocsSearchError(larkDockError):
    pass


class LarkDocs(Lark):
    SPREAD_SHEETS_TEMPLATE = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{SHEET_TOKEN}/values/{RANGE}"
    SHEETS_INFO = (
        "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{SHEET_TOKEN}/metainfo"
    )
    DOCS_CREATE = (
        "https://open.feishu.cn/open-apis/drive/explorer/v2/file/{FOLDER_TOKEN}"
    )
    DOCS_COPY = "https://open.feishu.cn/open-apis/drive/explorer/v2/file/copy/files/{FILE_TOKEN}"
    DOCS_PERMISSION_CREATE = (
        "https://open.feishu.cn/open-apis/drive/permission/member/create"
    )
    FOLDER_CHILDREN = "https://open.feishu.cn/open-apis/drive/explorer/v2/folder/{FOLDER_TOKEN}/children"
    REFRESH_TOKEN = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"

    def __init__(
        self,
        access_token,
        refresh_token=None,
        app_access_token=None,
        is_lasted=True,
        set_attr=None,
        get_attr=None,
    ):
        """初始化 SDK ， 如果需要实现刷新功能 Token 则需要填写 access_token 和 app_access_token，否则无法完成刷新
        https://open.feishu.cn/document/ukTMukTMukTM/uQDO4UjL0gDO14CN4gTN


        Args:
            access_token (str): [description]
            refresh_token (str, optional): [description]. Defaults to None.
            app_access_token (str, optional): 这个token 必须是 使用 code2token 时使用的 token . Defaults to None.
            is_lasted (bool, optional): 是否根据 refresh token 获取最新的 access Token. Defaults to True.
            set_attr (func, optional): 设置类的属性.
            get_attr (func, optional): 获取类的属性.
        """
        self.set_attr = set_attr if set_attr else self.set_attr
        self.get_attr = get_attr if get_attr else self.get_attr
        self.set_attr("access_token", access_token)
        self.set_attr("refresh_token", refresh_token)
        self.set_attr("app_access_token", app_access_token)
        self.set_attr("is_lasted", is_lasted)
        self.set_attr("refreshable", bool(refresh_token or app_access_token))

    def refresh_access_token(self):
        """https://open.feishu.cn/document/ukTMukTMukTM/uQDO4UjL0gDO14CN4gTN

        Raises:
            LarkVaildError: [description]
        """
        if not self.get_attr("refreshable"):
            raise LarkVaildError(u"缺少 refresh_token,app_access_token 无法完成刷新")
        data = self._post_refresh_token(
            {
                "app_access_token": self.get_attr("app_access_token"),
                "grant_type": "refresh_token",
                "refresh_token": self.get_attr("refresh_token"),
            }
        )
        access_token, refresh_token = self.data_parser(
            data, ["access_token", "refresh_token"]
        )
        self.set_attr("access_token", access_token)
        self.set_attr("refresh_token", refresh_token)

    @post_request(larkDockError)
    def _post_refresh_token(self, data):
        return requests.post(self.REFRESH_TOKEN, json=data).json()

    def get_access_token(self):
        if self.get_attr("is_lasted") and self.get_attr("refreshable"):
            self.refresh_access_token()
        return self.get_attr("access_token")

    @post_request(larkDockError)
    def get_sheet_info(self, sheet_token):
        """获取表格元数据

        Args:
            sheet_token (string):

        Returns:
            sheet_info: 表格信息
        {
            "properties": {
                "title": "",
                "ownerUser": 0,
                "sheetCount": 0,
                "revision": 0
            },
            "sheets": [
                {
                    "sheetId": "***",
                    "title": "***",
                    "index": 0,
                    "rowCount": 0,
                    "columnCount": 0
                }
            ],
            "spreadsheetToken": "***"
        }

        """
        url = self.SHEETS_INFO.format(**{"SHEET_TOKEN": sheet_token,})
        return self.get(url)

    def get_sheet_info_by_sheet_id(self, sheet_token, sheet_id):
        """获取指定子表的信息 如果没有找到则会返回 None 类型

        Args:
            sheet_token (str): 表的 Token
            sheet_id (str): 子表名

        Returns:
            sheets: {
                    "sheetId": "***",
                    "title": "***",
                    "index": 0,
                    "rowCount": 0,
                    "columnCount": 0
                }
        """
        sheets_info = self.get_sheet_info(sheet_token)
        # 获取符合要求的 sheet
        goal_sheets = list(
            filter(lambda x: x["sheetId"] == sheet_id, sheets_info["sheets"])
        )
        return goal_sheets.pop() if goal_sheets else None

    @post_request(larkDockError)
    def create_docs(self, folder_token, title, docs_type="sheet"):
        """创建文档

        Args:
            folder_token (string): folder 的 token
            title (title): 文档的 Title
            docs_type (string, optional): 文件的类型. Defaults to "sheet".

        Returns:
            fileinfo: 文档的信息

        {
            "revision":0,
            "token":"string",
            "url":"string"
        }
        """
        url = DOCS_CREATE.format(**{"FOLDER_TOKEN": folder_token})
        return self.post(url, json={"title": title, "type": docs_type})

    @post_request(larkDockError)
    def copy_docs(self, file_token, docs_info):
        """对文档进行 copy
        https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uYTNzUjL2UzM14iN1MTN

        Args:
            file_token ([type]): file_token
            docs_info ([type]): 文档信息

                {
                    "type":"sheet",
                    "dstFolderToken":"string",
                    "dstName":"string",
                    "permissionNeeded":true,
                    "CommentNeeded":true
                }
        """
        url = self.DOCS_COPY.format(**{"FILE_TOKEN": file_token})
        return self.post(url, json=docs_info)

    @post_request(larkDockError)
    # WARAING: 无法授权给自己
    def create_permissions(self, file_token, docs_type, member):
        """给指定文件增加 权限

        Args:
            file_token (string): 文件的 token
            docs_type (string): 文件的类型
            member (string): 成员信息
                [
                    {
                        "member_type": "openid",
                        "member_id": "string",
                        "perm": "view"
                    }
                ]

        Returns:
            permissions: 权限信息

                "is_all_success": true,
                "fail_members": [
                    {
                        "member_type": "openid",
                        "member_id": "string",
                        "perm": "view"
                    }
                ]
        """
        return self.post(
            self.DOCS_PERMISSION_CREATE,
            json={"token": file_token, "type": docs_type, "members": member},
        )

    @post_request(larkDockError)
    def get_folder_children(self, folder_token, file_types=["sheet"]):
        """获取文件夹下的文档信息

        Args:
            folder_token (string)): 文件夹 Token
            file_types (list, optional): 文件种类可多选. Defaults to [].

        Returns:

            fils_infos: 文件信息
                {
                    "parentToken": "token",
                    "children": {
                        "lq3xxxxxwLfExB23": { //文件 token
                            "token": "lq3xxxxxwLfExB23",
                            "name": "test_folder_name",
                            "type": "folder",
                    },
                            "lq3xxxxxddddB24": { //文件 token
                                    "token": "lq3xxxxxddddB24",
                                    "name": "test_sheet_name",
                                    "type": "sheet",
                                }
                    }
                }
        """
        url = (
            self.FOLDER_CHILDREN.format(**{"FOLDER_TOKEN": folder_token})
            + "?"
            + "&".join(["type=" + file_type for file_type in file_types])
        )
        return self.get(url)

    @post_request(
        larkDockError,
        parse_func=lambda response: response["data"]["valueRange"]["values"],
    )
    def get_sheet_by_range(self, sheet_token, sheet_range):
        """获取指定的表格信息
        https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/ugTMzUjL4EzM14COxMTN
        Args:
            sheet_token (string): sheet_token
            sheet_range (string): rage

        Raises:
            larkDocsSearchError: 获取失败

        Returns:
            sheetinfo: 获取到的表格信息

        """
        url = self.SPREAD_SHEETS_TEMPLATE.format(
            **{"SHEET_TOKEN": sheet_token, "RANGE": sheet_range,}
        )
        return self.get(url)

    @post_request(larkDockError)
    def write_sheet_by_range(self, sheet_token, sheet_range, value):
        url = self.SPREAD_SHEETS_TEMPLATE.format(
            **{"SHEET_TOKEN": sheet_token, "RANGE": "",}
        )
        return self.put(
            url, json={"valueRange": {"range": sheet_range, "values": value,}}
        )

    @post_request(larkDockError)
    def write_sheet_by_more_range(self, sheet_token, valueRanges):
        """向多个范围写入数据
        https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uEjMzUjLxIzM14SMyMTN

        Args:
            sheet_token (str): 表格的 token
            valueRanges ([type]): [description]

            values: 
                "valueRanges": [
                    {
                    "range": "range1",
                    "values": [
                        [
                        "string1", 1, "http://www.xx.com"
                        ]
                    ]
                    },
                    {
                    "range": "range2",
                    "values": [
                        [
                        "string2", 2, "http://www.xx.com"
                        ]
                    ]
                    }
                ]

        Returns:


            "responses": [
                {
                    "spreadsheetToken": "***",
                    "updatedCells": 0,
                    "updatedColumns": 0,
                    "updatedRange": "***",
                    "updatedRows": 0
                },
                {
                    "spreadsheetToken": "***",
                    "updatedCells": 0,
                    "updatedColumns": 0,
                    "updatedRange": "***",
                    "updatedRows": 0
                }
            ],
            "revision": 0,
            "spreadsheetToken": "***"
        """
        url = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{}/values_batch_update".format(
            sheet_token
        )
        return self.post(url, json={"valueRanges": valueRanges})

    @post_request(larkDockError)
    def lock_sheet(self, sheet_token, sheet_id, lock_info="Locked"):
        """锁定指定单元格

        Args:
            sheet_token (str): sheet_token
            sheet_id (str): sheet_id 子表的 id
            lock_info (str, optional):锁定的信息. Defaults to "Locked".
        """
        url = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{}/sheets_batch_update".format(
            sheet_token
        )
        return self.post(
            url,
            json={
                "requests": [
                    {
                        "updateSheet": {
                            "properties": {
                                "sheetId": sheet_id,
                                "protect": {"lock": "LOCK", "lockInfo": lock_info,},
                            }
                        }
                    }
                ]
            },
        )

    @post_request(larkDockError)
    def unlock_sheet(self, sheet_token, sheet_id):
        """解锁指定单元格

        Args:
            sheet_token (str): sheet_token
            sheet_id (str): sheet_id 子表的 id
        """
        url = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{}/sheets_batch_update".format(
            sheet_token
        )
        return self.post(
            url,
            json={
                "requests": [
                    {
                        "updateSheet": {
                            "properties": {
                                "sheetId": sheet_id,
                                "protect": {"lock": "UNLOCK",},
                            }
                        }
                    }
                ]
            },
        )

    @post_request(larkDockError)
    def update_sheet_name(self, sheet_token, sheet_id, sheet_title):
        """更改子表的名字 注意重名的 sheets 会报错失败

        Args:
            sheet_token (str): sheet_token
            sheet_id (str): sheet_id 子表的 id
            sheet_title (str): 要修改的子表名字
        """
        url = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{}/sheets_batch_update".format(
            sheet_token
        )
        return self.post(
            url,
            json={
                "requests": [
                    {
                        "updateSheet": {
                            "properties": {"sheetId": sheet_id, "title": sheet_title}
                        }
                    }
                ]
            },
        )

    @post_request(larkDockError)
    def get_root_folder_metadata(self):
        """获取 "我的空间" 的元信息
        https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uAjNzUjLwYzM14CM2MTN

        Returns:
            "data": {
                "token": "string",
                "id": "folderId",
                "user_id": "userId"
            }
        """
        url = "https://open.feishu.cn/open-apis/drive/explorer/v2/root_folder/meta"
        return self.get(url)
