"""
本地微服务之间的调用详细错误提示码
"""


class RPCException(Exception):

    code = 1000

    def __init__(self, err_desc: str = "未知异常"):
        self.err_desc = err_desc


class RPCIvalidPayload(RPCException):
    """ ivalid payload, You sent an invalid payload. """

    code = 4000

    def __init__(self, err_desc: str = "无效请求参数"):
        self.err_desc = err_desc


class RPCInvalidCommand(RPCException):
    """ Invalid command, Invalid command name specified. """

    code = 4002

    def __init__(self, err_desc: str = "无效命令"):
        self.err_desc = err_desc


class RPCInvalidServer(RPCException):
    """ Invalid server, Invalid server ID specified. """

    code = 4003

    def __init__(self, err_desc: str = "无效服务器"):
        self.err_desc = err_desc


class RPCInvalidEvent(RPCException):
    """ Invalid event, Invalid event name specified. """

    code = 4004

    def __init__(self, err_desc: str = "无效事件"):
        self.err_desc = err_desc


class RPCInvalidChannel(RPCException):
    """ Invalid channel, Invalid channel ID specified. """

    code = 4005

    def __init__(self, err_desc: str = "无效频道"):
        self.err_desc = err_desc


class RPCInvalidPermissions(RPCException):
    """ Invalid permissions, You lack permissions to access the given resource. """

    code = 4006

    def __init__(self, err_desc: str = "权限不够"):
        self.err_desc = err_desc


class RPCInvalidClientID(RPCException):
    """ Invalid client ID, An invalid OAuth2 application ID was used to authorize or authenticate with. """

    code = 4007

    def __init__(self, err_desc: str = "无效客户端ID"):
        self.err_desc = err_desc


class RPCInvalidOrigin(RPCException):
    """ Invalid origin, An invalid OAuth2 application origin was used to authorize or authenticate with. """

    code = 4008

    def __init__(self, err_desc: str = "非法应用"):
        self.err_desc = err_desc


class RPCInvalidToken(RPCException):
    """ Invalid token, An invalid OAuth2 token was used to authorize or authenticate with. """

    code = 4009

    def __init__(self, err_desc: str = "验证码错误"):
        self.err_desc = err_desc


class RPCInvalidUser(RPCException):
    """ Invalid user, The specified user ID was invalid. """

    code = 4010

    def __init__(self, err_desc: str = "非法用户"):
        self.err_desc = err_desc


class RPCOAuth2Error(RPCException):
    """OAuth2 error, A standard OAuth2 error occurred; check the data object for the OAuth2 error details. """

    code = 5000

    def __init__(self, err_desc: str = "鉴权错误"):
        self.err_desc = err_desc


class RPCSelectChannelTimeount(RPCException):
    """ Select channel timed out, An asynchronous SELECT_TEXT_CHANNEL/SELECT_VOICE_CHANNEL command timed out. """

    code = 5001

    def __init__(self, err_desc: str = "选择频道超时"):
        self.err_desc = err_desc


class RPCGetServerTimeout(RPCException):
    """ GET_GUILD timed out, An asynchronous GET_GUILD command timed out. """

    code = 5002

    def __init__(self, err_desc: str = "获取服务器超时"):
        self.err_desc = err_desc


class RPCUserWasIn(RPCException):
    """ Select voice force required, You tried to join a user to a voice channel but the user was already in one. """

    code = 5003

    def __init__(self, err_desc: str = "用户已加入"):
        self.err_desc = err_desc


class RPCShortcutListening(RPCException):
    """ Capture shortcut already listening, You tried to capture more than one shortcut key at once. """

    code = 5004

    def __init__(self, err_desc: str = "快捷键已被监听"):
        self.err_desc = err_desc


if __name__ == "__main__":

    try:
        raise RPCShortcutListening()
    except RPCException as err:
        print("异常信息", err.code, err.err_desc)
