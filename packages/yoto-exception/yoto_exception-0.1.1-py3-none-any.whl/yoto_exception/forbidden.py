"""
禁止异常
"""


class ForbiddenException(Exception):

    code = 40000

    def __init__(self, err_desc: str = "非法操作"):
        self.err_desc = err_desc


class ForbiddenUnauthorized(ForbiddenException):
    """ Unauthorized. Provide a valid token and try again """

    code = 40001

    def __init__(self, err_desc: str = "未登陆，请重新登陆"):
        self.err_desc = err_desc


class ForbiddenNeedVerify(ForbiddenException):
    """ You need to verify your account in order to perform this action """

    code = 40002

    def __init__(self, err_desc: str = "账户尚未认证，请前往认证"):
        self.err_desc = err_desc


class ForbiddenRequestEntityTooLarge(ForbiddenException):
    """ Request entity too large. Try sending something smaller in size """

    code = 40005

    def __init__(self, err_desc: str = "请求实体太大"):
        self.err_desc = err_desc


class ForbiddenBeenDisaled(ForbiddenException):
    """ This feature has been temporarily disabled server-side """

    code = 40006

    def __init__(self, err_desc: str = "此功能已在服务器端暂时禁用"):
        self.err_desc = err_desc


class ForbiddenUserIsBanned(ForbiddenException):
    """ The user is banned from this guild """

    code = 40007

    def __init__(self, err_desc: str = "该用户在此服务器被禁止"):
        self.err_desc = err_desc


class ForbiddenBeenCrossposted(ForbiddenException):
    """ This message has already been crossposted """

    code = 40033

    def __init__(self, err_desc: str = "此消息已被交叉发布"):
        self.err_desc = err_desc


if __name__ == "__main__":

    try:
        raise ForbiddenBeenCrossposted()
    except ForbiddenException as err:
        print("异常信息", err.code, err.err_desc)
