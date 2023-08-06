from django.conf import settings
from request_sign.utils import handle_pass_list

__all__ = ['ENABLE_REQUEST_SIGNATURE', 'SIGNATURE_SECRET', 'SIGNATURE_ALLOW_TIME_ERROR', 'SIGNATURE_RESPONSE',
           'SIGNATURE_PASS_URL', 'SIGNATURE_PASS_URL_NAME', 'SIGNATURE_PASS_URL_REGULAR', 'SIGNATURE_METHOD',
           'NONCE_CACHE_KEY']

TEST = False

http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

ENABLE_REQUEST_SIGNATURE = settings.ENABLE_REQUEST_SIGNATURE if \
    not TEST and \
    hasattr(settings, 'ENABLE_REQUEST_SIGNATURE') else False  # 开启签名校检

SIGNATURE_SECRET = settings.SIGNATURE_SECRET if \
    not TEST and \
    hasattr(settings, 'SIGNATURE_SECRET') else None  # 私钥

SIGNATURE_ALLOW_TIME_ERROR = settings.SIGNATURE_ALLOW_TIME_ERROR if \
    not TEST and \
    hasattr(settings, 'SIGNATURE_ALLOW_TIME_ERROR') else 600  # 允许时间误差

SIGNATURE_RESPONSE = settings.SIGNATURE_RESPONSE if \
    not TEST and \
    hasattr(settings, 'SIGNATURE_RESPONSE') else 'request_sign.utils.default_response'  # 签名不通过返回方法

SIGNATURE_PASS_URL = settings.SIGNATURE_PASS_URL if \
    not TEST and \
    hasattr(settings, 'SIGNATURE_PASS_URL') else []  # 不效验签名的url

SIGNATURE_PASS_URL_NAME = handle_pass_list(settings.SIGNATURE_PASS_URL_NAME) if \
    not TEST and \
    hasattr(settings, 'SIGNATURE_PASS_URL_NAME') else []  # 不效验签名的url,传入django的url name字段

SIGNATURE_PASS_URL_REGULAR = settings.SIGNATURE_PASS_URL_REGULAR if \
    not TEST and \
    hasattr(settings, 'SIGNATURE_PASS_URL_REGULAR') else []  # 不效验签名url正则

SIGNATURE_METHOD = settings.SIGNATURE_METHOD if \
    not TEST and \
    hasattr(settings, 'SIGNATURE_METHOD') else http_method_names  # 检查的请求类型，默认全部检查
NONCE_CACHE_KEY = settings.NONCE_CACHE_KEY if \
    not TEST and \
    hasattr(settings, 'NONCE_CACHE_KEY') else "django_request_sign_nonce_{nonce}"  # 检查的请求类型，默认全部检查
