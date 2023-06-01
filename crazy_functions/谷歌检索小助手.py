from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from toolbox import CatchException, report_execption, write_results_to_file
from toolbox import update_ui

def get_meta_information(url, chatbot, history):
    import requests
    import arxiv
    import difflib
    from bs4 import BeautifulSoup
    from toolbox import get_conf
    proxies, = get_conf('proxies')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    # 发送 GET 请求
    response = requests.get(url, proxies=proxies, headers=headers)

    # 解析网页内容
    soup = BeautifulSoup(response.text, "html.parser")

    def string_similar(s1, s2):
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

    profile = []
    # 获取所有文章的标题和作者
    for result in soup.select(".gs_ri"):
        title = result.a.text.replace('\n', ' ').replace('  ', ' ')
        author = result.select_one(".gs_a").text
        try:
            citation = result.select_one(".gs_fl > a[href*='cites']").text  # 引用次数是链接中的文本，直接取出来
        except:
            citation = 'cited by 0'
        abstract = result.select_one(".gs_rs").text.strip()  # 摘要在 .gs_rs 中的文本，需要清除首尾空格
        search = arxiv.Search(
            query = title,
            max_results = 1,
            sort_by = arxiv.SortCriterion.Relevance,
        )
        try:
            paper = next(search.results())
            if string_similar(title, paper.title) > 0.90: # same paper
                abstract = paper.summary.replace('\n', ' ')
                is_paper_in_arxiv = True
            else:   # different paper
                abstract = abstract
                is_paper_in_arxiv = False
            paper = next(search.results())
        except:
            abstract = abstract
            is_paper_in_arxiv = False
        print(title)
        print(author)
        print(citation)
        profile.append({
            'title':title,
            'author':author,
            'citation':citation,
            'abstract':abstract,
            'is_paper_in_arxiv':is_paper_in_arxiv,
        })

        chatbot[-1] = [chatbot[-1][0], title + f'\n\n是否在arxiv中（不在arxiv中無法獲取完整摘要）:{is_paper_in_arxiv}\n\n' + abstract]
        yield from update_ui(chatbot=chatbot, history=[]) # 刷新界面
    return profile

@CatchException
def 谷歌检索小助手(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # 基本信息：功能、贡献者
    chatbot.append([
        "函數插件功能？",
        "分析用戶提供的谷歌學術（google scholar）搜索頁面中，出現的所有文章: binary-husky，插件初始化中..."])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import arxiv
        import math
        from bs4 import BeautifulSoup
    except:
        report_execption(chatbot, history, 
            a = f"解析項目: {txt}", 
            b = f"導入軟件依賴失敗。使用該模塊需要額外依賴，安裝方法```pip install --upgrade beautifulsoup4 arxiv```。")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 清空历史，以免输入溢出
    history = []
    meta_paper_info_list = yield from get_meta_information(txt, chatbot, history)
    batchsize = 5
    for batch in range(math.ceil(len(meta_paper_info_list)/batchsize)):
        if len(meta_paper_info_list[:batchsize]) > 0:
            i_say = "下面是一些學術文獻的數據，提取出以下內容：" + \
            "1、英文題目；2、中文題目翻譯；3、作者；4、arxiv公開（is_paper_in_arxiv）；4、引用數量（cite）；5、中文摘要翻譯。" + \
            f"以下是信息源：{str(meta_paper_info_list[:batchsize])}" 

            inputs_show_user = f"請分析此頁面中出現的所有文章：{txt}，這是第{batch+1}批"
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, inputs_show_user=inputs_show_user,
                llm_kwargs=llm_kwargs, chatbot=chatbot, history=[],
                sys_prompt="你是一個學術翻譯，請從數據中提取信息。你必須使用Markdown表格。你必須逐個文獻進行處理。"
            )

            history.extend([ f"第{batch+1}批", gpt_say ])
            meta_paper_info_list = meta_paper_info_list[batchsize:]

    chatbot.append(["狀態？", 
        "已經全部完成，您可以試試讓AI寫一個Related Works，例如您可以繼續輸入Write a \"Related Works\" section about \"你搜索的研究領域\" for me."])
    msg = '正常'
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
    res = write_results_to_file(history)
    chatbot.append(("完成了嗎？", res)); 
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
