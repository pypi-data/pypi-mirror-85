"""
权限异常
"""


class AuthException(Exception):

    code = 50000

    def __init__(self, err_desc: str = "您无权进行此操作"):
        self.err_desc = err_desc


class AuthMissingAccess(AuthException):
    """ Missing access """

    code = 50001

    def __init__(self, err_desc: str = "缺少访问权限"):
        self.err_desc = err_desc


class AuthNeedInvalidAccountType(AuthException):
    """ Invalid account type """

    code = 50002

    def __init__(self, err_desc: str = "无效账号类型"):
        self.err_desc = err_desc


class AuthCannotExecuteAction(AuthException):
    """ Cannot execute action on a DM channel """

    code = 50003

    def __init__(self, err_desc: str = "不能在DM频道执行操作"):
        self.err_desc = err_desc


class AuthGuildWidgetDisabled(AuthException):
    """ Guild widget disabled """

    code = 50004

    def __init__(self, err_desc: str = "服务器部件不可用"):
        self.err_desc = err_desc


class AuthSendByAnotherUser(AuthException):
    """ Cannot edit a message authored by another user """

    code = 50005

    def __init__(self, err_desc: str = "不能编辑其他用户发送的消息"):
        self.err_desc = err_desc


class AuthEmptyMessage(AuthException):
    """ Cannot send an empty message """

    code = 50006

    def __init__(self, err_desc: str = "不能发送空消息"):
        self.err_desc = err_desc


class AuthUnacceptableUser(AuthException):
    """ Cannot send messages to this user """

    code = 50007

    def __init__(self, err_desc: str = "不能给该用户发送消息"):
        self.err_desc = err_desc


class AuthCannotSendInVoiceChannel(AuthException):
    """ Cannot send messages in a voice channel """

    code = 50008

    def __init__(self, err_desc: str = "不能在语音频道发消息"):
        self.err_desc = err_desc


class AuthCVLIsTooHigh(AuthException):
    """ Channel verification level is too high for you to gain access """

    code = 50009

    def __init__(self, err_desc: str = "频道验证级别过高，您无法获得访问权限"):
        self.err_desc = err_desc


class AuthOAuth2HasNoBot(AuthException):
    """ OAuth2 application does not have a bot """

    code = 50010

    def __init__(self, err_desc: str = "OAuth2应用没有机器人"):
        self.err_desc = err_desc


class AuthOAuth2Limit(AuthException):
    """ OAuth2 application limit reached """

    code = 50011

    def __init__(self, err_desc: str = "达到OAuth2应用限制"):
        self.err_desc = err_desc


class AuthInvalidOAuth2State(AuthException):
    """ Invalid OAuth2 state """

    code = 50012

    def __init__(self, err_desc: str = "无效OAuth2状态"):
        self.err_desc = err_desc


class AuthLackPermissions(AuthException):
    """ You lack permissions to perform that action """

    code = 50013

    def __init__(self, err_desc: str = "您没有执行该操作的权限"):
        self.err_desc = err_desc


class AuthInvalidToken(AuthException):
    """ Invalid authentication token provided """

    code = 50014

    def __init__(self, err_desc: str = "提供了无效的认证令牌"):
        self.err_desc = err_desc


class AuthNoteTooLong(AuthException):
    """ Note was too long """

    code = 50015

    def __init__(self, err_desc: str = "提示过长"):
        self.err_desc = err_desc


class AuthDeleteOutOfLimit(AuthException):
    """ Provided too few or too many messages to delete. Must provide at least 2 and fewer than 100 messages to delete """

    code = 50016

    def __init__(self, err_desc: str = "需要删除的消息超出取值范围"):
        self.err_desc = err_desc


class AuthOnlyPinInSendChannel(AuthException):
    """ A message can only be pinned to the channel it was sent in """

    code = 50019

    def __init__(self, err_desc: str = "消息只能在发送频道被PIN"):
        self.err_desc = err_desc


class AuthInvalidInviteCode(AuthException):
    """ Invite code was either invalid or taken """

    code = 50020

    def __init__(self, err_desc: str = "邀请链接无效或已被使用"):
        self.err_desc = err_desc


class AuthSysMsgInvalidAction(AuthException):
    """ Cannot execute action on a system message """

    code = 50021

    def __init__(self, err_desc: str = "无法对系统消息执行操作"):
        self.err_desc = err_desc


class AuthInvalidActionOnChannelType(AuthException):
    """ Cannot execute action on this channel type """

    code = 50024

    def __init__(self, err_desc: str = "无法对该频道类型执行操作"):
        self.err_desc = err_desc


class AuthInvalidOAuth2Token(AuthException):
    """ Invalid OAuth2 access token provided """

    code = 50025

    def __init__(self, err_desc: str = "提供了无效的OAuth2访问令牌"):
        self.err_desc = err_desc


class AuthInvalidRecipient(AuthException):
    """ Invalid Recipient(s) """

    code = 50033

    def __init__(self, err_desc: str = "收件人无效"):
        self.err_desc = err_desc


class AuthDeleteMsgTooOld(AuthException):
    """ A message provided was too old to bulk delete """

    code = 50034

    def __init__(self, err_desc: str = "提供的消息太旧，无法批量删除"):
        self.err_desc = err_desc


class AuthInvalidRequest(AuthException):
    """ Invalid form body (returned for both application/json and multipart/form-data bodies), or invalid Content-Type provided """

    code = 50035

    def __init__(self, err_desc: str = "无效的表单主体，或提供的Content-Type无效"):
        self.err_desc = err_desc


class AuthBotIsUnacceptable(AuthException):
    """ An invite was accepted to a guild the application's bot is not in """

    code = 50036

    def __init__(self, err_desc: str = "邀请被接受加入服务器的应用程序的机器人不在"):
        self.err_desc = err_desc


class AuthInvalidAPIVersion(AuthException):
    """ Invalid API version provided """

    code = 50041

    def __init__(self, err_desc: str = "无效API版本"):
        self.err_desc = err_desc


class AuthForbiddenDeleteChannel(AuthException):
    """ Cannot delete a channel required for Community guilds """

    code = 50074

    def __init__(self, err_desc: str = "无法删除社区服务器所需的频道"):
        self.err_desc = err_desc


if __name__ == "__main__":

    try:
        raise AuthForbiddenDeleteChannel()
    except AuthException as err:
        print("异常信息", err.code, err.err_desc)
