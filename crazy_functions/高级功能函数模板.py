from toolbox import CatchException, update_ui
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import datetime, re

@CatchException
def 高阶功能模板函数(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             输入栏用户输入的文本，例如需要翻译的一段话，再例如一个包含了待处理文件的路径
    llm_kwargs      gpt模型参数，如温度和top_p等，一般原样传递下去就行
    plugin_kwargs   插件模型的参数，暂时没有用武之地
    chatbot         聊天显示框的句柄，用于显示给用户
    history         聊天历史，前情提要
    system_prompt   给gpt的静默提醒
    web_port        当前软件运行的端口号
    """
    history = []    # 清空历史，以免输入溢出
    chatbot.append(("這是什麼功能？", "[Local Message] 請注意，您正在調用一個[函數插件]的模板，該函數面向希望實現更多有趣功能的開發者，它可以作為創建新功能函數的模板（該函數只有20多行代碼）。"))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 由于请求gpt需要一段时间，我们先及时地做一次界面更新
    for i in range(5):
        currentMonth = (datetime.date.today() + datetime.timedelta(days=i)).month
        currentDay = (datetime.date.today() + datetime.timedelta(days=i)).day
        i_say = f'歷史中哪些事件發生在{currentMonth}月{currentDay}日？用中文列舉兩條，然後分別給出描述事件的兩個英文單詞。' + '當你給出關鍵詞時，使用以下json格式：{"Keywords":[EnglishKeyWord1,EnglishKeyWord2]}。'
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say, 
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=[], 
            sys_prompt='輸出格式示例：1908年，美國消防救援事業發展的“美國消防協會”成立。關鍵詞：{"Keywords":["Fire","American"]}。'
        )
        gpt_say = get_images(gpt_say)
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 界面更新


def get_images(gpt_say):
    def get_image_by_keyword(keyword):
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(f'https://wallhaven.cc/search?q={keyword}', timeout=2)
        for image_element in BeautifulSoup(response.content, 'html.parser').findAll("img"):
            if "data-src" in image_element: break
        return image_element["data-src"]

    for keywords in re.findall('{"KeyWords":\[(.*?)\]}', gpt_say):
        keywords = [n.strip('"') for n in keywords.split(',')]
        try:
            description = keywords[0]
            url = get_image_by_keyword(keywords[0])
            img_tag = f"\n\n![{description}]({url})"
            gpt_say += img_tag
        except:
            continue
    return gpt_say