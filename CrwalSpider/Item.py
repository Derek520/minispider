

class SaveData(object):
    """保存数据"""
    def __init__(self):
        self.datas = []

    def add_data(self,data):
        if data is None:
            return None
        self.datas.append(data)

    def save(self):
        # 保存位置自己可以设置
        if len(self.datas)==0:
            return None
        with open("test.txt", "w") as f:
            for data in self.datas:
                print(data)
                f.write(data["url"] +"\n")
                f.write(data["title"] + "\n")
                f.write(data["summary"] + "\n")



