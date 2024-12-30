class shopkeeper:
    def __init__(self):
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
                tempdict[keys[i]] = values[i]
            self.pricetable[key_0] = tempdict


if __name__ == '__main__':
    keeper = shopkeeper()
    print(keeper.pricetable)