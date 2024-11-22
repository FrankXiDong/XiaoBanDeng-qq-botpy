# -*- coding: utf-8 -*-
import os
import json

import botpy
from botpy import logging
from botpy import logger

from botpy.message import DirectMessage,Message,GroupMessage
from botpy.ext.cog_yaml import read
from botpy.types.message import Reference
from botpy.types.announce import AnnouncesType
from botpy.forum import Thread
from botpy.types.forum import Post, Reply, AuditResult
from botpy.types.channel import ChannelSubType, ChannelType

from time import sleep
import time
import random

import requests
from openai import OpenAI
import ast
import json,urllib
from urllib.parse import urlencode
from urllib.request import urlopen

#config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


#敏感词词典，实际以存储的文件（keywords.txt）为准
keywords=['政治','资本',
          ]
#问答词典，暂无存储文件
keyanswer={"test":"你在测试什么？"}
#积分系统（测试版）
box=[{"user":"efsdw","id":"324","score":0},{"user":"abandon","id":"324","score":0},{'user': '咚咚咚别睡了（诈尸）','id': '2207801275763224088',"score":0}]

nid={"8A0FBC6EAFCE6496E863E7F59B46255E":"1945748037"}

def tryagain(text):  
    # 将字符串转换为字符列表，除了最后一个字符外，每个字符后都加上"？"  
    result = ''.join([char + '.' if i < len(text) - 1 else char for i, char in enumerate(text)])  
    return result  


def areacode(area):
    url = 'http://api.k780.com'
    params = {
      'app' : 'life.areacode',
      'areacode' : area,
      'appkey' : '73847',
      'sign' : '66107e84b89b9eba439b35daa9eb54a4',
      'format' : 'json',
      
    }
    params = urlencode(params)
    

    f = urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    #print content
    a_result = json.loads(nowapi_call)
    if a_result:
      if a_result['success'] != '0':
        print(a_result['result'])
        data=a_result['result']
        simcalls = [item['simcall'] for item in data['lists']]  
        return simcalls
      else:
        print(a_result['msgid']+' '+a_result['msg'])
        return a_result['msgid']+' '+a_result['msg']
    else:
      print('Request nowapi fail.')
      return 'Request nowapi fail.'
def areaname(area):
    url = 'http://api.k780.com'
    params = {
      'app' : 'life.areacode',
      'areaname' : area,
      'appkey' : '73847',
      'sign' : '66107e84b89b9eba439b35daa9eb54a4',
      'format' : 'json',
    }
    params = urlencode(params)

    f = urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    #print content
    a_result = json.loads(nowapi_call)
    if a_result:
      if a_result['success'] != '0':
        print(a_result['result'])
        data=a_result['result']
        simcalls = [item['areacode'] for item in data['lists']]  
        return simcalls
      else:
        return a_result['msgid']+' '+a_result['msg']
    else:
      return 'Request nowapi fail.'


    
#AI交互问答功能
#...................................................
#...................................................
    
def chat_with_deepseek(api_key, model_name, user_message, system_message,temp_message):  
    """  
    与DeepSeek的聊天模型进行交互。  
  
    参数:  
    - api_key: 用于访问DeepSeek API的密钥。  
    - model_name: 要使用的模型名称。  
    - user_message: 用户发送给聊天模型的消息。  
    - system_message: 系统发送给聊天模型的初始消息（可选，默认为"You are a helpful assistant"）。  
  
    返回:  
    - 聊天模型的响应内容。  
  
    抛出:  
    - OpenAIError: 如果API调用失败。  
    """  
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")  
    ins=[{"role": "system", "content": system_message}]
    #ins=[{"role": "system", "content": "你是个机器人"}]
    ins.append(eval(temp_message))
    ins.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model=model_name,  
            messages=ins,
            max_tokens=800,
            temperature=0.5,
            stream=False
        )  
        # 假设API响应结构符合OpenAI Playground的结构  
        try:
            return response.choices[0].message.content
        except:
            print(f"An error occurred:程序报错")  
            return "程序出错了！"
    except:  
        print(f"An error occurred:程序报错")  
        return "程序出错了！"
    
    #return "0"



