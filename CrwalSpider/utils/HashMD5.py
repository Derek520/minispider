from hashlib import md5,sha1
import hashlib

# class HashMD5(object):
#     def __init__(self):
#         self.md5 = md5()
#         self.sha1 = sha1()  #sha1加密

def update(url):
    # md5加密１２８长度,加盐
    m = hashlib.updata(url.encode("utf-8"))
    return m.hexdigest()

def HashMD5(url):
    # md5加密，每一条加密
    m =  hashlib.md5(url.encode('utf-8'))
    return m.hexdigest()



def SHA_ONE(url):
    # sha1加密１６０长度
    self.sha1.update(url.encode("utf-8"))

def get_md5(self):
    return self.md5.hexdigest()

def get_sha():
    return self.sha1.hexdigest()


if __name__ == '__main__':

    print(HashMD5('SDSDSD'))
    print(HashMD5('SDSDSD'))
    print(HashMD5('DSASDADA'))

