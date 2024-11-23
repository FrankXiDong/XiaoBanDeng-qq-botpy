import os,json,time,random,requests,ast,urllib
from time import sleep
from openai import OpenAI
from urllib.parse import urlencode
from urllib.request import urlopen
from codeshop.areacode import mareacode,mareaname
from codeshop.locknum import locknum
from codeshop.game import joingame,startgame
from codeshop.balance import balance
from codeshop.DeepSeek import chatlearning,chatsimple
def arcode(areanum):
    area=areanum.split('查地方 ')[1]
    ans=str(mareacode(area))
    ans=ans.replace('[','').replace(']','')
    if "1000060" in ans:
        return "没有查到该区号，请确认区号是否正确，指令有无多余标点字符和空格。"
    else:
        return "区号"+area+"的对应地为: "+ans
def arname(areaname):
    area=areaname.split('查区号 ')[1]
    if "三沙" in area:
        ans="0898"
    else:
        ans=str(mareaname(area))
        ans=ans.replace('[','').replace(']','')
    if "1000060" in ans:
        return "没有查到该地方，请确认地方是否正确，是否为地级行政区划正式名称，指令有无多余标点字符和空格。"
    else:
        return "地方 "+area+" 的区号为: "+ans
def check(value, my_dict):
    for key in my_dict:
        if value == key:
            return True
    return False
def tryagain(text): #给消息加密，躲避屏蔽词
    result = ''.join([char + '丿' if i < len(text) - 1 else char for i, char in enumerate(text)])  
    return result
def chat_body(content):
    #api_key = "sk-5cd23846d4304f63b93db419bf87641e"  
    api_key = "sk-d6af0c89a1f44195beec9213074f52b7" #临时
    model_name = "deepseek-chat"  
    user_message = content 
    with open('./temp/model.txt','r', encoding='utf-8') as f:
        model=f.read()
    with open('./temp/temp_message.txt', 'r', encoding='utf-8') as f:  
        temp_message=f.read()
    #分情况请求不同的API
    if "维权" in content:
        response = chatlearning(api_key, model_name, user_message, model,temp_message) 
    else:
        response = chatsimple(api_key, model_name, user_message, model,temp_message)  
    print(response)
    if "程序出错" in response:
        ins=False
        return 0
    #对回答进行修改，以免被拦截
    answer=response.strip('**')
    if ".com"in answer:
        answer=answer.replace(".","点")
    if ".cn"in answer:
        answer=answer.replace(".","点")
    if "共产党"in answer:
        answer=answer.replace("共产党","CPC") 
    answer=answer.replace("**"," ").replace("#"," ")        
    text="\n"+answer+"\n\n声明：以上内容为AI自动生成，仅供参考！\n注：小板凳智能助手已经升级6.1版本了，欢迎大家体验！"
    temp_message=eval(temp_message)
    temp_message.append({"role":"user","content":user_message})
    temp_message.append({"role":"assistant","content":answer})
    temp_message=str(temp_message)
    with open('./temp/temp_message.txt', 'w', encoding='utf-8') as file:  
        file.write(str(temp_message))
    return text