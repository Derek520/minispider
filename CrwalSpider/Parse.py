import re
from urllib.parse import urljoin
from lxml import etree

class HtmlParse(object):
    """内容解析，使用xpath和re"""
    def __init__(self):
        self._new_url = set()
        self.data = []
        self.deep = 0

    def parse(self,url,html,callback=True):
        # 需要当前页面的返回内容和请求url地址，进行匹配
        if html is None:
            return None
        html  = etree.HTML(html)
        new_url = self.__get_new_url(url,html)
        if callback:
            new_data = self.__get_data(url,html)
        else:
            new_data = None
        return new_url,new_data

    def __get_new_url(self,url,html):
        # 获取该html的新url，加入集合中
        # 此处规则，可以自己定义
        if url is None or html is None:
            return None
        # 获取该页面的所有链接
        a_list = html.xpath('//h4/a[contains(@href,"//book")]/@href')
        # 判断获取的是否为空
        if len(a_list)==0:
            return None
        # 遍历取出a标签
        for a in a_list:
            new_url = urljoin(url,a)
            self._new_url.add(new_url)
        return self._new_url

    def __get_data(self,url,html):
        # 获取页面的有效数据
        if url is None or html is None:
            return None
        # 获取页面内容，规则自定义
        item = {}
        item["url"] = url
        item["title"] = html.xpath('//dd[@class="lemmaWgt-lemmaTitle-title"]/h1/text()')[0]
        list1 = html.xpath('//div[@class="lemma-summary"]/div/text()')
        d = ""
        for content in list1:
            d+=content+'\n'
        item["summary"] =  d

        return item

class Page(object):
    """下一页"""
    pass