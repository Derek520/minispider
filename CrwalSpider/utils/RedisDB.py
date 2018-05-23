import redis

REDIS_URL = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


def Redis_client(REDIS_URL=REDIS_URL,REDIS_PORT=REDIS_PORT,REDIS_DB=REDIS_DB):
    try:
        redis_store = redis.Redis(host=REDIS_URL,port=REDIS_PORT,db=REDIS_DB)
    except Exception as e:
        print("reids数据库连接失败")
    else:
        return redis_store

'https://www.xcxdh666.com/pageList.htm?pageNum=10'

# http://www.wechat-cloud.com/index.php?s=/home/article/ajax_get_list.html&category_id=&page=5&size=20