class MyClient(botpy.Client):
    async def on_ready(self):
       print("\
-----------启动成功------------\n\
     小板凳频道管家，启动！\n\
     版本号：4.2.1-120")
    with open('./temp/keywords.txt','r') as f:
        keywords=eval(f.read())

    async def on_direct_message_create(self, message: DirectMessage):
        data=message
        username = data.author.username 
        #author_info = json.loads(author_data)  # 将字符串转换为字典    
        #username = author_info['username']


        #通过私信发送匿名帖子

        #介绍功能使用方法
        if "我要发帖" in message.content:
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"\
欢迎使用“小板凳匿名发帖”功能！\n\n\
使用本功能发帖，在频道内不会出现您的昵称，可以起到匿名发帖的作用。\n\
但是，为了保障机器人和频道的安全，防止匿名发布违法违规内容，您的发帖内容、发帖时间、昵称等有关信息会被记录在机器人服务器中，\
若出现违规匿名帖，频道会查询这些信息，对你进行处罚；频道管理组将采取包括但不限于禁言、禁止使用匿名发帖功能、取消身份组、踢出、拉黑等操作，\
情节严重的犯罪行为，频道管理组将依法报告给有关机关。\n\n\
使用方法：\n\
1.“/简单帖”+帖子内容（使用该方式，帖子标题默认为“成员投稿”）\n\
2.“/标准帖”+帖子标题+“//”+帖子正文\n\
3.“/指定帖”+版块代号+“//”+帖子标题+“：：”（中文冒号）+帖子正文\n\n\
若指令输入正确，机器人会回复你一条消息；若指令输入错误，机器人可能不会回复任何消息、不会执行任何操作。",
                msg_id=message.id,
            )
        
        #发送方式1——无标题，标题默认为“成员投稿”
        elif "/简单帖" in message.content:
            logger.info(username+"("+message.author.id+")发送了："+message.content)
            mes=message.content.split('/简单帖 ')[1]

            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"我已经收到你要发送的帖子了！请核对帖子内容:\n {mes}\n\
------温馨提示------\n\
温馨提示：根据腾讯频道发帖机制，你发出的帖子需要经过审核才会被公开。我已经第一时间\
将帖子发送，正在审核中，请耐心等待。\n\
若超过24小时仍未公开，可能是被腾讯频道屏蔽，请修改帖子内容后重试！",
                msg_id=message.id,
            )
            n=message.content
            s = n.split("/简单帖")[1]
            await self.api.post_thread(channel_id="635737790",title="成员投稿",
                                       content=s, format="1")
            login=username+"("+message.author.id+")发送了："+message.content
            logger.info(login)

        #发送方式2——有标题，发送方式：/发送帖子2+标题+//+正文
        elif "/标准帖" in message.content:
            logger.info(username+"("+message.author.id+")发送了："+message.content)
            mes=message.content.split('/标准帖')[1]
            mt=mes.split('//')[0]
            mc=mes.split('//')[1]
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"我已经收到你要发送的帖子了！请核对帖子内容:\n 【标题：】{mt}\n{mc}\n\n\
------温馨提示------\n\
温馨提示：根据腾讯频道发帖机制，你发出的帖子需要经过审核才会被公开。我已经第一时间\
将帖子发送，正在审核中，请耐心等待。\n\
若超过24小时仍未公开，可能是被腾讯频道屏蔽，请修改帖子内容后重试！",
                msg_id=message.id,
            )
            await self.api.post_thread(channel_id="635737790", title=mt,content=mc, format="1")
            login=username+"("+message.author.id+")发送了："+message.content
            logger.info(login)
            
        elif "/指定帖" in message.content:
            true=message.content.split("/指定帖")[1]
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"收到你要发送的帖子了:\n {true}",
                msg_id=message.id,
            )
            cha=true.split('//')[0]
            mes=true.split('//')[1]
            tit=mes.split('：：')[0]
            con=mes.split('：：')[1]
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=f"我已经收到你要发送的帖子了！请核对帖子内容:\n 【标题：】{tit}\n{con}\n\n\
------温馨提示------\n\
温馨提示：根据腾讯频道发帖机制，你发出的帖子需要经过审核才会被公开。我已经第一时间\
将帖子发送，正在审核中，请耐心等待。\n\
若超过24小时仍未公开，可能是被腾讯频道屏蔽，请修改帖子内容后重试！",
                msg_id=message.id,
            )
            await self.api.post_thread(channel_id=cha, title=tit,content=con, format="1")
            login=username+"("+message.author.id+")发送了："+message.content
            logger.info(login)
            
        elif "/新增词库" in message.content:
            word=message.content.split('/新增词库 ')[1]
            keywords.append(word)
            with open('./temp/keywords.txt','w') as f:
                f.write(str(keywords))

        elif "/新增提示词" in message.content:
            word=message.content.split('/新增提示词')[1]
            with open('./temp/model.txt', 'a',encoding='utf-8') as file:  
                file.write("\n"+word+"\n")
        


    #一切消息
        
    async def on_message_create(self, message: Message):
        #_message = await message.reply(content=f"test返回")
        s=message.content 
        m = s.lower().replace(" ", "") .replace(".","").replace("。","")
        if "/创建子频道" in message.content:
            n=str(random.randint(100000,999999))
            a=await self.api.create_channel(
          guild_id=message.guild_id,
          name="新的子频道"+n,
          type="0",
          sub_type="0",
          position="20",
          parent_id="642317176",
        )
            _message = await message.reply(content=f"已创建<#"+a["id"]+">!")
        elif "参加真心话"in message.content or "加入真心话" in message.content:
            with open('./temp/scor.txt','r')as f:
                score=eval(f.read())
            a_name=message.author.username
            a_id=message.author.id
            def check(value, my_dict):
                for key in my_dict:
                    if value == key:
                        return True
                return False
            chong=check(a_id,score)
            if chong==True:
                _message = await message.reply(content=f"你已加入游戏，请勿重复加入！")
                
            else:
                n=message.content
                score[a_id]={"name":a_name,"exe":1,"score":0}
                message_reference = Reference(message_id=message.id)
                await self.api.post_message(channel_id=message.channel_id, content="<@"+a_id+">加入游戏成功~",
                                        msg_id=message.id,message_reference=message_reference)

                with open('./temp/scor.txt','w') as f:
                    f.write(str(score))    
            
        elif "开始真心话" in message.content:
            with open('./temp/scor.txt','r')as f:
                score=eval(f.read())
            
            n=len(score.keys())
            
            if n<=1:
                _message = await message.reply(content=f"参加的人数不够呢，快去邀请其他人一起加入吧！")
            else:
                win=random.randint(1,n)
                a=0
                loser=[]
                for i in score:
                    a+=1
                    if a==win:
                        winner=score[i]["name"]
                    else:
                        loser.append(score[i]["name"])
                message_reference = Reference(message_id=message.id)
                await self.api.post_message(channel_id=message.channel_id, content="获胜者："+winner,
                                            msg_id=message.id,message_reference=message_reference)
                await self.api.post_message(channel_id=message.channel_id, content="输家："+str(loser),
                                            msg_id=message.id,message_reference=message_reference)
                score={}
                with open('./temp/scor.txt','w') as f:
                    f.write('{}') 
        for kw in keywords:
            if m=="":
                break
            elif kw in m:
                role=message.member.roles
                try:
                    if "16617493" in role:
                        await self.api.delete_guild_role_member(guild_id=message.guild_id,
                                                                role_id="16617493",
                                                                user_id=message.author.id)
                        await self.api.recall_message(message.channel_id, message_id=message.id, hidetip=False)
                        _message = await message.reply(content=f"您的信息内包含关键词，将撤回您的消息！")
                        await self.api.create_guild_role_member(guild_id=message.guild_id,
                                                                role_id="16617493",
                                                                user_id=message.author.id)
                        sleep(5)
                        await self.api.recall_message(message.channel_id, _message.get("id"), hidetip=False)
                        
                        
                        
                    elif "16784946" in role:
                        await self.api.delete_guild_role_member(guild_id=message.guild_id,
                                                                role_id="16784946",
                                                                user_id=message.author.id)
                        await self.api.recall_message(message.channel_id, message_id=message.id, hidetip=False)
                        _message = await message.reply(content=f"您的信息内包含关键词，将撤回您的消息！")
                        await self.api.create_guild_role_member(guild_id=message.guild_id,
                                                                role_id="16784946",
                                                                user_id=message.author.id)
                        sleep(5)
                        await self.api.recall_message(message.channel_id, _message.get("id"), hidetip=False)
                        
                    else:
                        await self.api.recall_message(message.channel_id, message_id=message.id, hidetip=False)
                        _message = await message.reply(content=f"您的信息内包含关键词，将撤回您的消息！")
                        sleep(5)
                        await self.api.recall_message(message.channel_id, _message.get("id"), hidetip=False)
                except:
                    message_reference = Reference(message_id=message.id)
                    await self.api.post_message(channel_id=message.channel_id, content="----------------提示----------------\n\
<@"+message.author.id+">\n\
您的信息内包含关键词。\n\
本频道未开通管理功能或者您的等级较高，请自觉撤回。", msg_id=message.id,message_reference=message_reference)
            elif "m浩" in message.content and "roro" in message.content:
                role=message.member.roles
                try:
                    if "16617493" in role:
                        await self.api.delete_guild_role_member(guild_id=message.guild_id,
                                                                role_id="16617493",
                                                                user_id=message.author.id)
                        await self.api.recall_message(message.channel_id, message_id=message.id, hidetip=True)
                        await self.api.create_guild_role_member(guild_id=message.guild_id,
                                                                role_id="16617493",
                                                                user_id=message.author.id)
                        
                        
                    elif "16784946" in role:
                        await self.api.delete_guild_role_member(guild_id=message.guild_id,
                                                                role_id="16784946",
                                                                user_id=message.author.id)
                        await self.api.recall_message(message.channel_id, message_id=message.id, hidetip=True)
                        await self.api.create_guild_role_member(guild_id=message.guild_id,
                                                                role_id="16784946",
                                                                user_id=message.author.id)
                    else:
                        await self.api.recall_message(message.channel_id, message_id=message.id, hidetip=True)
                        break
                except:
                    a=0
            
     
    #@的消息
                    
    async def on_at_message_create(self, message: Message):
        global score,nid
        #logger.info(message)
        
        
        if "799" in message.content:
            ww=await self.api.get_message(channel_id=message.channel_id, message_id=message.id)
            logger.info(ww)
            ta=message.author.id
            tb=message.author.username
            logger.info(ta+tb)

        
        elif "解锁私信" in message.content:
            #await self.api.get_guild(guild_id=message.guild_id)
            await self.api.create_dms(guild_id=message.guild_id, user_id=message.author.id)
            #await self.api.get_channels(guild_id=message.guild_id)
            await self.api.post_message(channel_id=message.channel_id,content="快来找我玩啊！",msg_id=message.id)
            #a=await self.api.get_channels(guild_id=message.guild_id)
            #logger.info(a)
            #logger.info(channels.name,channels.id)
        elif "人数查询" in message.content:
            mes=await self.api.get_guild(guild_id=message.guild_id)
            a='-----查询结果-----\n频道人数：'+str(mes["member_count"])+'\n频道人数上限:'+str(mes["max_members"])
            await self.api.post_message(channel_id=message.channel_id,content=a,msg_id=message.id)
        elif "子频道权限" in message.content:
            mes=await self.api.get_channel_user_permissions(channel_id=message.channel_id, user_id=message.author.id)
            
            await self.api.post_message(channel_id=message.channel_id,content=mes["permissions"],msg_id=message.id)
            
        elif "你是哪个省的" in message.content:
            _message = await message.reply(content=f"妈妈生的（确信）")
        elif "补课" in message.content:
            _message = await message.reply(content=f"什么sb学校还补课？？")
        elif "什么是学削" in message.content or "什么是学校" in message.content:
            _message = "学削就是以自我利益至上，违规、违法、违纪，把学生当成盈利的工具，\
甚至给其或其家长洗脑的病态学校。\n不过，不包括少数依然站立在教育正确道路上的正常学校在内。"
            await self.api.post_message(channel_id=message.channel_id, content=_message, msg_id=message.id)

        elif "给我点赞" in message.content:
            await self.api.put_reaction(channel_id=message.channel_id, message_id=message.id,
                                        emoji_type=1, emoji_id="76")
            message_reference = Reference(message_id=message.id)
            await self.api.post_message(channel_id=message.channel_id, content="给你点赞啦，不用谢！",
                                        msg_id=message.id,message_reference=message_reference)
        elif "上麦" in message.content:
            await self.api.on_microphone(message.channel_id)
        elif "谢谢小董" in message.content:
            _message = "谢谢小董！"*100
            a=await self.api.post_message(channel_id=message.channel_id, content=_message, msg_id=message.id)
            await self.api.put_reaction(channel_id=message.channel_id, message_id=a.message.id,
                                        emoji_type=1, emoji_id="76")
        elif "新建子频道" in message.content:
            n=str(random.randint(100000,999999))
            a=await self.api.create_channel(
          guild_id=message.guild_id,
          name="新的子频道"+n,
          type="0",
          sub_type="0",
          position="20",
          parent_id="642317176",
        )
            _message = await message.reply(content=f"已创建<#"+a["id"]+">!")

        elif "新建公告子频道" in message.content:
            n=str(random.randint(100000,999999))
            a=await self.api.create_channel(
          guild_id=message.guild_id,
          name="新的子频道"+n,
          type="0",
          sub_type="1",
          position="20",
          parent_id="642317176",
        )
            _message = await message.reply(content=f"已创建<#"+a["id"]+">!")

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
           
        elif "发送消息" in message.content:#临时发送信息
            n=message.content
            s = n.split("发送消息")[1]
            cha=s.split("//")[0]
            mes=s.split("//")[1]
            await self.api.post_message(channel_id=cha, content=mes,
                                        msg_id=message.id)        
            #await self.api.post_message(channel_id=message.channel_id, content="！", msg_id=message.id)

       
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
            
        elif "参加真心话"in message.content or "加入真心话" in message.content:
            with open('./temp/scor.txt','r')as f:
                score=eval(f.read())
            a_name=message.author.username
            a_id=message.author.id
            def check(value, my_dict):
                for key in my_dict:
                    if value == key:
                        return True
                return False
            chong=check(a_id,score)
            if chong==True:
                _message = await message.reply(content=f"你已加入游戏，请勿重复加入！")
                
            else:
                n=message.content
                score[a_id]={"name":a_name,"exe":1,"score":0}
                message_reference = Reference(message_id=message.id)
                await self.api.post_message(channel_id=message.channel_id, content="<@"+a_id+">加入游戏成功~",
                                        msg_id=message.id,message_reference=message_reference)

                with open('./temp/scor.txt','w') as f:
                    f.write(str(score))    
            
        elif "开始真心话" in message.content:
            with open('./temp/scor.txt','r')as f:
                score=eval(f.read())
            
            n=len(score.keys())
            
            if n<=1:
                _message = await message.reply(content=f"参加的人数不够呢，快去邀请其他人一起加入吧！")
            else:
                win=random.randint(1,n)
                a=0
                loser=[]
                for i in score:
                    a+=1
                    if a==win:
                        winner=score[i]["name"]
                    else:
                        loser.append(score[i]["name"])
                message_reference = Reference(message_id=message.id)
                await self.api.post_message(channel_id=message.channel_id, content="获胜者："+winner,
                                            msg_id=message.id,message_reference=message_reference)
                await self.api.post_message(channel_id=message.channel_id, content="输家："+str(loser),
                                            msg_id=message.id,message_reference=message_reference)
                score={}
                with open('./temp/scor.txt','w') as f:
                    f.write('{}') 
        elif "真心话" in message.content or "大冒险" in message.content:           
            await message.reply(content=f"\
--------指令错误！--------\n\
请尝试使用指令：\n\
  @小板凳频道管家 加入真心话\n\
  @小板凳频道管家 开始真心话")

        

        
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
                _message = await message.reply(content=f"尚不支持该指令或尚未开通有关功能捏~\n\
你可以试试：@小板凳频道管家 开始真心话")




            #测试！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
            #测试！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
            #群消息



                
    async def on_group_at_message_create(self, message: GroupMessage):
        _log.info(message)
        
        if "/绑定 " in message.content:
            n=message.content
            tid = n.split("/绑定 ")[1]  
            # 解析author字段为字典
            a=eval(str(message.author))
            oid = a['member_openid']
            with open('./temp/nid.txt','r',encoding='utf-8')as f:
                nid=eval(f.read())
            def check(value, my_dict):
                for key in my_dict:
                    if value == key:
                        return True
                return False
    
            if check(oid,nid) == False:
                nid[oid]=tid
                with open('./temp/nid.txt','w',encoding='utf-8') as f:
                    f.write(str(nid))   
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"用户{tid}已绑定成功！"
                    )
            else:
                nid[oid]=tid
                with open('./temp/nid.txt','w',encoding='utf-8') as f:
                    f.write(str(nid)) 
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"用户{tid}已修改用户名！"
                    )
            print(nid)
            e=str(nid)

        
        elif "参加真心话"in message.content or "加入真心话" in message.content:
            with open('./temp/scor.txt','r')as f:
                score=eval(f.read())
            a=eval(str(message.author))
            oid = a['member_openid']
            with open('./temp/nid.txt','r',encoding='utf-8')as f:
                nid=eval(f.read())
            if oid in str(nid):                
                a_name=nid[oid]
            else:
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"请先绑定你的QQ号或用户名。\n\
绑定方法：@机器人并发送指令“/绑定 ”+QQ号或用户名"
                    )
                beak
            a_id=oid
            def check(value, my_dict):
                for key in my_dict:
                    if value == key:
                        return True
                return False

            if oid in str(score):
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"拥护{a_name}已加入过了，请勿重复加入！"
                    )   
            else:
                n=message.content
                score[a_id]={"name":a_name,"exe":1,"score":0}
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"用户{a_name}加入游戏成功~"
                    )
                with open('./temp/scor.txt','w') as f:
                    f.write(str(score))
            
            
        elif "开始真心话" in message.content:
            with open('./temp/scor.txt','r')as f:
                score=eval(f.read())
            a=eval(str(message.author))
            oid = a['member_openid']
            with open('./temp/nid.txt','r',encoding='utf-8')as f:
                nid=eval(f.read())
            a_name=nid[oid]
            a_id=oid
            n=len(score.keys())
            
            if n<=1:
                
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"参加的人数不够呢，快去邀请其他人一起加入吧！")

            else:
                win=random.randint(1,n)
                a=0
                loser=[]
                for i in score:
                    a+=1
                    if a==win:
                        winner=score[i]["name"]
                    else:
                        loser.append(score[i]["name"])
                loser=str(loser).replace('[','').replace(']','')
                message_reference = Reference(message_id=message.id)
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"获胜者：{winner}，\n输家：{loser}\n\
请输家接受获胜者的惩罚！")
                score={}
                with open('./temp/scor.txt','w') as f:
                    f.write('{}') 
        
        elif "查询余额" in message.content:
            url = "https://api.deepseek.com/user/balance"
            payload={}
            headers = {
              'Accept': 'application/json',
              'Authorization': 'Bearer sk-5cd23846d4304f63b93db419bf87641e'
            }
            response = requests.request("GET", url, headers=headers, data=payload)

            print(response.text)
            data = json.loads(response.text)  
            a=data["balance_infos"][0]["total_balance"]
            await message._api.post_group_message(group_openid=message.group_openid,
                                                    msg_type=0,
                                                    msg_id=message.id,
                                                    content=f"{a}元人民币")
        elif "读取" in message.content:
            with open('./temp/tryagain.txt','r', encoding='utf-8') as f:
                        text=f.read()
            await message._api.post_group_message(group_openid=message.group_openid,
                                                    msg_type=0,
                                                    msg_id=message.id,
                                                    content=f"以下为新的回答：{text}")    
        elif "查地方 " in message.content:
            area=message.content.split('查地方 ')[1]
            ans=str(areacode(area))
            ans=ans.replace('[','').replace(']','')
            await message._api.post_group_message(group_openid=message.group_openid,
                                                    msg_type=0,
                                                    msg_id=message.id,
                                                    content=f"区号{area}对应地为：{ans}")
        elif "查区号 " in message.content:
            area=message.content.split('查区号 ')[1]
            if "三沙" in area:
                ans="0898"
            else:
                ans=str(areaname(area))
                ans=ans.replace('[','').replace(']','')
                if "1000060" in ans:
                    await message._api.post_group_message(group_openid=message.group_openid,
                                                        msg_type=0,
                                                        msg_id=message.id,
                                                        content=f"没有查到该地方的区号，\
请确认地名是否为地级行政区划。")
                else:
                    await message._api.post_group_message(group_openid=message.group_openid,
                                                        msg_type=0,
                                                        msg_id=message.id,
                                                        content=f"地方{area}的区号为：{ans}")
        
        else:
            #.............................................
            #.............................................
            #.............................................
            #..................AI问答功能.................
            #.............................................
            #.............................................
            #.............................................
            for k,r in keyanswer.items():
                if k in message.content:
                    await message._api.post_group_message(group_openid=message.group_openid,
                                                    msg_type=0,
                                                    msg_id=message.id,
                                                    content=f"{r}")
                else:
                    api_key = "sk-5cd23846d4304f63b93db419bf87641e"  
                    model_name = "小板凳机器人"  
                    user_message = message.content  
                    with open('./temp/model.txt','r', encoding='utf-8') as f:
                        model=f.read()
                    with open('./temp/temp_message.txt', 'r', encoding='utf-8') as f:  
                        temp_message=(f.read())
                    #请求API答复
                    response = chat_with_deepseek(api_key, model_name, user_message, model,temp_message)  
                    if response:  
                        print(response)
                        answer=response.strip('**')
                        text="\
\n"+answer+"\
\n\n\
声明：以上内容为AI自动生成，仅供参考！"
                        temp_message=eval(temp_message)
                        temp_message.append({"role":"user","content":message.content})
                        temp_message.append({"role":"assistant","content":response})
                        temp_message=str(temp_message)
                        with open('./temp/temp_message.txt', 'w', encoding='utf-8') as file:  
                            file.write(str(temp_message))
                        try:
                            w=await message._api.post_group_message(group_openid=message.group_openid,
                                                            msg_type=0,
                                                            msg_id=message.id,
                                                            content=text)
                        except:
                            await message._api.post_group_message(group_openid=message.group_openid,
                                                            msg_type=0,
                                                            msg_id=message.id,
                                                            content="非常遗憾，我的回答可能被Tencent拦截了。\n\
请稍等约10秒，再发送“读取”重新尝试获取回答。")
                            api_key = "sk-5cd23846d4304f63b93db419bf87641e"  
                            model_name = "deepseek-chat"  
                            user_message = response+"\n\n请翻译以上内容为韩语！"  
                            moedel="请翻译提问者提供的文本"
                            response = chat_with_deepseek(api_key, model_name, user_message, model)  
                            if response:  
                                print(response)
                                with open('./temp/tryagain.txt', 'w', encoding='utf-8') as file:  
                                    file.write(response)  
                            
                    else:  
                        print("No response received.")
                        await message._api.post_group_message(group_openid=message.group_openid,
                                                        msg_type=0,
                                                        msg_id=message.id,
                                                        content=f"非常抱歉，程序报错。请联系管理员报告问题。")
                        

        
    async def on_c2c_message_create(self, message:Message):
        if "/新增提示词" in message.content:
            word=message.content.split('/新增提示词')[1]
            with open('./temp/model.txt', 'a',encoding='utf-8') as file:  
                file.write("\n"+word+"\n")
            await message._api.post_c2c_message(
                openid=message.author.user_openid, 
                msg_type=0, msg_id=message.id, 
                content=f"我收到了你的提示词：{word}"
            )


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
    client = MyClient(intents=intents)
    client.run(appid="102040950",secret="Pr9E9sPimeIoCg4K")
