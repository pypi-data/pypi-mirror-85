"""
连接请求异常
"""


class ConnectionException(Exception):

    code = 90000

    def __init__(self, err_desc: str = "操作不被允许"):
        self.err_desc = err_desc


class ConnectionReactionBlocked(ConnectionException):
    """ Reaction was blocked """

    code = 90001

    def __init__(self, err_desc: str = "响应被阻止"):
        self.err_desc = err_desc


class PermissionResourceOverloaded(ConnectionException):
    """ API resource is currently overloaded. Try again a little later """

    code = 90002

    def __init__(self, err_desc: str = "服务器繁忙，请稍后重试"):
        self.err_desc = err_desc


if __name__ == "__main__":

    try:
        raise PermissionResourceOverloaded()
    except ConnectionException as err:
        print("异常信息", err.code, err.err_desc)
