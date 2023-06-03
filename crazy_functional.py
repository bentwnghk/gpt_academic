from toolbox import HotReload  # HotReload 的意思是热更新，修改函数插件后，不需要重启程序，代码直接生效


def get_crazy_functions():
    ###################### 第一组插件 ###########################
    from crazy_functions.读文章写摘要 import 读文章写摘要
    from crazy_functions.生成函数注释 import 批量生成函数注释
    from crazy_functions.解析项目源代码 import 解析项目本身
    from crazy_functions.解析项目源代码 import 解析一个Python项目
    from crazy_functions.解析项目源代码 import 解析一个C项目的头文件
    from crazy_functions.解析项目源代码 import 解析一个C项目
    from crazy_functions.解析项目源代码 import 解析一个Golang项目
    from crazy_functions.解析项目源代码 import 解析一个Rust项目
    from crazy_functions.解析项目源代码 import 解析一个Java项目
    from crazy_functions.解析项目源代码 import 解析一个前端项目
    from crazy_functions.高级功能函数模板 import 高阶功能模板函数
    from crazy_functions.代码重写为全英文_多线程 import 全项目切换英文
    from crazy_functions.Latex全文润色 import Latex英文润色
    from crazy_functions.询问多个大语言模型 import 同时问询
    from crazy_functions.解析项目源代码 import 解析一个Lua项目
    from crazy_functions.解析项目源代码 import 解析一个CSharp项目
    from crazy_functions.总结word文档 import 总结word文档
    from crazy_functions.解析JupyterNotebook import 解析ipynb文件
    from crazy_functions.对话历史存档 import 对话历史存档
    from crazy_functions.对话历史存档 import 载入对话历史存档
    from crazy_functions.对话历史存档 import 删除所有本地对话历史记录
    
    from crazy_functions.批量Markdown翻译 import Markdown英译中
    function_plugins = {
        "解析整個Python項目": {
            "Color": "stop",    # 按钮颜色
            "Function": HotReload(解析一个Python项目)
        },
        "載入對話歷史存檔（先上傳存檔或輸入路徑）": {
            "Color": "stop",
            "AsButton":False,
            "Function": HotReload(载入对话历史存档)
        },
        "刪除所有本地對話歷史記錄（請謹慎操作）": {
            "AsButton":False,
            "Function": HotReload(删除所有本地对话历史记录)
        },
        "[測試功能] 解析Jupyter Notebook文件": {
            "Color": "stop",
            "AsButton":False,
            "Function": HotReload(解析ipynb文件),
            "AdvancedArgs": True, # 调用时，唤起高级参数输入区（默认False）
            "ArgsReminder": "若輸入0，則不解析notebook中的Markdown塊", # 高级参数输入区的显示提示
        },
        "批量總結Word文檔": {
            "Color": "stop",
            "Function": HotReload(总结word文档)
        },
        "解析整個C++項目頭文件": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个C项目的头文件)
        },
        "解析整個C++項目（.cpp/.hpp/.c/.h）": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个C项目)
        },
        "解析整個Go項目": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个Golang项目)
        },
        "解析整個Rust項目": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个Rust项目)
        },
        "解析整個Java項目": {
            "Color": "stop",  # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个Java项目)
        },
        "解析整個前端項目（js,ts,css等）": {
            "Color": "stop",  # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个前端项目)
        },
        "解析整個Lua項目": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个Lua项目)
        },
        "解析整個CSharp項目": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个CSharp项目)
        },
        "讀Tex論文寫摘要": {
            "Color": "stop",    # 按钮颜色
            "Function": HotReload(读文章写摘要)
        },
        "Markdown/Readme英譯中": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "Function": HotReload(Markdown英译中)
        },
        "批量生成函數註釋": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(批量生成函数注释)
        },
        "保存當前的對話": {
            "Function": HotReload(对话历史存档)
        },
        "[多線程Demo] 解析此項目本身（源碼自譯解）": {
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析项目本身)
        },
        "[老舊的Demo] 把本項目源代碼切換成全英文": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(全项目切换英文)
        },
        "[插件demo] 歷史上的今天": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Function": HotReload(高阶功能模板函数)
        },

    }
    ###################### 第二组插件 ###########################
    # [第二组插件]: 经过充分测试
    from crazy_functions.批量总结PDF文档 import 批量总结PDF文档
    # from crazy_functions.批量总结PDF文档pdfminer import 批量总结PDF文档pdfminer
    from crazy_functions.批量翻译PDF文档_多线程 import 批量翻译PDF文档
    from crazy_functions.谷歌检索小助手 import 谷歌检索小助手
    from crazy_functions.理解PDF文档内容 import 理解PDF文档内容标准文件输入
    from crazy_functions.Latex全文润色 import Latex中文润色
    from crazy_functions.Latex全文润色 import Latex英文纠错
    from crazy_functions.Latex全文翻译 import Latex中译英
    from crazy_functions.Latex全文翻译 import Latex英译中
    from crazy_functions.批量Markdown翻译 import Markdown中译英

    function_plugins.update({
        "批量翻譯PDF文檔（多線程）": {
            "Color": "stop",
            "AsButton": True,  # 加入下拉菜单中
            "Function": HotReload(批量翻译PDF文档)
        },
        "詢問多個GPT模型": {
            "Color": "stop",    # 按钮颜色
            "Function": HotReload(同时问询)
        },
        "[測試功能] 批量總結PDF文檔": {
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Function": HotReload(批量总结PDF文档)
        },
        # "[測試功能] 批量總結PDF文檔pdfminer": {
        #    "Color": "stop",
        #    "AsButton": False,  # 加入下拉菜单中
        #    "Function": HotReload(批量总结PDF文档pdfminer)
        # },
        "谷歌學術檢索助手（輸入谷歌學術搜索頁url）": {
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(谷歌检索小助手)
        },

        "理解PDF文檔內容 （模仿ChatPDF）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(理解PDF文档内容标准文件输入)
        },
        "英文Latex項目全文潤色（輸入路徑或上傳壓縮包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex英文润色)
        },
        "英文Latex項目全文糾錯（輸入路徑或上傳壓縮包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex英文纠错)
        },
        "中文Latex項目全文潤色（輸入路徑或上傳壓縮包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex中文润色)
        },
        "Latex項目全文中譯英（輸入路徑或上傳壓縮包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex中译英)
        },
        "Latex項目全文英譯中（輸入路徑或上傳壓縮包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex英译中)
        },
        "批量Markdown中譯英（輸入路徑或上傳壓縮包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Markdown中译英)
        },


    })

    ###################### 第三组插件 ###########################
    # [第三组插件]: 尚未充分测试的函数插件

    try:
        from crazy_functions.下载arxiv论文翻译摘要 import 下载arxiv论文并翻译摘要
        function_plugins.update({
            "一鍵下載arxiv論文並翻譯摘要（先在input輸入編號，如1812.10695）": {
                "Color": "stop",
                "AsButton": False,  # 加入下拉菜单中
                "Function": HotReload(下载arxiv论文并翻译摘要)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.联网的ChatGPT import 连接网络回答问题
        function_plugins.update({
            "連接網絡回答問題（先輸入問題，再點擊按鈕，需要訪問谷歌）": {
                "Color": "stop",
                "AsButton": False,  # 加入下拉菜单中
                "Function": HotReload(连接网络回答问题)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.解析项目源代码 import 解析任意code项目
        function_plugins.update({
            "解析項目源代碼（手動指定和篩選源代碼文件類型）": {
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True, # 调用时，唤起高级参数输入区（默认False）
                "ArgsReminder": "輸入時用逗號隔開, *代表通配符, 加了^代表不匹配; 不輸入代表全部匹配。例如: \"*.c, ^*.cpp, config.toml, ^*.toml\"", # 高级参数输入区的显示提示
                "Function": HotReload(解析任意code项目)
            },
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.询问多个大语言模型 import 同时问询_指定模型
        function_plugins.update({
            "詢問多個GPT模型（手動指定詢問哪些模型）": {
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True, # 调用时，唤起高级参数输入区（默认False）
                "ArgsReminder": "支持任意數量的LLM接口，用&符號分隔，例如: gpt-3.5-turbo&stack-claude&newbing-free", # 高级参数输入区的显示提示
                "Function": HotReload(同时问询_指定模型)
            },
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.图片生成 import 图片生成
        function_plugins.update({
            "圖片生成（先切換模型到openai或api2d）": {
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True, # 调用时，唤起高级参数输入区（默认False）
                "ArgsReminder": "在這裡輸入分辨率, 如: 256x256（默認）", # 高级参数输入区的显示提示
                "Function": HotReload(图片生成)
            },
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.总结音视频 import 总结音视频
        function_plugins.update({
            "批量總結音視頻（輸入路徑或上傳壓縮包）": {
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "調用openai api 使用whisper-1模型, 目前支持的格式: mp4, m4a, wav, mpga, mpeg, mp3。此處可以輸入解析提示，例如：解析為繁體中文",
                "Function": HotReload(总结音视频)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.数学动画生成manim import 动画生成
        function_plugins.update({
            "數學動畫生成（Manim）": {
                "Color": "stop",
                "AsButton": False,
                "Function": HotReload(动画生成)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.批量Markdown翻译 import Markdown翻译指定语言
        function_plugins.update({
            "Markdown翻譯（手動指定語言）": {
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "請輸入要翻譯成哪種語言，默認為中文。",
                "Function": HotReload(Markdown翻译指定语言)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.Langchain知识库 import 知识库问答
        function_plugins.update({
            "[功能尚不穩定] 構建知識庫（請先上傳文件素材）": {
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "待注入的知識庫名稱id, 默認為default",
                "Function": HotReload(知识库问答)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.Langchain知识库 import 读取知识库作答
        function_plugins.update({
            "[功能尚不穩定] 知識庫問答": {
                "Color": "stop",
                "AsButton": False,
                "AdvancedArgs": True,
                "ArgsReminder": "待提取的知識庫名稱id, 默認為default, 您需要首先調用構建知識庫",
                "Function": HotReload(读取知识库作答)
            }
        })
    except:
        print('Load function plugin failed')

    try:
        from crazy_functions.Latex输出PDF结果 import Latex英文纠错加PDF对比
        function_plugins.update({
            "[功能尚不稳定] Latex英文纠错+LatexDiff高亮修正位置": {
                "Color": "stop",
                "AsButton": False,
                # "AdvancedArgs": True,
                # "ArgsReminder": "",
                "Function": HotReload(Latex英文纠错加PDF对比)
            }
        })
        from crazy_functions.Latex输出PDF结果 import Latex翻译中文并重新编译PDF
        function_plugins.update({
            "[功能尚不稳定] Latex翻译/Arixv翻译+重构PDF": {
                "Color": "stop",
                "AsButton": False,
                # "AdvancedArgs": True,
                # "ArgsReminder": "",
                "Function": HotReload(Latex翻译中文并重新编译PDF)
            }
        })
    except:
        print('Load function plugin failed')
    ###################### 第n组插件 ###########################
    return function_plugins
