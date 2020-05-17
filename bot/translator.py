import requests
from config import YANDEX_TOKEN

def trans(text, langs):
    URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    data = {"key": YANDEX_TOKEN,
            "text": text,
            "lang": langs}

    req = eval(requests.post(URL, data=data).text)
    return req['text']
