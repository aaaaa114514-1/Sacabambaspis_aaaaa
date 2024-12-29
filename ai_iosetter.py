from openai import OpenAI
from typing import List, Dict
from datetime import datetime
from account_setter import account_admin

'''
npc_dia:
    nowtime(str):               对话时间
    name(str):                  npc的名字
    username(str):              用户名
    client(OpenAI):             npc的控制AI
    cli_messages([Dict]):       npc与用户的对话(含初始系统设置)
    judge(OpenAI):              判断者AI
    jud_setting(Dict):          判断者设置
    acer(<account_admin>):      账户操作助手
    user_resource(Dict):        用户数据
    likability(int):            好感度(1~100)

    talk(user_input):  -> str       与AI对话, 返回AI的回答, 并将记录通过write_in方法写入文件
        user_input(str)                 用户的输入
    write_in(name, content):        写入文件"Text\\Accounts\\{self.username}\\Dialogue_with_{name}_{nowtime}.txt"
        name(str):                      说话者的名字
        content(str):                   某个人的话
'''

class npc_dia:
    def __init__(self, name:str, username:str):
        self.username = username
        self.nowtime = datetime.now().strftime('%Y%m%d_%H%M%S')
        f = open(f"Text\\Accounts\\{self.username}\\Dialogue_with_{name}_{self.nowtime}.txt", "a", encoding="UTF-8")
        with open(f"Text\\Accounts\\{self.username}\\Dialogue_with_{name}_{self.nowtime}.txt", 'w') as file:
            pass
        f.write("Dialogue\n\n")
        f.close()
        self.name = name
        self.client = OpenAI(
            base_url = 'http://10.15.88.73:5016/v1',
            api_key = 'ollama',
        )
        with open(f'AI_Settings\\{name}.txt', 'r') as file:
            cli_settings = file.read()
        self.cli_messages : List[Dict] = [{"role": "system", "content": cli_settings}]

        self.judge = OpenAI(
            base_url = 'http://10.15.88.73:5016/v1',
            api_key = 'ollama',
        )
        with open(f'AI_Settings\\{name}_judge.txt', 'r') as file:
            jud_settings = file.read()
        self.jud_setting =  {"role": "system", "content": jud_settings}
        self.acer = account_admin
        self.user_resource = self.acer.get_resource(self.username)
        self.likability = int(self.user_resource[f'likability_{self.name}'])


    def talk(self, user_input:str):
        self.cli_messages.append({"role": "user", "content": user_input+f'\nLikability = {self.likability}'})
        response = self.client.chat.completions.create(
            model = "llama3.2",      
            messages = self.cli_messages,
        )
        cli_reply = response.choices[0].message.content
        self.cli_messages.append({"role": "assistant", "content": cli_reply})

        response = self.judge.chat.completions.create(
            model= "llama3.2",
            messages=[self.jud_setting, {"role": "user", "content": f'The user: {user_input}; {self.name}: {self.cli_messages[-1]['content']}'}],
        )
        jud_reply = response.choices[0].message.content
        if 'Low' in jud_reply or 'low' in jud_reply:
            self.likability -= 1
        elif 'medium' in jud_reply or 'Medium' in jud_reply:
            self.likability += 1
        elif 'High' in jud_reply or 'high' in jud_reply:
            self.likability += 3
        if self.likability < 0:
            self.likability = 0
        elif self.likability > 100:
            self.likability = 100
        self.user_resource[f'likability_{self.name}'] = self.likability

        if '1' in jud_reply:
            self.user_resource['Soulstone'] += 1
        elif '2' in jud_reply:
            self.user_resource['Soulstone'] += 2
        elif '3' in jud_reply:
            self.user_resource['Soulstone'] += 3

        self.write_in(0, user_input)
        self.write_in(self.name, self.cli_messages[-1]['content'])
        
        
        self.acer.update_resource(self.username, self.user_resource)
        return cli_reply

    def write_in(self, name:str, content:str):
        f = open(f"Text\\Accounts\\{self.username}\\Dialogue_with_{self.name}_{self.nowtime}.txt", "a", encoding="UTF-8")
        f.write(f"{name}   \t{content}\n\n")
        f.close()

if __name__ == "__main__":
    npc1 = npc_dia('Alice','aaaaa')
    while 1:
        print(npc_dia.talk(npc1,input()))
        print(npc1.likability)