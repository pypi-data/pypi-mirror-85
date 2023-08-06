"""
未知实体异常
"""


class UnknownException(Exception):

    code = 10000

    def __init__(self, err_desc: str = "未知实体异常"):
        self.err_desc = err_desc


class UnknownAccount(UnknownException):
    """ Unknown account """

    code = 10001

    def __init__(self, err_desc: str = "未知账号"):
        self.err_desc = err_desc


class UnknownApplication(UnknownException):
    """ Unknown account """

    code = 10002

    def __init__(self, err_desc: str = "未知应用"):
        self.err_desc = err_desc


class UnknownChannel(UnknownException):
    """ Unknown channel """

    code = 10003

    def __init__(self, err_desc: str = "未知频道"):
        self.err_desc = err_desc


class UnknownServer(UnknownException):
    """ Unknown server """

    code = 10004

    def __init__(self, err_desc: str = "未知服务器"):
        self.err_desc = err_desc


class UnknownIntegration(UnknownException):
    """ Unknown integration """

    code = 10005

    def __init__(self, err_desc: str = "未知积分"):
        self.err_desc = err_desc


class UnknownInvite(UnknownException):
    """ Unknown invite """

    code = 10006

    def __init__(self, err_desc: str = "未知邀请"):
        self.err_desc = err_desc


class UnknownMember(UnknownException):
    """ Unknown member """

    code = 10007

    def __init__(self, err_desc: str = "未知成员"):
        self.err_desc = err_desc


class UnknownMessage(UnknownException):
    """ Unknown message """

    code = 10008

    def __init__(self, err_desc: str = "未知消息"):
        self.err_desc = err_desc


class UnknownPermissionOverwrite(UnknownException):
    """ Unknown permission overwrite """

    code = 10009

    def __init__(self, err_desc: str = "未知权限覆盖"):
        self.err_desc = err_desc


class UnknownProvider(UnknownException):
    """ Unknown provider """

    code = 10010

    def __init__(self, err_desc: str = "未知提供者"):
        self.err_desc = err_desc


class UnknownRole(UnknownException):
    """ Unknown role """

    code = 10011

    def __init__(self, err_desc: str = "未知角色"):
        self.err_desc = err_desc


class UnknownToken(UnknownException):
    """ Unknown token """

    code = 10012

    def __init__(self, err_desc: str = "未知token"):
        self.err_desc = err_desc


class UnknownUser(UnknownException):
    """ Unknown user """

    code = 10013

    def __init__(self, err_desc: str = "未知用户"):
        self.err_desc = err_desc


class UnknownEmoji(UnknownException):
    """ Unknown emoji """

    code = 10014

    def __init__(self, err_desc: str = "未知emoji"):
        self.err_desc = err_desc


class UnknownWebhook(UnknownException):
    """ Unknown webhook """

    code = 10015

    def __init__(self, err_desc: str = "未知webhook"):
        self.err_desc = err_desc


class UnknownBan(UnknownException):
    """ Unknown ban """

    code = 10026

    def __init__(self, err_desc: str = "未知禁令"):
        self.err_desc = err_desc


class UnknownSKU(UnknownException):
    """ Unknown SKU """

    code = 10027

    def __init__(self, err_desc: str = "未知SKU"):
        self.err_desc = err_desc


class UnknownStoreListing(UnknownException):
    """ Unknown Store Listing """

    code = 10028

    def __init__(self, err_desc: str = "未知商店列表"):
        self.err_desc = err_desc


class UnknownEntitlement(UnknownException):
    """ Unknown entitlement """

    code = 10029

    def __init__(self, err_desc: str = "未知的权利"):
        self.err_desc = err_desc


class UnknownBuild(UnknownException):
    """ Unknown build """

    code = 10030

    def __init__(self, err_desc: str = "未知版本"):
        self.err_desc = err_desc


class UnknownLobby(UnknownException):
    """ Unknown lobby """

    code = 10031

    def __init__(self, err_desc: str = "未知大厅"):
        self.err_desc = err_desc


class UnknownBranch(UnknownException):
    """ Unknown branch """

    code = 10032

    def __init__(self, err_desc: str = "未知分支"):
        self.err_desc = err_desc


class UnknownRedistributable(UnknownException):
    """ Unknown redistributable """

    code = 10036

    def __init__(self, err_desc: str = "未知的可再发行"):
        self.err_desc = err_desc


class UnknownServerTemplate(UnknownException):
    """ Unknown server template """

    code = 10057

    def __init__(self, err_desc: str = "未知服务器模版"):
        self.err_desc = err_desc


if __name__ == "__main__":

    try:
        raise UnknownServerTemplate()
    except UnknownException as err:
        print("异常信息", err.code, err.err_desc)
