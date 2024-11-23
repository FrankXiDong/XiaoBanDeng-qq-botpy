import os,json,botpy,time,random,requests,ast,urllib,datetime
from botpy import logging,logger,message,BotAPI
from botpy.message import DirectMessage,Message,GroupMessage
from botpy.ext.cog_yaml import read
from botpy.types.message import Reference
from botpy.types.announce import AnnouncesType
from botpy.forum import Thread
from botpy.types.forum import Post, Reply, AuditResult
from botpy.types.channel import ChannelSubType, ChannelType
from time import sleep
from codeshop.locknum import locknum
from codeshop.game import joingame,startgame
from codeshop.balance import balance
from codeshop.output import arcode,arname,tryagain,chat_body

_log = logging.get_logger()
keyanswer={
    "test":"你在测试什么？",
    "你是哪个省的":"妈妈生的（误）",
    }

class MyClient(botpy.Client):
    
    async def on_ready(self):#初次启动时
        start_txt="\
-----------启动成功------------\n\
    小板凳频道管家，启动！\n\
    版本:v6.0.0-600"
        print(start_txt)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%m")
    if date == '2024-8-28 17:50':
        message._api.post_group_message(
                    group_openid="BC5B5B45E1A6AF8BAEE0166EE82584E9",
                    msg_type=0,
                    msg_id=message.id,
                    content=f"test"
                    )
    async def on_c2c_message_create(self, message:Message):#收到私聊信息时
        dataid=eval(str(message.author))
        open_id = dataid['user_openid']#获取open_id
        if "新增提示词" in message.content:#新增AI大模型的提示词
            word = message.content.split('新增提示词')[1]
            with open('./temp/model.txt', 'a',encoding='utf-8') as file:  
                file.write("\n"+word)
            await message._api.post_c2c_message(
                openid=message.author.user_openid, 
                msg_type=0, msg_id=message.id, 
                content=f"我收到了你的提示词：{word}。"
            )
            logger.info("新增了一个提示词。\n发送指令的ID：{open_id}\n提示词内容：{word}")
    async def on_group_at_message_create(self, message: GroupMessage):#收到群消息时        
        dataid=eval(str(message.author))
        open_id = dataid['member_openid']#获取open_id
        result=False
        if "/绑定 " in message.content:#绑定用户名和open_id
            result=locknum(message.content,open_id)
        elif "加入真心话" in message.content or "参加真心话" in message.content:#加入游戏
            result=joingame(message.author)
        elif "开始真心话" in message.content:#开始游戏
            result=startgame(message.author)
        elif "查询余额" in message.content:
            data=balance()
            result="剩余的余额为："+data+"元人民币。"
        elif "读取" in message.content:
            with open('./temp/tryagain.txt','r', encoding='utf-8') as f:
                result=f.read()
        elif "查地方 " in message.content:
            result=arcode(message.content)
        elif "查区号 " in message.content:
            result=arname(message.content)
        elif "清空上下文" in message.content:
            with open('./temp/temp_message.txt', 'w', encoding='utf-8') as file:  
                file.write("[]")
            result="已经清空了缓存的所有上下文数据！"  
        elif "/功能" in message.content:
            with open('./temp/aboutme.txt', 'r', encoding='utf-8') as file:  
                result=file.read()
        else:
            data = False
            for k,r in keyanswer.items():
                if k in message.content:#如果在固定问答内容中，使用固定问答文本
                    result=r
                    data=True
            if data == False:
                result=chat_body(message.content)
        if result!=False:
            try:
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"{result}"
                    )
                result=True
            except:
                a=tryagain(result)
                print(a)
                with open('./temp/tryagain.txt', 'w', encoding='utf-8') as file:  
                    file.write(a)
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"请尝试发送“读取”获取加密版回答"
                    )
        else:
            await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"机器人的程序貌似出错了，请联系开发者处理！"
                    )
        return result
                            

if __name__ == "__main__":
    intents = botpy.Intents.none()
    intents.public_guild_messages=True
    intents.direct_message=True
    intents.guilds=True
    intents.guild_messages=True
    intents.guild_members=True
    intents.interaction=True
    intents.guild_message_reactions=True
    intents.forums=True
    intents.public_messages=True
    #intents = botpy.Intents(public_guild_messages=True, direct_message=True, guilds=True)
    client = MyClient(intents=intents,timeout=8)
    client.run(appid="102040950",secret="Pr9E9sPimeIoCg4K")