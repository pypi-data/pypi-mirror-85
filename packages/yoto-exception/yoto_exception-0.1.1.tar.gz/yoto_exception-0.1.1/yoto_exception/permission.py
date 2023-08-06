"""
允许异常
"""


class PermissionException(Exception):

    code = 20000

    def __init__(self, err_desc: str = "操作不被允许"):
        self.err_desc = err_desc


class PermissionBotsCannotUseEndpoint(PermissionException):
    """ Bots cannot use this endpoint """

    code = 20001

    def __init__(self, err_desc: str = "机器人无法使用此端点"):
        self.err_desc = err_desc

	
class PermissionOnlyBotsCanUseEndpoint(PermissionException):
    """ Only bots can use this endpoint """

    code = 20002

    def __init__(self, err_desc: str = "只有机器人可以使用此端点"):
        self.err_desc = err_desc

		

class PermissionMessageEditDueToRateLimits(PermissionException):
    """ This message cannot be edited due to announcement rate limits """

    code = 20022

    def __init__(self, err_desc: str = "由于播报率限制，无法编辑此消息"):
        self.err_desc = err_desc

	
class PermissionChannelWriteRateLimit(PermissionException):
    """ The channel you are writing has hit the write rate limit """

    code = 20028

    def __init__(self, err_desc: str = "达到频道的写入速率限制"):
        self.err_desc = err_desc


if __name__ == "__main__":

    try:
        raise PermissionChannelWriteRateLimit()
    except PermissionException as err:
        print("异常信息", err.code, err.err_desc)
