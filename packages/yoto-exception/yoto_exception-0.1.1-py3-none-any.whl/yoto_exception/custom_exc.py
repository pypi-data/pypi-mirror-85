"""
自定义异常
"""


class PostParamsError(Exception):
    def __init__(self, err_desc: str = "POST请求参数错误"):
        self.err_desc = err_desc


class TokenAuthError(Exception):
    def __init__(self, err_desc: str = "token认证失败"):
        self.err_desc = err_desc


class HttpErrorException(Exception):
    def __init__(self, err_desc: str = "Http请求失败！"):
        self.err_desc = err_desc


class YotoPermissionError(Exception):
    def __init__(self, err_desc: str = "没有操作权限！"):
        self.err_desc = err_desc
