from toolbox import CatchException, update_ui
from crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import datetime

高阶功能模板函数示意图 = f"""
```mermaid
flowchart TD
    %% <gpt_academic_hide_mermaid_code> 一个特殊标记，用于在生成mermaid图表时隐藏代码块
    subgraph 函数调用["函数调用过程"]
        AA["输入栏用户输入的文本(txt)"] --> BB["gpt模型参数(llm_kwargs)"]
        BB --> CC["插件模型参数(plugin_kwargs)"]
        CC --> DD["对话显示框的句柄(chatbot)"]
        DD --> EE["对话历史(history)"]
        EE --> FF["系统提示词(system_prompt)"]
        FF --> GG["当前用户信息(web_port)"]

        A["开始(查询5天历史事件)"]
        A --> B["获取当前月份和日期"]
        B --> C["生成历史事件查询提示词"]
        C --> D["调用大模型"]
        D --> E["更新界面"]
        E --> F["记录历史"]
        F --> |"下一天"| B
    end
```
"""

@CatchException
def 高阶功能模板函数(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    # 高阶功能模板函数示意图：https://mermaid.live/edit#pako:eNptk1tvEkEYhv8KmattQpvlvOyFCcdeeaVXuoYssBwie8gyhCIlqVoLhrbbtAWNUpEGUkyMEDW2Fmn_DDOL_8LZHdOwxrnamX3f7_3mmZk6yKhZCfAgV1KrmYKoQ9fDuKC4yChX0nld1Aou1JzjznQ5fWmejh8LYHW6vG2a47YAnlCLNSIRolnenKBXI_zRIBrcuqRT890u7jZx7zMDt-AaMbnW1--5olGiz2sQjwfoQxsZL0hxplSSU0-rop4vrzmKR6O2JxYjHmwcL2Y_HDatVMkXlf86YzHbGY9bO5j8XE7O8Nsbc3iNB3ukL2SMcH-XIQBgWoVOZzxuOxOJOyc63EPGV6ZQLENVrznViYStTiaJ2vw2M2d9bByRnOXkgCnXylCSU5quyto_IcmkbdvctELmJ-j1ASW3uB3g5xOmKqVTmqr_Na3AtuS_dtBFm8H90XJyHkDDT7S9xXWb4HGmRChx64AOL5HRpUm411rM5uh4H78Z4V7fCZzytjZz2seto9XaNPFue07clLaVZF8UNLygJ-VES8lah_n-O-5Ozc7-77NzJ0-K0yr0ZYrmHdqAk50t2RbA4qq9uNohBASw7YpSgaRkLWCCAtxAlnRZLGbJba9bPwUAC5IsCYAnn1kpJ1ZKUACC0iBSsQLVBzUlA3ioVyQ3qGhZEUrxokiehAz4nFgqk1VNVABfB1uAD_g2_AGPl-W8nMcbCvsDblADfNCz4feyobDPy3rYEMtxwYYbPFNVUoHdCPmDHBv2cP4AMfrCbiBli-Q-3afv0X6WdsIjW2-10fgDy1SAig

    txt             输入栏用户输入的文本，例如需要翻译的一段话，再例如一个包含了待处理文件的路径
    llm_kwargs      gpt模型参数，如温度和top_p等，一般原样传递下去就行
    plugin_kwargs   插件模型的参数，用于灵活调整复杂功能的各种参数
    chatbot         聊天显示框的句柄，用于显示给用户
    history         聊天历史，前情提要
    system_prompt   给gpt的静默提醒
    user_request    当前用户的请求信息（IP地址等）
    """
    history = []    # 清空历史，以免输入溢出
    chatbot.append((
        "您正在調用插件：歷史上的今天", 
        "[Local Message] 請注意，您正在調用一個[函數插件]的模板，該函數面向希望實現更多有趣功能的開發者，它可以作為創建新功能函數的模板（該函數隻有20多行代碼）。此外我們也提供可同步處理大量文件的多線程Demo供您參考。您若希望分享新的功能模組，請不吝PR！" + 高階功能模板函數示意圖))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 由于请求gpt需要一段时间，我们先及时地做一次界面更新
    for i in range(5):
        currentMonth = (datetime.date.today() + datetime.timedelta(days=i)).month
        currentDay = (datetime.date.today() + datetime.timedelta(days=i)).day
        i_say = f'歷史中哪些事件發生在{currentMonth}月{currentDay}日？列舉兩條並發送相關圖片。發送圖片時，請使用Markdown，將Unsplash API中的PUT_YOUR_QUERY_HERE替換成描述該事件的一個最重要的單詞。'
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say, 
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=[], 
            sys_prompt="當你想發送一張照片時，請使用Markdown, 並且不要有反斜線, 不要用代碼塊。使用 Unsplash API (https://source.unsplash.com/1280x720/? < PUT_YOUR_QUERY_HERE >)。"
        )
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 界面更新




PROMPT = """
请你给出围绕“{subject}”的逻辑关系图，使用mermaid语法，mermaid语法举例：
```mermaid
graph TD
    P(编程) --> L1(Python)
    P(编程) --> L2(C)
    P(编程) --> L3(C++)
    P(编程) --> L4(Javascipt)
    P(编程) --> L5(PHP)
```
"""
@CatchException
def 测试图表渲染(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    txt             输入栏用户输入的文本，例如需要翻译的一段话，再例如一个包含了待处理文件的路径
    llm_kwargs      gpt模型参数，如温度和top_p等，一般原样传递下去就行
    plugin_kwargs   插件模型的参数，用于灵活调整复杂功能的各种参数
    chatbot         聊天显示框的句柄，用于显示给用户
    history         聊天历史，前情提要
    system_prompt   给gpt的静默提醒
    user_request    当前用户的请求信息（IP地址等）
    """
    history = []    # 清空历史，以免输入溢出
    chatbot.append(("这是什么功能？", "一个测试mermaid绘制图表的功能，您可以在输入框中输入一些关键词，然后使用mermaid+llm绘制图表。"))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 由于请求gpt需要一段时间，我们先及时地做一次界面更新

    if txt == "": txt = "空白的输入栏" # 调皮一下

    i_say_show_user = f'请绘制有关“{txt}”的逻辑关系图。'
    i_say = PROMPT.format(subject=txt)
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say,
        inputs_show_user=i_say_show_user,
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=[],
        sys_prompt=""
    )
    history.append(i_say); history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 界面更新