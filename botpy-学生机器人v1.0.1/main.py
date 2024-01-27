# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging
from botpy import logger

from botpy.message import DirectMessage,Message
from botpy.ext.cog_yaml import read
from botpy.types.message import Reference
from botpy.types.announce import AnnouncesType

from time import sleep
import time
import random

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

keywords=['sb','党','政治','资本','他妈的','woc','体制','tm','wc','fuck']
keyanswer={'你好':'你好！',"你知道大鸟吗":"我知道啊，她可是我们频道的管理啊！","你认识大鸟吗":"我知道啊，她可是我们频道的管理啊！",
           "你能干什么":"你猜~"}

import csv

def scored(uid,score):
    csv_file = open('score.csv', 'w', newline='', encoding='utf-8')
    uid=str(uid)
    score=str(score)
    writer = csv.writer(csv_file)
    writer.writerow([uid, score])
    csv_file.close()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")
        '''
        while True:
            t = time.localtime()
            if t.tm_hour==21 and t.tm_min==2:
                await self.api.mute_all(guild_id="15112674826139015277",mute_seconds="5")
                sleep(60)
            elif t.tm_hour==9 and t.tm_min==30:
                await self.api.mute_all(guild_id="15112674826139015277",mute_seconds="1800")
                sleep(60)

        '''
    
    async def on_direct_message_create(self, message: DirectMessage):
        
        if "/发送帖子" in message.content:#该功能未调试完毕
            mes=message.content.split('/发送帖子 ')[1]
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"收到你要发送的帖子了:\n {mes}",
                msg_id=message.id,
            )
            
    async def on_message_create(self, message: Message):
        #_message = await message.reply(content=f"test返回")
        m=message.content
        for kw in keywords:
            if kw in m:
                try:
                    await self.api.recall_message(message.channel_id, message_id=message.id, hidetip=False)
                    _message = await message.reply(content=f"您的信息内包含关键词，将撤回您的消息！")
                    sleep(5)
                    await self.api.recall_message(message.channel_id, _message.get("id"), hidetip=False)
                except:
                    message_reference = Reference(message_id=message.id)
                    await self.api.post_message(channel_id=message.channel_id, content="您的信息内包含关键词。\
本频道未开通管理功能或者您的等级较高，请自觉撤回。", msg_id=message.id,message_reference=message_reference)
     

    async def on_at_message_create(self, message: Message):
        if "解锁私信" in message.content:
            #await self.api.get_guild(guild_id=message.guild_id)
            await self.api.create_dms(guild_id=message.guild_id, user_id=message.author.id)
            await self.api.get_channels(guild_id=message.guild_id)
            await self.api.post_dms(guild_id=message.guild_id,content="快来找我玩啊！",msg_id=message.id)
            a=await self.api.get_channels(guild_id=message.guild_id)
            logger.info(a)
            #logger.info(channels.name,channels.id)
        elif "你是哪个省的" in message.content:
            _message = await message.reply(content=f"妈妈生的（确信）")
        elif "补课" in message.content:
            _message = await message.reply(content=f"什么s b学校还补课？？")
        if "什么是学削" in message.content or "什么是学校" in message.content:
            _message = "学削就是以自我利益至上，违规、违法、违纪，把学生当成盈利的工具，\
甚至给其或其家长洗脑的病态学校。\n不过，不包括少数依然站立在教育正确道路上的正常学校在内。"
            await self.api.post_message(channel_id=message.channel_id, content=_message, msg_id=message.id)

        elif "给我点赞" in message.content:
            await self.api.put_reaction(channel_id=message.channel_id, message_id=message.id,
                                        emoji_type=1, emoji_id="76")
            message_reference = Reference(message_id=message.id)
            await self.api.post_message(channel_id=message.channel_id, content="给你点赞啦，不用谢！",
                                        msg_id=message.id,message_reference=message_reference)
            
        elif "创建子频道" in message.content:
            n=message.content
            x = n.split("子频道 ")[1]
            if x=="":
                x="新的子频道"
            #mcard=await self.api.get_guild_member(guild_id=message.guild_id, user_id=message.author.id)
            p=await self.api.get_channel(channel_id=message.channel_id)
            if "4"or"2"or"7"or"16611081"or"16617493" in mcard.roles:
                await self.api.create_channel(guild_id=message.guild_id,name=x,type="0",
              sub_type="0",position=100,parent_id=p["parent_id"])
                message_reference = Reference(message_id=message.id)
                await self.api.post_message(channel_id=message.channel_id, content="创建成功！",
                                            msg_id=message.id,message_reference=message_reference)
            else:
                _message = await message.reply(content=f"你没有权限！")

        elif "身份组列表" in message.content:
            role=await self.api.get_guild_roles(guild_id=message.guild_id)
            roles=role["roles"]
            #logger.info(roles)
            _message = await message.reply(content=f"已打印到日志中")
            
            ma=""
            for ro in roles:  
                # 输出每一项的id和name  
                ma+=ro['id']+" "+ro['name']+"\n"
            await self.api.post_message(channel_id=message.channel_id, content=ma, msg_id=message.id)
            logger.info(ma)
            
        elif "7931" in message.content:#发送信息到通知区指令
            n=message.content
            s = n.split("7931")[1]
            await self.api.post_message(channel_id="638842221", content=s,
                                        msg_id=message.id)        
            await self.api.post_message(channel_id=message.channel_id, content="！", msg_id=message.id)

        elif "5357" in message.content:#发送信息到通管理群指令
            n=message.content
            s = n.split("5357")[1]
            await self.api.post_message(channel_id="638632892", content=s,
                                        msg_id=message.id,
                                        )        
            await self.api.post_message(channel_id=message.channel_id, content="！", msg_id=message.id)
            


        elif "1792" in message.content:#临时指令2
            await self.api.update_guild_role(
            guild_id=message.guild_id,
            role_id="16752938",
            name="智慧少年",
            color="4251856",
            hoist=1,
        )
            await self.api.post_message(channel_id=message.channel_id, content="！",
                                        msg_id=message.id)

        elif "子频道列表" in message.content:
            channel=await self.api.get_channels(guild_id=message.guild_id)
            #logger.info(channel)
            _message = await message.reply(content=f"已打印到日志中")
            ma=""
            for ch in channel:  
                # 输出每一项的id和name  
                ma+=ch['id']+" "+ch['name']+"\n"
            await self.api.post_message(channel_id=message.channel_id, content=ma, msg_id=message.id)
            logger.info(ma)
            

            
        elif "精选子频道" in message.content:
            channel_list = [{"channel_id": message.channel_id, "introduce": "introduce"}]
            await self.api.create_recommend_announce(message.guild_id, AnnouncesType.MEMBER, channel_list)
            message_reference = Reference(message_id=message.id)
            await self.api.post_message(channel_id=message.channel_id, content="已经设置精选！",
                                        msg_id=message.id,message_reference=message_reference)

        elif "创建身份组" in message.content:
            await self.api.create_guild_role(
                guild_id=message.guild_id,
                name="临时身份组",
                color="10395294",
                hoist=1,
            )
            _message = await message.reply(content=f"已创建")
            
        elif "真心话大冒险" in message.content:
            #_message = await message.reply(content=f"注意：该功能正在调试！")
            a=0
            try:
                n=message.content

                x = n.split("大冒险 ")[1]
                #x = n.lstrip('<@!17579885878760051378> /真心话大冒险 ')
                sleep(3)
                #_message = await message.reply(content=f"该功能经常报错，请等待修复！")
                #a=await self.api.post_message(channel_id=message.channel_id, content=x,msg_id=message.id)
                people=int(x)
                #a=people % 1
                if people<=1:
                    ans=str(people)+'个人玩个毛？快邀请好友一起来玩吧！'
                    await self.api.post_message(channel_id=message.channel_id, content=ans,
                                                msg_id=message.id)
                #elif type(people)!=int:
                #    ams='我想见见你那小数个朋友（）'
                #    await self.api.post_message(channel_id=message.channel_id, content=ans,msg_id=message.id)
                else:
                    m=0
                    for i in range (0,people):
                        m+=1
                        num=random.randint(30,500)
                        ans='第'+str(m)+'个玩家的值为：'+str(num)
                        b=await self.api.post_message(channel_id=message.channel_id, content=ans,
                                                      msg_id=message.id)
            except:
                _message = await message.reply(content=f"程序报错！")
                print("（真心话大冒险）程序报错")
                logger.info("（真心话大冒险）程序报错")
        
        else:
            ret=False
            for k,r in keyanswer.items():
                if k in message.content:
                    ret=True
                    message_reference = Reference(message_id=message.id)
                    await self.api.post_message(channel_id=message.channel_id, content=r,
                                                msg_id=message.id,message_reference=message_reference)
                    
                    

            
            #re=False#临时
            if ret==False:
                _message = await message.reply(content=f"尚不支持该指令或尚未开通有关功能！")
if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    #intents = botpy.Intents.none()
    #intents = botpy.Intents.all()
    intents = botpy.Intents.none()
    intents.public_guild_messages=True
    intents.direct_message=True
    intents.guilds=True
    intents.guild_messages=True
    intents.guild_members=True
    intents.interaction=True
    intents.guild_message_reactions=True

    #intents = botpy.Intents(public_guild_messages=True, direct_message=True, guilds=True)


    client = MyClient(intents=intents)
    client.run(appid="102040950",secret="Pr9E9sPimeIoCg4K")
