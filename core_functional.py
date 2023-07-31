# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er
import importlib
from toolbox import clear_line_break


def get_core_functions():
    return {
        "英語學術潤色": {
            # 前缀，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等
            "Prefix":   r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                        r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. " +
                        r"Furthermore, list all modification and explain the reasons to do so in markdown table." + "\n\n",
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":   r"",
            # 按钮颜色 (默认 secondary)
            "Color":    r"secondary",
            # 按钮是否可见 (默认 True，即可见)
            "Visible": True,
            # 是否在触发时清除历史 (默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False
        },
        "中文學術潤色": {
            "Prefix":   r"作為一名中文學術論文寫作改進助理，你的任務是改進所提供文本的拼寫、語法、清晰、簡潔和整體可讀性，" +
                        r"同時分解長句，減少重複，並提供改進建議。請只提供文本的更正版本，避免包括解釋。請編輯以下文本" + "\n\n",
            "Suffix":   r"",
        },
        "查找語法錯誤": {
            "Prefix":   r"Can you help me ensure that the grammar and the spelling is correct? " +
                        r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good." +
                        r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, " +
                        r"put the original text the first column, " +
                        r"put the corrected text in the second column and highlight the key words you fixed.""\n"
                        r"Example:""\n"
                        r"Paragraph: How is you? Do you knows what is it?""\n"
                        r"| Original sentence | Corrected sentence |""\n"
                        r"| :--- | :--- |""\n"
                        r"| How **is** you? | How **are** you? |""\n"
                        r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n"
                        r"Below is a paragraph from an academic paper. "
                        r"You need to report all grammar and spelling mistakes as the example before."
                        + "\n\n",
            "Suffix":   r"",
            "PreProcess": clear_line_break,    # 预处理：清除换行符
        },
        "中譯英": {
            "Prefix":   r"Please translate following sentence to English:" + "\n\n",
            "Suffix":   r"",
        },
        "學術中英互譯": {
            "Prefix":   r"I want you to act as a scientific English-Chinese translator, " +
                        r"I will provide you with some paragraphs in one language " +
                        r"and your task is to accurately and academically translate the paragraphs only into the other language. " +
                        r"Do not repeat the original provided paragraphs after translation. " +
                        r"You should use artificial intelligence tools, " +
                        r"such as natural language processing, and rhetorical knowledge " +
                        r"and experience about effective writing techniques to reply. " +
                        r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:" + "\n\n",
            "Suffix": "",
            "Color": "secondary",
        },
        "英譯中": {
            "Prefix":   r"翻譯成地道的中文：" + "\n\n",
            "Suffix":   r"",
        },
        "閱讀理解練習": {
            "Prefix":   r"I want you to act as a reading comprehension exercise generator. " +
                        r"Write a passage on my requested topic and formulate 8 MCQs to test students' understanding of the passage. " +
                        r"The types of questions you ask may include literal, inference, evaluation, application, analysis, synthesis, vocabulary, summary, and reference questions. " +
                        r"Finally, provide the correct answers at the end of the test. " +
                        r"Now, please start by asking me for a topic, the desired length of the passage, and the level of difficulty of the words to be used in the passage." + "\n\n",
            "Suffix":   r"",
        },
        "找圖片": {
            "Prefix":   r"我需要你找一張網絡圖片。使用Unsplash API(https://source.unsplash.com/960x640/?<英語關鍵詞>)獲取圖片URL，" +
                        r"然後請使用Markdown格式封裝，並且不要有反斜線，不要用代碼塊。現在，請按以下描述給我發送圖片：" + "\n\n",
            "Suffix":   r"",
            "Visible": False,
        },
        "解釋代碼": {
            "Prefix":   r"請解釋以下代碼：" + "\n```\n",
            "Suffix":   "\n```\n",
            "Visible": False,
        },
        "參考文獻轉Bib": {
            "Prefix":   r"Here are some bibliography items, please transform them into bibtex style." +
                        r"Note that, reference styles maybe more than one kind, you should transform each item correctly." +
                        r"Items need to be transformed:",
            "Suffix":   r"",
        }
    }


def handle_core_functionality(additional_fn, inputs, history, chatbot):
    import core_functional
    importlib.reload(core_functional)    # 热更新prompt
    core_functional = core_functional.get_core_functions()
    if "PreProcess" in core_functional[additional_fn]: inputs = core_functional[additional_fn]["PreProcess"](inputs)  # 获取预处理函数（如果有的话）
    inputs = core_functional[additional_fn]["Prefix"] + inputs + core_functional[additional_fn]["Suffix"]
    if core_functional[additional_fn].get("AutoClearHistory", False):
        history = []
    return inputs, history
