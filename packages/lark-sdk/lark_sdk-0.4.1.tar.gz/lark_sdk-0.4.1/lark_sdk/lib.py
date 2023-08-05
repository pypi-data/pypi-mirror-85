import json


class LarkRequestError(Exception):
    pass


# coding=utf-8
def pre_request(func):
    def wrapper(self, *args, **kwargs):
        kwargs["headers"] = kwargs.get("headers", {"Content-Type": "application/json"})
        if self.get_access_token() and not kwargs["headers"].get("Authorization"):
            kwargs["headers"]["Authorization"] = "Bearer " + self.get_access_token()
        response = func(self, *args, **kwargs)
        if response.status_code == 200:
            return response.json()
        raise LarkRequestError(response.status_code, response.text)

    return wrapper


# 加打点
def post_request(
    exception, parse_func=lambda response: response["data"], valid_func=None
):
    """对请求结果进行再处理，验证参数是否请求成功（默认为检测 code 是否 为 0），如果不成功则抛出预定的报错，如果为成功，则执行默认的数据处理函数对数据进行在处理。

    Args:
        exception ([type]): [description]
        parse_func ([type], optional): [description]. Defaults to lambda response:response['data'].
        valid_func ([type], optional): [description]. Defaults to lambda response:response['code'] == 0.
    """

    def decorator(func):
        def response_check(response, exception, valid_func=None):
            """检验参数是否正确，默认使用 code = 0, 支持传入一个函数

            Args:
                response (any): 接受的 resposne
                exception (Exception): 出错时抛出的报错

            Raises:
                exception: 定义的报错
            """
            valid_func = (
                valid_func if valid_func else lambda response: response["code"] == 0
            )
            if not valid_func(response):
                raise exception(
                    response["message"]
                    if "message" in response
                    else json.dumps(response)
                )  # 抛出报错信息
            return response

        def wrapper(self, *args, **kwargs):
            response = response_check(
                func(self, *args, **kwargs), exception, valid_func
            )
            return parse_func(response)

        return wrapper

    return decorator
