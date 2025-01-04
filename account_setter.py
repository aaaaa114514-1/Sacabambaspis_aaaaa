import shutil
import os
import hashlib

'''
account_admin:
    update_resource(username, user_resource):       更新指定用户的account_resource.txt文件
        username(str):                                  用户名
        user_resource(Dict):                            用户的资源数据
    get_resource(username):      -> Dict            获取指定用户的account_resource.txt文件内数据, 输出到Dict中
        username(str):                                  用户名
    clear_all_accounts():                           删除所有用户数据
    remove_account(usename):                        删除指定用户数据
        username(str):                                  用户名
    create_account(username, password):             创建账户
        username(str):                                  用户名
        password(str):                                  密码(未加密)
    is_empty(path):            -> bool              判断指定txt文件是否只有'Dialogue'
        path(str):                                      txt文件路径
    clear_empty_dialogues(username=None)            清除指定用户只有'Dialogue'的txt文件
        username(str):                                  指定的用户(默认为None, 即所有用户)
'''
class account_admin:
    def __init__(self):
        pass

    def hash_data(self, data: str) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        return sha256_hash.hexdigest()

    def update_resource(self, username:str, user_resource:dict):
        with open (f'Text\\Accounts\\{username}\\account_resource.txt', 'w') as f:
            for key in user_resource.keys():
                f.write(f'{key}   \t{user_resource[key]}\n')
        f.close()

    def get_resource(self, username:str):
        user_resource = dict()
        with open(f'Text\\Accounts\\{username}\\account_resource.txt', 'r') as f:
            for line in f:
                user_resource[line.split()[0]] = int(line.split()[1])
        return user_resource

    def clear_all_accounts(self):
        shutil.rmtree('Text\\Accounts')
        os.mkdir('Text\\Accounts')
        open('Text\\Accounts.txt', 'w')

    def remove_account(self, username):
        shutil.rmtree(f'Text\\Accounts\\{username}')
        userinfo = dict()
        with open(f'Text\\Accounts.txt', 'r') as f:
            for line in f:
                if line.split()[0] != username:
                    userinfo[line.split()[0]] = line.split()[1]
        f.close()
        with open (f'Text\\Accounts.txt', 'w') as f:
            for key in userinfo.keys():
                f.write(f'{key}   \t{userinfo[key]}\n')
        f.close()

    def create_account(self, username, password, is_cheater = False):
        f = open(f'Text\Accounts.txt', "a", encoding="UTF-8")
        f.write(f'{username}   \t{self.hash_data(password)}\n')
        f.close()
        os.mkdir(f'Text\\Accounts\\{username}')
        shutil.copy('Text\\account_resource.txt',f'Text\\Accounts\\{username}\\account_resource.txt')
        if is_cheater:
            userinfo = {'Soulstone': 1000, 'has_read0': 0, 'has_read1': 0, 'likeability_Alice': 100, 'likeability_Bob': 100, 'Original_gun': 1, 'Speeding_up': 1, 'Solid_body': 1, 'Magician': 1, 'Soul_gun': 1, 'Firing_gun': 1, 'Infinite_magic': 1, 'Infinite_firepower': -3}
            self.update_resource(username, userinfo)

    def is_empty(self, path):
        with open(path, 'r', encoding="UTF-8") as f:
            if f.read().strip() == 'Dialogue':
                return 1
            else:
                return 0

    def clear_empty_dialogues(self, username = None):
        if username == None:
            for root, dirs, files in os.walk('Text\\Accounts'):
                for file in files:
                    if self.is_empty(os.path.join(root, file)):
                        os.remove(os.path.join(root, file))
        else:
            for root, dirs, files in os.walk(f'Text\\Accounts\\{username}'):
                for file in files:
                    if self.is_empty(os.path.join(root, file)):
                        os.remove(os.path.join(root, file))



if __name__ == '__main__':
    acer0 = account_admin()
    acer0.clear_all_accounts()
    acer0.create_account('aaaaa','',1)
