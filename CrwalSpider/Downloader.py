import requests

class Downloader(object):
    """url下载器"""

    def capture(self,url):
        # 使用request请求
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/64.0.3282.140 Safari/537.36'
        headers = {'User-Agent': user_agent}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.content.decode()
        else:
            return None
