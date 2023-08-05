# TODO: 这里可以优化一下 不能全依赖过来
from .lark import *


class LarkRecallError(LarkError):
    pass


class LarkSender(Lark):
    """用于 Lark 的 各种消息发送
    https://open.feishu.cn/document/ukTMukTMukTM/ucDO1EjL3gTNx4yN4UTM
    """

    REVEIVERS_KINDS = ["open_id", "email", "chat_id", "user_id", "open_ids"]
    SEND_MESSAGE_URL = "https://open.feishu.cn/open-apis/message/v4/send/"
    RECALL_URL = "https://open.feishu.cn/open-apis/message/v4/recall/"
    READ_INFO_URL = "https://open.feishu.cn/open-apis/message/v4/read_info/"
    URGENT_URL = "https://open.feishu.cn/open-apis/message/v4/urgent/"

    def __init__(self, app_id, secret, receiver, root_id=None):
        super(LarkSender, self).__init__(app_id, secret)
        self.receiver = receiver
        self.root_id = root_id

    def genrate_msg(self, msg_type):
        # 复制一份防止修改原数据
        pre_msg_body = dict(**self.receiver)
        for key in self.receiver:
            # 去掉不合法的参数
            if key not in self.REVEIVERS_KINDS:
                del pre_msg_body[key]
        if self.root_id:
            pre_msg_body["root_id"] = self.root_id
        pre_msg_body["msg_type"] = msg_type
        return pre_msg_body

    def send_message(self, *args, **kwargs):
        return self.post(self.SEND_MESSAGE_URL, *args, **kwargs)

    @post_request(LarkRequestError)
    def send_text(self, message):
        """发送文本消息
        https://open.feishu.cn/document/ukTMukTMukTM/uUjNz4SN2MjL1YzM
        Args:
            message (text): 消息的内容

        Returns:
            message: 返回消息的 message_id

            {
                "message_id":str
            }
        """
        msg_body = self.genrate_msg("text")
        msg_body["content"] = {"text": message}
        return self.send_message(json=msg_body)

    @post_request(LarkRequestError)
    def send_post(self, title, content, language="zh_cn"):
        """发送富文本消息
        https://open.feishu.cn/document/ukTMukTMukTM/uMDMxEjLzATMx4yMwETM
        Args:
            title (str): 消息的 title
            content (str): 消息的正文
            language (str, optional): 语言类型，目前只支持同时发送一种，可选 ja_jp,en_us. Defaults to "zh_cn".
        
        Returns:
            message: 返回消息的 message_id

            {
                "message_id":str
            }
        """
        msg_body = self.genrate_msg("post")
        msg_body["content"] = {"post": {language: {"title": title, "content": content}}}
        return self.send_message(json=msg_body)

    @post_request(LarkRecallError, parse_func=lambda response: response)
    def recall_message(self, message_id):
        """撤回消息，注意必须要发送时长小于 24 h
        https://open.feishu.cn/open-apis/message/v4/recall/
        Args:
            message_id (str): 发送的消息 ID 

        Returns:
            response: 撤回结果

        {
            code:number
            msg:str
        }
        """
        return self.post(self.RECALL_URL, json={"message_id": message_id})

    @post_request(LarkRequestError)
    def read_info(self, message_id):
        """ 查看消息的已读情况 返回所有已读的消息列表

        Args:
            message_id (str): 消息的 message_id ID

        Returns:
            user_list: 已读的用户

            "read_users": [
                {
                    "open_id": "ou_18eac85d35a26f989317ad4f02e8bbbb",
                    "timestamp": "1570697776",
                    "user_id": "ca51d83b"
                }
            ]
        """
        return self.post(self.READ_INFO_URL, json={"message_id": message_id})

    @post_request(
        LarkRequestError,
        parse_func=lambda response: response["invalid_open_ids"]
        if "invalid_open_ids" in response
        else response,
    )
    def urgent(self, message_id, urgent_type="app"):
        """加急消息 需要额外申请权限

        https://open.feishu.cn/open-apis/message/v4/urgent/

        Args:
            message_id (str): 消息的 id
            urgent_type (str, optional): 加急的类型 应用内加急（app），短信加急（sms），电话加急（phone）。加急权限需要申请。. Defaults to "app".
        
        Returns:

            user_list: 用户列表
            [
                "ou_uj98af65g7910044998k064t3ghib90g"
            ]
        """
        open_ids = self.receiver.get("open_ids")
        if not open_ids:
            raise LarkvalueError("open_ids is None！")
        return self.post(
            self.URGENT_URL,
            json={
                "message_id": message_id,
                "urgent_type": urgent_type,
                "open_ids": open_ids,
            },
        )

    def send_card(self, card, update_multi=False):
        """发送卡片消息
        https://open.feishu.cn/document/ukTMukTMukTM/uYTNwUjL2UDM14iN1ATN
        
        Args:
            card (card): 要发送的卡片消息，详细数据结构请参考文档
            update_multi (bool, optional): 控制卡片是否是共享卡片(所有用户共享同一张消息卡片). Defaults to False.

        Returns:
            message_id: 消息 ID

            {
                "message_id": "om_92eb70a7120ga8c3ca56a12ee9ba7ca2"
            }
        """
        msg_body = self.genrate_msg("interactive")
        msg_body["update_multi"] = update_multi
        msg_body["card"] = card
        return self.send_message(msg_body)
