from CrwalSpider.Manger import Scheduler,SchedulerHash
from CrwalSpider.Downloader import Downloader
from CrwalSpider.Parse import HtmlParse
from CrwalSpider.Item import SaveData

class SpiderManger(object):
    """爬虫初始化"""
    def __init__(self):
        # 指纹库
        self.scheduler = SchedulerHash()
        # 下载器
        self.download = Downloader()
        # 解析器
        self.parse = HtmlParse()
        # 数据保存
        self.item = SaveData()

    def run(self,url):
        # 爬虫入口处
        # 1. 将url加入未爬取的队列中
        self.scheduler.add_new_url(url)
        # 2. 爬取的数据量,判断待爬取的队列是否为空，已爬取的队列中是否小于10
        while self.scheduler.not_new_size() and self.scheduler.get_old_size()<100:
            try:
                # 3.如果满足则先获取需要爬取的url
                # TODO 后续添加增量爬虫
                url = self.scheduler.get_new_url()
                # 4.开始爬取页面，返回结果是html页面内容
                html = self.download.capture(url)
                # 5.解析html页面内容
                new_url,new_data = self.parse.parse(url,html,callback=False)
                # 6.将新的url添加到队列中
                self.scheduler.add_new_urls(new_url)
                # 7.添加数据，最后一次输出
                # self.item.add_data(new_data)
                print("爬取url:------{}".format(url))
            except Exception as e:
                self.scheduler.delete(url)
                print("爬取失败url:----{}".format(url))
        # 8.保存输出数据
        # self.item.save()
        # 9.打印成功/失败爬取的数量
        print("成功爬取url:----{}条".format(self.scheduler.get_old_size()))
        print("爬取失败url:----{}条".format(self.scheduler.get_fail_urls()))
        print("带爬取队列任务数量：{}条".format(self.scheduler.get_queue()))

if __name__ == '__main__':
    # url = 'https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711?fr=aladdin'
    url = 'https://www.qidian.com/free/all?orderId=&vip=hidden&pageSize=20&pubflag=0&page=1'
    spider = SpiderManger()
    spider.run(url)

