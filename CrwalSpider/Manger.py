from CrwalSpider.utils.HashMD5 import HashMD5
from CrwalSpider.utils.RedisDB import Redis_client
from queue import Queue


"""
@作者：Ｄerek
@时间：2018-05-21
@作用：该模块主要实现了url指纹库，去重的效果，处理待爬取url去集合和已爬取url集合
"""
class Scheduler(object):
    """url指纹库
    分为待爬取url和已爬取url
    采用集合url去重
    """
    def __init__(self):

        self.new_urls = set()   # 待爬取url
        self.old_urls = set()   # 已经爬取的url
        self.fail_urls = set()  # 爬取失败的url

    def add_new_url(self,url):
        # 该方法获取新的url进行添加到集合中,单个url，开始url
        if url is None:
            return None
        # 判断是否存在url集合中，满足条件添加到新的url
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self,urls):
        # 该方法是将提取的url放进集合中
        if urls is None:
            return None
        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        # 获取一个url，就要从new_urls删除一个，在old_urls中加一条
        # 集合模式可以自己改
        url = self.new_urls.pop()
        self.old_urls.add(url)
        return url

    def get_new_size(self):
        # 获取待爬取的集合大小
        size = len(self.new_urls)
        return size

    def get_old_size(self):
        # 获取已爬取的集合大小
        size = len(self.old_urls)
        return size

    def not_new_size(self):
        # 判断待爬取的集合中是否为空
        return self.get_new_size() != 0

    def delete(self,url):
        # 删除爬取失败后的url
        self.old_urls.remove(url)
        self.fail_urls.add(url)

    def get_fail_urls(self):
        # 获取失败的url
        return len(self.fail_urls)


class SchedulerHash(object):
    def __init__(self):
        self.redis_store = Redis_client()
        self.new_urls = set()   # 新增url，hase加密后的值
        self.old_urls = set()   # 爬取url，hase加密后的值
        self.fail_urls = set()   # 失败url，地址
        # self.hash = HashMD5()   # hash加密
        # self.new_urls_set = set()   # 这个是未加密的url

    def add_new_url(self,url):
        # 添加新的url,进行md5 hash处理
        if url is None:
            return None
        md5 = HashMD5(url)    # 先进行hash加密处理

        new_urls = self.redis_store.sismember("new_urls",md5)
        old_urls = self.redis_store.sismember("old_urls",md5)
        # if md5 not in new_urls and md5 not in self.old_urls:   # 判断是否存在新增集合和已爬集合列中
        if new_urls or old_urls:
            return None
        # self.new_urls_set.add(url)  # 加入集合中，方便获取url地址,后面放进redis
        self.redis_store.lpush('queue',url)  # 将任务放进有列表中，从前往后添加
        # self.new_urls.add(md5)   # 加入url集合中，方便对比，这个今后会存在redis
        self.redis_store.sadd("new_urls",md5)

    def add_new_urls(self,urls):
        if urls is None:
            return None
        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        # 从集合中获取请求url
        if self.redis_store.llen("queue") !=0:
            # url = self.new_urls_set.pop()
            # 谁先入队，先取谁
            url = self.redis_store.lpop("queue").decode()
            md5 = HashMD5(url)
            # 判断是否已爬取过url，如果爬取过重新获取新的url
            if self.redis_store.sismember("old_urls",md5):
                self.get_new_url()
            # 将没有爬取的url，加入已爬取的集合中f
            self.redis_store.sadd("old_urls",md5)
            # 将已爬取的url，从new_url中删除
            self.redis_store.srem("new_urls",md5)
            return url

    def get_new_size(self):
        # 获取待爬取的集合大小
        size = self.redis_store.scard("new_urls")
        return size

    def get_old_size(self):
        # 获取已爬取的集合大小
        size = self.redis_store.scard("old_urls")
        return size

    def not_new_size(self):
        # 判断待爬取的集合中是否为空
        return self.get_new_size() != 0

    def delete(self,url):
        # 删除爬取失败后的url
        # self.old_urls.remove(url)
        md5 = HashMD5(url)
        self.redis_store.srem("old_urls",md5)
        self.fail_urls.add(url)

    def get_fail_urls(self):
        # 获取失败的url
        return len(self.fail_urls)

    def get_queue(self):
        # 获取队列中的任务数
        return self.redis_store.llen("queue")

if __name__ == '__main__':
    s = SchedulerHash()
    s.add_url("http://wwbdi")
    s.add_urls(["httpsds","yuandsds","dsdsdsdsds"])
    print(s.new_urls)
