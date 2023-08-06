"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/14 4:39 下午
"""
import re
import hashlib

from datetime import datetime
from urllib.parse import unquote

from django.core.cache import cache

from request_sign.utils import try_safe_eval
from request_sign.settings import SIGNATURE_SECRET, SIGNATURE_ALLOW_TIME_ERROR, NONCE_CACHE_KEY, SIGNATURE_PASS_URL, \
    SIGNATURE_PASS_URL_NAME, SIGNATURE_PASS_URL_REGULAR

KEY_MAP = {
    'True': 'true',
    'False': 'false',
    'None': None
}

DELETE_KEY_MAP = ['[]', '{}', [], {}, None]


def signature_parameters(parameters):
    # 列表生成式，生成key=value格式
    parameters_list = ["".join(map(str, i)) for i in parameters.items() if i[1] and i[0] != "sign"]
    # 参数名ASCII码从小到大排序
    sort_parameters = "".join(sorted(parameters_list))
    # 在strA后面拼接上SIGNATURE_SECRET得到signature_str字符串
    signature_str = sort_parameters + SIGNATURE_SECRET
    # MD5加密
    m = hashlib.md5()
    m.update(signature_str.lower().encode('UTF-8'))
    return m.hexdigest()


def check_pass_url_regular(path):
    for r in SIGNATURE_PASS_URL_REGULAR:
        if re.search(r, path):
            return True

    return False


def check_signature(request):
    # pass list
    if request.path in SIGNATURE_PASS_URL or request.path in SIGNATURE_PASS_URL_NAME or \
            check_pass_url_regular(request.path):
        return True

    timestamp = request.META.get("HTTP_TIMESTAMP")
    nonce = request.META.get("HTTP_NONCE")
    sign = request.META.get("HTTP_SIGN")

    # 判断cache是否正常
    if hasattr(cache, 'get') and hasattr(cache, 'set'):
        if cache.get(NONCE_CACHE_KEY.format(nonce=nonce)):
            return False
        else:
            cache.set(NONCE_CACHE_KEY.format(nonce=nonce), True, SIGNATURE_ALLOW_TIME_ERROR)

    if not all([timestamp, nonce, sign]):
        return False

    try:
        timestamp = float(timestamp)
    except:
        raise ValueError('timestamp must be int or float')

    now_timestamp = datetime.now().timestamp()
    if (now_timestamp - SIGNATURE_ALLOW_TIME_ERROR) > timestamp or timestamp > (
            now_timestamp + SIGNATURE_ALLOW_TIME_ERROR):
        return False

    parameters = {
        'nonce': nonce
    }
    get_parameters = request.GET.urlencode()
    post_parameters = request.POST.urlencode()
    body_parameters = str(request.body, encoding='utf-8')
    parameters = handle_parameter(parameters, get_parameters,
                                  post_parameters, body_parameters)
    return sign == signature_parameters(parameters)


def handle_parameter(parameters, get_parameters, post_parameters, body_parameters):
    for parameter in ("&".join([get_parameters, post_parameters, body_parameters])).split('&'):
        if parameter:
            parameter = try_safe_eval(parameter)
            if isinstance(parameter, dict):
                # 遍历字典，对value进行url解码
                parameters = dict(parameters,
                                  **dict(zip(
                                      parameter.keys(),
                                      map(lambda x: KEY_MAP.get(str(x))
                                      if str(x) in KEY_MAP else
                                      unquote(str(x)).replace('+', ' '),
                                          parameter.values()))
                                  ))

                # 删除字典中空参数
                for p in list(parameters.keys()):
                    p_value = try_safe_eval(parameters[p])
                    if (not isinstance(p_value, bool) and (not p_value or len(p_value)) == 0) or \
                            p_value in DELETE_KEY_MAP:
                        del parameters[p]

            else:
                if len(str(parameter).split('=')) == 2:
                    key, value = str(parameter).split('=')
                    if key not in parameters:
                        # 解码并去除空格
                        parameters[key] = unquote(value).replace('+', ' ')
    return parameters
