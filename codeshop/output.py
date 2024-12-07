from time import sleep
import json
from codeshop.areacode import mareacode, mareaname
from codeshop.DeepSeek import chatlearning, chatsimple, chatgame


def arcode(areanum):
    area = areanum.split("查地方 ")[1]
    ans = str(mareacode(area))
    ans = ans.replace("[", "").replace("]", "")
    if "1000060" in ans:
        return "没有查到该区号，请确认区号是否正确，指令有无多余标点字符和空格。"
    else:
        return "区号" + area + "的对应地为: " + ans


def arname(areaname):
    area = areaname.split("查区号 ")[1]
    if "三沙" in area:
        ans = "0898"
    else:
        ans = str(mareaname(area))
        ans = ans.replace("[", "").replace("]", "")
    if "1000060" in ans:
        return "没有查到该地方，请确认地方是否正确，是否为地级行政区划正式名称，指令有无多余标点字符和空格。"
    else:
        return "地方 " + area + " 的区号为: " + ans


def check(value, my_dict):
    for key in my_dict:
        if value == key:
            return True
    return False


def tryagain(text):  # 给消息加密，躲避屏蔽词
    result = "".join(
        [char + "丿" if i < len(text) - 1 else char for i, char in enumerate(text)]
    )
    return result


def chat_body(content, key):
    # api_key = "sk-5cd23846d4304f63b93db419bf87641e"
    # api_key = "sk-846438feee1e41a08d644e86d1bc02c7"
    api_key = key  # 临时
    model_name = "deepseek-chat"
    user_message = content
    with open("./temp/model.txt", "r", encoding="utf-8") as f:
        model_chat = f.read()
    with open("./temp/temp_message.txt", "r", encoding="utf-8") as f:
        temp_message_chat = f.read()
    with open("./temp/model_game.txt", "r", encoding="utf-8") as f:
        model_game = f.read()
    with open("./temp/temp_message_game.json", "r", encoding="utf-8") as f:
        temp_message_game = json.load(f)
    # 分情况请求不同的API
    if "/游戏" in content:
        user_message = user_message.split("/游戏")[1]
        ans = chatgame(
            api_key, model_name, user_message, model_game, temp_message_game
        )
        response = "【游戏模式】\n" + ans
        game = True
    elif "维权" in content:
        ans = chatlearning(api_key, model_name, user_message, model_chat, temp_message_chat)
        response = ans
        game = False
    else:
        ans = chatsimple(api_key, model_name, user_message, model_chat, temp_message_chat)
        response = ans
        game = False
    print(response)
    if "机器人程序codeshop.DeepSeek出错" in response:
        ins = False
        return 0
    answer = after(response)
    if game == False:
        temp_message = eval(temp_message_chat)
        temp_message.append({"role": "user", "content": user_message})
        temp_message.append({"role": "assistant", "content": ans})
        with open("./temp/temp_message.txt", "w", encoding="utf-8") as file:
            file.write(str(temp_message))
        text = "\n" + answer + "\n\nPS：以上内容为AI自动生成，仅供参考。"
    else:
        temp_message_game.append({"role": "user", "content": user_message})
        temp_message_game.append({"role": "assistant", "content": ans})
        with open("./temp/temp_message_game.json", "w", encoding="utf-8") as file:
            json.dump(temp_message_game, file, ensure_ascii=False, indent=4)
        text = "\n" + answer + "\n\nPS：以上内容为AI自动生成，仅供娱乐，无实际意义。"
    return text


def after(text):
    # 对回答进行修改，以免被拦截
    answer = text.strip("**")
    if ".com" in answer:
        answer = answer.replace(".", "点")
    if ".cn" in answer:
        answer = answer.replace(".", "点")
    if "共产党" in answer:
        answer = answer.replace("共产党", "CPC")
    answer = answer.replace("**", " ").replace("#", " ")
    return answer
