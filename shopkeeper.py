from load_picture import pictures

'''
shopkeeper:
    pic(pictures):                          图片加载器
    pricetable(dict):                       价目表
'''
class shopkeeper:
    def __init__(self):
        self.pic = pictures()
        self.pricetable = dict()
        with open('AI_Settings\\PriceTable.txt', 'r') as f:
            for line in f:
                if line.strip() != '':
                    if line.strip().split()[0] != 'Name':
                        self.pricetable[line.split()[0]] = list(map(int,line.strip().split()[1:]))
                    else:
                        keys = line.strip().split()[1:]
            f.close()
        for key_0, values in self.pricetable.items():
            tempdict = dict()
            for i in range(len(values)):
                if keys[i] == 'Bullet_Image':
                    if values[i] == 0:
                        tempdict[keys[i]] = self.pic.bullet0
                    if values[i] == 1:
                        tempdict[keys[i]] = self.pic.bullet1
                    if values[i] == 2:
                        tempdict[keys[i]] = self.pic.bullet2
                    if values[i] == 3:
                        tempdict[keys[i]] = self.pic.bullet3
                    if values[i] == 4:
                        tempdict[keys[i]] = self.pic.bullet4
                else:
                    tempdict[keys[i]] = values[i]
            self.pricetable[key_0] = tempdict


if __name__ == '__main__':
    keeper = shopkeeper()
    print(keeper.pricetable)