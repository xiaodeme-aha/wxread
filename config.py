# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re

"""
可修改区域
默认使用本地值如果不存在从环境变量中获取值
"""

# 阅读次数 默认120次/60分钟
READ_NUM = int(os.getenv('READ_NUM') or 120)
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
# pushplus推送时需填
PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
# telegram推送时需填
TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
# wxpusher推送时需填
WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = os.getenv('WXREAD_CURL_BASH')

# headers、cookies是一个省略模版，本地或者docker部署时对应替换
cookies = {
    'RK': 'oxEY1bTnXf',
    'ptcz': '46c87074f1768dd4dc9208759f7e1e9b33957a37e075464229f7f2032d89e6ab',
    'pac_uid': '0_G54iGJTxzSd5C',
    'iip': '0',
    '_qimei_uuid42': '052224ffcf4ccad1033b54a40970480d',
    'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPiajxSqBRaEKGGFCck8NbhzIHxiaJ2D1cWpNYGXrb6SYeXuofqfTNvYcsfX9q6USib2ibTQdzT5zUkxfiasN0xq3YsSDZ45SzFzriaLYlKVMlmPuygSRciaDZ2FAg%2F132',
    'wr_gender': '0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=dev-1744284348588,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=fd17cb15d8574cb98065500f86906b86',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
}


"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""
data = {
    "appId": "wb182564874663h706005038",
    "b": "1b5329305cc7881b5f2da82",
    "c": "e3632bd0222e369853df322",
    "ci": 3,
    "co": 350,
    "sm": "受佐伊·安德森(1986—2010)之启",
    "pr": 0,
    "rt": 8,
    "ts": 1744335045757,
    "rn": 84,
    "sg": "4c1cdf503cc9e89444805281f53a594a4a2f1aa27057404222f2be867e3b1833",
    "ct": 1744335045,
    "ps": "339326b07a65a4dfg013798",
    "pc": "531327d07a65a4dfg01641e",
}


def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}
    
    # 从 -H 'Cookie: xxx' 提取
    cookie_header = next((v for k, v in headers_temp.items() 
                         if k.lower() == 'cookie'), '')
    
    # 从 -b 'xxx' 提取
    cookie_b = re.search(r"-b '([^']+)'", curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header
    
    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() 
              if k.lower() != 'cookie'}

    return headers, cookies


headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
