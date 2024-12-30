import shutil
import os

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
'''
class account_admin:
    def __init__(self):
        pass

    def update_resource(username:str, user_resource:dict):
        with open (f'Text\\Accounts\\{username}\\account_resource.txt', 'w') as f:
            for key in user_resource.keys():
                f.write(f'{key}   \t{user_resource[key]}\n')
        f.close()

    def get_resource(username:str):
        user_resource = dict()
        with open(f'Text\\Accounts\\{username}\\account_resource.txt', 'r') as f:
            for line in f:
                user_resource[line.split()[0]] = int(line.split()[1])
        return user_resource

    def clear_all_accounts():
        shutil.rmtree('Text\\Accounts')
        os.mkdir('Text\\Accounts')
        open('Text\\Accounts.txt', 'w')

    def remove_account(username):
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



if __name__ == '__main__':
    acer0 = account_admin
    acer0.remove_account('33')