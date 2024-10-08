from loguru import logger
from toolbox import update_ui
from toolbox import CatchException, report_exception
from toolbox import write_history_to_file, promote_file_to_downloadzone
from crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive

def 生成函数注释(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, os
    logger.info('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()

        i_say = f'请对下面的程序文件做一个概述，并对文件中的所有函数生成注释，使用markdown表格输出结果，文件名是{os.path.relpath(fp, project_folder)}，文件内容是 ```{file_content}```'
        i_say_show_user = f'[{index+1}/{len(file_manifest)}] 请对下面的程序文件做一个概述，并对文件中的所有函数生成注释: {os.path.abspath(fp)}'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

        msg = '正常'
        # ** gpt request **
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            i_say, i_say_show_user, llm_kwargs, chatbot, history=[], sys_prompt=system_prompt)   # 带超时倒计时

        chatbot[-1] = (i_say_show_user, gpt_say)
        history.append(i_say_show_user); history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
        time.sleep(2)

    res = write_history_to_file(history)
    promote_file_to_downloadzone(res, chatbot=chatbot)
    chatbot.append(("完成了吗？", res))
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面



@CatchException
def 批量生成函数注释(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    history = []    # 清空历史，以免输入溢出
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = '空空如也的輸入欄'
        report_execption(chatbot, history, a = f"解析項目: {txt}", b = f"找不到本地項目或無權訪問: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.py', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)]

    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"解析項目: {txt}", b = f"找不到任何.tex文件: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    yield from 生成函数注释(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
