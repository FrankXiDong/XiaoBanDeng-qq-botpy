import os, json, botpy, time, random, requests, ast, urllib, datetime
from botpy import logging, logger, message, BotAPI
from botpy.message import DirectMessage, Message, GroupMessage
from botpy.ext.cog_yaml import read
from botpy.types.message import Reference
from botpy.types.announce import AnnouncesType
from botpy.forum import Thread
from botpy.types.forum import Post, Reply, AuditResult
from botpy.types.channel import ChannelSubType, ChannelType
from time import sleep
from codeshop.locknum import locknum
from codeshop.game import joingame, startgame
from codeshop.balance import balance
from codeshop.output import arcode, arname, tryagain, chat_body
from botpy.audio import Audio
import asyncio

_log = logging.get_logger()
keyanswer = {
    "test": "你在测试什么？",
    "你是哪个省的": "妈妈生的（误）",
}
json_data = {}
version = ""


class MyClient(botpy.Client):

    async def on_ready(self):  # 初次启动时
        global version
        with open("./temp/version.txt", "r", encoding="utf-8") as file:
            version=file.read()
        start_txt = "\
-----------启动成功------------\n\
    小板凳频道管家，启动！\n\
    版本:"+version
        print(start_txt)



    async def on_group_at_message_create(self, message: GroupMessage):  # 收到群消息时
        print(message)
        global json_data
        dataid = eval(str(message.author))
        open_id = dataid["member_openid"]  # 获取open_id
        result = False
        if "查询余额" in message.content:
            key = json_data["ai"]["chat 02"]["key"]
            data = balance(key=key)
            result = "剩余的余额为：" + data + "元人民币。"
        elif "查地方 " in message.content:
            result = arcode(message.content)
        elif "查区号 " in message.content:
            result = arname(message.content)
        elif "/游戏" in message.content:
            result = "功能暂未开发，敬请期待！"
        await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=f"{result}",
                )
                


if __name__ == "__main__":
    intents = botpy.Intents.none()
    intents.public_guild_messages = True
    intents.direct_message = True
    intents.guilds = True
    intents.guild_messages = True
    intents.guild_members = True
    intents.interaction = True
    intents.guild_message_reactions = True
    intents.forums = True
    intents.public_messages = True
    # intents = botpy.Intents(public_guild_messages=True, direct_message=True, guilds=True)
    with open("../config.json", "r", encoding="utf-8") as fp:
        json_data = json.load(fp)
        appid = json_data["bot"]["appid"]
        secret = json_data["bot"]["secret"]
    client = MyClient(intents=intents, timeout=8)
    client.run(appid=appid, secret=secret)
