"""
超过数量上限异常
"""


class MaximumException(Exception):

    code = 30000

    def __init__(self, err_desc: str = "超过数量上限异常"):
        self.err_desc = err_desc


class MaximumNumberOfServer(MaximumException):
    """ Maximum number of guilds reached (100) """

    code = 30001

    def __init__(self, err_desc: str = "超过服务器数量上限"):
        self.err_desc = err_desc


class MaximumNumberOfFriends(MaximumException):
    """ Maximum number of friends reached (1000) """

    code = 30002

    def __init__(self, err_desc: str = "超过好友数量上限"):
        self.err_desc = err_desc


class MaximumNumberOfPin(MaximumException):
    """ Maximum number of pins reached for the channel (50) """

    code = 30003

    def __init__(self, err_desc: str = "超过频道pin数量上限"):
        self.err_desc = err_desc


class MaximumNumberOfServerRoles(MaximumException):
    """ Maximum number of guild roles reached (250) """

    code = 30005

    def __init__(self, err_desc: str = "超过服务器角色数量上限"):
        self.err_desc = err_desc


class MaximumNumberOfWebhooks(MaximumException):
    """ Maximum number of webhooks reached (10) """

    code = 30007

    def __init__(self, err_desc: str = "超过webhook数量上限"):
        self.err_desc = err_desc


class MaximumNumberOfReactions(MaximumException):
    """ Maximum number of reactions reached (20) """

    code = 30010

    def __init__(self, err_desc: str = "超过reaction数量上限"):
        self.err_desc = err_desc


class MaximumNumberOfServerChannels(MaximumException):
    """ Maximum number of guild channels reached (500) """

    code = 30013

    def __init__(self, err_desc: str = "超过服务器频道数量上限"):
        self.err_desc = err_desc


class MaximumNumberOfAttachments(MaximumException):
    """ Maximum number of attachments in a message reached (10) """

    code = 30015

    def __init__(self, err_desc: str = "超过消息附件数量上限"):
        self.err_desc = err_desc


class MaximumNumberOfInvites(MaximumException):
    """ Maximum number of invites reached (1000) """

    code = 30016

    def __init__(self, err_desc: str = "超过邀请数量上限"):
        self.err_desc = err_desc


if __name__ == "__main__":

    try:
        raise MaximumNumberOfInvites()
    except MaximumException as err:
        print("异常信息", err.code, err.err_desc)
