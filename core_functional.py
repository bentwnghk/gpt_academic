# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er
import importlib
from toolbox import clear_line_break
from toolbox import apply_gpt_academic_string_mask_langbased
from toolbox import build_gpt_academic_masked_string_langbased
from textwrap import dedent

def get_core_functions():
    return {

        "學術語料潤色": {
            # [1*] 前缀字符串，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等。
            #      这里填一个提示词字符串就行了，这里为了区分中英文情景搞复杂了一点
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=
                                r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, "
                                r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. "
                                r"Firstly, you should provide the polished paragraph. "
                                r"Secondly, you should list all your modification and explain the reasons to do so in markdown table.",
                            text_show_chinese=
                                r"作為一名中文學術論文寫作改進助理，你的任務是改進所提供文本的拼寫、語法、清晰、簡潔和整體可讀性，"
                                r"同時分解長句，減少重復，並提供改進建議。請先提供文本的更正版本，然后在markdown表格中列出修改的內容，並給出修改的理由："
                        ) + "\n\n",
            # [2*] 后缀字符串，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":   r"",
            # [3] 按钮颜色 (可选参数，默认 secondary)
            "Color":    r"secondary",
            # [4] 按钮是否可见 (可选参数，默认 True，即可见)
            "Visible": True,
            # [5] 是否在触发时清除历史 (可选参数，默认 False，即不处理之前的对话历史)
            "AutoClearHistory": False,
            # [6] 文本预处理 （可选参数，默认 None，举例：写个函数移除所有的换行符）
            "PreProcess": None,
            # [7] 模型选择 （可选参数。如不设置，则使用当前全局模型；如设置，则用指定模型覆盖全局模型。）
            # "ModelOverride": "gpt-3.5-turbo", # 主要用途：强制点击此基础功能按钮时，使用指定的模型。
        },
        
        
        "總結繪製腦圖": {
            # 前缀，会被加在你的输入之前。例如，用来描述你的要求，例如翻译、解释代码、润色等等
            "Prefix":   '''"""\n\n''',
            # 后缀，会被加在你的输入之后。例如，配合前缀可以把你的输入内容用引号圈起来
            "Suffix":
                # dedent() 函数用于去除多行字符串的缩进
                dedent("\n\n"+r'''
                    """

                    使用mermaid flowchart對以上文本進行總結，概括上述段落的內容以及內在邏輯關系，例如：

                    以下是對以上文本的總結，以mermaid flowchart的形式展示：
                    ```mermaid
                    flowchart LR
                        A["節點名1"] --> B("節點名2")
                        B --> C{"節點名稱3"}
                        C --> D["節點名4"]
                        C --> |"箭頭名1"| E["節點名5"]
                        C --> |"箭頭名2"| F["節點名6"]
                    ```

                    注意：
                    （1）使用中文
                    （2）節點名字使用引號包裹，如["Laptop"]
                    （3）`|` 和 `"`之間不要存在空格
                    （4）根據情況選擇flowchart LR（從左到右）或flowchart TD（從上到下）
                '''),
        },
        
        
        "查找語法錯誤": {
            "Prefix":   r"Help me ensure that the grammar and the spelling is correct. "
                        r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good. "
                        r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, "
                        r"put the original text the first column, "
                        r"put the corrected text in the second column and highlight the key words you fixed. "
                        r"Finally, please provide the proofreaded text.""\n\n"
                        r"Example:""\n"
                        r"Paragraph: How is you? Do you knows what is it?""\n"
                        r"| Original sentence | Corrected sentence |""\n"
                        r"| :--- | :--- |""\n"
                        r"| How **is** you? | How **are** you? |""\n"
                        r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n\n"
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
        
        
        "學術英中互譯": {
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_chinese=
                                r"I want you to act as a scientific English-Chinese translator, "
                                r"I will provide you with some paragraphs in one language "
                                r"and your task is to accurately and academically translate the paragraphs only into the other language. "
                                r"Do not repeat the original provided paragraphs after translation. "
                                r"You should use artificial intelligence tools, "
                                r"such as natural language processing, and rhetorical knowledge "
                                r"and experience about effective writing techniques to reply. "
                                r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:",
                            text_show_english=
                                r"你是經驗豐富的翻譯，請把以下學術文章段落翻譯成中文，"
                                r"並同時充分考慮中文的語法、清晰、簡潔和整體可讀性，"
                                r"必要時，你可以修改整個句子的順序以確保翻譯后的段落符合中文的語言習慣。"
                                r"你需要翻譯的文本如下："
                        ) + "\n\n",
            "Suffix":   r"",
        },
        
        
        "英譯中": {
            "Prefix":   r"翻譯成道地的中文：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
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
            "Prefix":   r"我需要你找一張網路圖片。使用Unsplash API(https://source.unsplash.com/960x640/?<英文關鍵字>)取得圖片URL，"
                        r"然後請使用Markdown格式封裝，並且不要有反斜線，不要使用程式碼區塊。現在，請按以下描述給我發送圖片：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },
        
        
        "解釋代碼": {
            "Prefix":   r"請解釋以下代碼：" + "\n```\n",
            "Suffix":   "\n```\n",
            "Visible": False,
        },
        
        
        "參考文獻轉Bib": {
            "Prefix":   r"Here are some bibliography items, please transform them into bibtex style."
                        r"Note that, reference styles maybe more than one kind, you should transform each item correctly."
                        r"Items need to be transformed:" + "\n\n",
            "Visible":  False,
            "Suffix":   r"",
        }
    }


def handle_core_functionality(additional_fn, inputs, history, chatbot):
    import core_functional
    importlib.reload(core_functional)    # 热更新prompt
    core_functional = core_functional.get_core_functions()
    addition = chatbot._cookies['customize_fn_overwrite']
    if additional_fn in addition:
        # 自定义功能
        inputs = addition[additional_fn]["Prefix"] + inputs + addition[additional_fn]["Suffix"]
        return inputs, history
    else:
        # 预制功能
        if "PreProcess" in core_functional[additional_fn]:
            if core_functional[additional_fn]["PreProcess"] is not None:
                inputs = core_functional[additional_fn]["PreProcess"](inputs)  # 获取预处理函数（如果有的话）
        # 为字符串加上上面定义的前缀和后缀。
        inputs = apply_gpt_academic_string_mask_langbased(
            string = core_functional[additional_fn]["Prefix"] + inputs + core_functional[additional_fn]["Suffix"],
            lang_reference = inputs,
        )
        if core_functional[additional_fn].get("AutoClearHistory", False):
            history = []
        return inputs, history

if __name__ == "__main__":
    t = get_core_functions()["總結繪製腦圖"]
    print(t["Prefix"] + t["Suffix"])