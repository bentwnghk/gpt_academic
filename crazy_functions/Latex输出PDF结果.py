from toolbox import update_ui, trimmed_format_exc, get_conf, objdump, objload
from toolbox import CatchException, report_execption, update_ui_lastest_msg, zip_result, gen_time_str
import glob, os, requests, time
pj = os.path.join

# =================================== 工具函数 ===============================================
沙雕GPT啊别犯这些低级翻译错误  = 'You must translate "agent" into "智能體". '
def switch_prompt(pfg, mode):
    """
    Generate prompts and system prompts based on the mode for proofreading or translating.
    Args:
    - pfg: Proofreader or Translator instance.
    - mode: A string specifying the mode, either 'proofread' or 'translate_zh'.

    Returns:
    - inputs_array: A list of strings containing prompts for users to respond to.
    - sys_prompt_array: A list of strings containing prompts for system prompts.
    """
    n_split = len(pfg.sp_file_contents)
    if mode == 'proofread':
        inputs_array = [r"Below is a section from an academic paper, proofread this section." + 
                        r"Do not modify any latex command such as \section, \cite, \begin, \item and equations. " + 
                        r"Answer me only with the revised text:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        sys_prompt_array = ["You are a professional academic paper writer." for _ in range(n_split)]
    elif mode == 'translate_zh':
        inputs_array = [r"Below is a section from an English academic paper, translate it into Chinese." + 沙雕GPT啊别犯这些低级翻译错误 + 
                        r"Do not modify any latex command such as \section, \cite, \begin, \item and equations. " + 
                        r"Answer me only with the translated text:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        sys_prompt_array = ["You are a professional translator." for _ in range(n_split)]
    else:
        assert False, "未知指令"
    return inputs_array, sys_prompt_array

def desend_to_extracted_folder_if_exist(project_folder):
    """ 
    Descend into the extracted folder if it exists, otherwise return the original folder.

    Args:
    - project_folder: A string specifying the folder path.

    Returns:
    - A string specifying the path to the extracted folder, or the original folder if there is no extracted folder.
    """
    maybe_dir = [f for f in glob.glob(f'{project_folder}/*') if os.path.isdir(f)]
    if len(maybe_dir) == 0: return project_folder
    if maybe_dir[0].endswith('.extract'): return maybe_dir[0]
    return project_folder

def move_project(project_folder):
    """ 
    Create a new work folder and copy the project folder to it.

    Args:
    - project_folder: A string specifying the folder path of the project.

    Returns:
    - A string specifying the path to the new work folder.
    """
    import shutil, time
    time.sleep(2)   # avoid time string conflict
    new_workfolder = f'gpt_log/{gen_time_str()}'
    shutil.copytree(src=project_folder, dst=new_workfolder)
    return new_workfolder

def arxiv_download(chatbot, history, txt):
    if not txt.startswith('https://arxiv.org'): 
        return txt
    
    # <-------------- inspect format ------------->
    chatbot.append([f"檢測到arxiv文檔連接", '嘗試下載 ...']) 
    yield from update_ui(chatbot=chatbot, history=history)
    time.sleep(1) # 刷新界面

    url_ = txt   # https://arxiv.org/abs/1707.06690
    if not txt.startswith('https://arxiv.org/abs/'): 
        msg = f"解析arxiv網址失敗, 期望格式例如: https://arxiv.org/abs/1707.06690。實際得到格式: {url_}"
        yield from update_ui_lastest_msg(msg, chatbot=chatbot, history=history) # 刷新界面
        return msg
    
    # <-------------- set format ------------->
    arxiv_id = url_.split('/abs/')[-1]
    url_tar = url_.replace('/abs/', '/e-print/')
    download_dir = './gpt_log/arxiv/'
    os.makedirs(download_dir, exist_ok=True)
    
    # <-------------- download arxiv source file ------------->
    dst = pj(download_dir, arxiv_id+'.tar')
    if os.path.exists(dst):
        yield from update_ui_lastest_msg("調用緩存", chatbot=chatbot, history=history)  # 刷新界面
    else:
        yield from update_ui_lastest_msg("開始下載", chatbot=chatbot, history=history)  # 刷新界面
        proxies, = get_conf('proxies')
        r = requests.get(url_tar, proxies=proxies)
        with open(dst, 'wb+') as f:
            f.write(r.content)
    # <-------------- extract file ------------->
    yield from update_ui_lastest_msg("下載完成", chatbot=chatbot, history=history)  # 刷新界面
    from toolbox import extract_archive
    extract_dst = f'gpt_log/{gen_time_str()}'
    extract_archive(file_path=dst, dest_dir=extract_dst)
    return extract_dst
# ========================================= 插件主程序1 =====================================================    


@CatchException
def Latex英文纠错加PDF对比(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # <-------------- information about this plugin ------------->
    chatbot.append([ "函數插件功能？",
        "對整個Latex項目進行糾錯, 用latex編譯為PDF對修正處做高亮。函數插件貢獻者: Binary-Husky。注意事項: 目前僅支持GPT3.5/GPT4，其他模型轉化效果未知。目前對機器學習類文獻轉化效果最好，其他類型文獻轉化效果未知。僅在Windows系統進行了測試，其他操作系統表現未知。"])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面


    # <-------------- check deps ------------->
    try:
        import glob, os, time
        os.system(f'pdflatex -version')
        from .latex_utils import Latex精细分解与转化, 编译Latex差别
    except Exception as e:
        chatbot.append([ f"解析項目: {txt}",
            f"嘗試執行Latex指令失敗。 Latex沒有安裝, 或者不在環境變量PATH中。報錯信息\n\n```\n\n{trimmed_format_exc()}\n\n```\n\n"])
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    

    # <-------------- clear history and read input ------------->
    history = []
    txt = yield from arxiv_download(chatbot, history, txt)
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = '空空如也的輸入欄'
        report_execption(chatbot, history, a = f"解析項目: {txt}", b = f"找不到本地項目或無權訪問: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"解析項目: {txt}", b = f"找不到任何.tex文件: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    

    # <-------------- if is a zip/tar file ------------->
    project_folder = desend_to_extracted_folder_if_exist(project_folder)


    # <-------------- move latex project away from temp folder ------------->
    project_folder = move_project(project_folder)


    # <-------------- if merge_translate_zh is already generated, skip gpt req ------------->
    if not os.path.exists(project_folder + '/merge_proofread.tex'):
        yield from Latex精细分解与转化(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, mode='proofread_latex', switch_prompt=switch_prompt)


    # <-------------- compile PDF ------------->
    success = yield from 编译Latex差别(chatbot, history, main_file_original='merge', main_file_modified='merge_proofread', 
                             work_folder_original=project_folder, work_folder_modified=project_folder, work_folder=project_folder)
    

    # <-------------- zip PDF ------------->
    zip_result(project_folder)
    if success:
        chatbot.append((f"成功啦", '請查收結果（壓縮包）...'))
        yield from update_ui(chatbot=chatbot, history=history); time.sleep(1) # 刷新界面
    else:
        chatbot.append((f"失敗了", '雖然PDF生成失敗了, 但請查收結果（壓縮包）, 內含已經翻譯的Tex文檔, 也是可讀的, 您可以到Github Issue區, 用該壓縮包+對話歷史存檔進行反饋 ...'))
        yield from update_ui(chatbot=chatbot, history=history); time.sleep(1) # 刷新界面

    # <-------------- we are done ------------->
    return success


# ========================================= 插件主程序2 =====================================================    

@CatchException
def Latex翻译中文并重新编译PDF(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # <-------------- information about this plugin ------------->
    chatbot.append([
        "函數插件功能？",
        "對整個Latex項目進行翻譯, 生成中文PDF。函數插件貢獻者: Binary-Husky。注意事項: 目前僅支持GPT3.5/GPT4，其他模型轉化效果未知。目前對機器學習類文獻轉化效果最好，其他類型文獻轉化效果未知。僅在Windows系統進行了測試，其他操作系統表現未知。"])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面


    # <-------------- check deps ------------->
    try:
        import glob, os, time
        os.system(f'pdflatex -version')
        from .latex_utils import Latex精细分解与转化, 编译Latex差别
    except Exception as e:
        chatbot.append([ f"解析項目: {txt}",
            f"嘗試執行Latex指令失敗。Latex沒有安裝, 或者不在環境變量PATH中。報錯信息\n\n```\n\n{trimmed_format_exc()}\n\n```\n\n"])
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    

    # <-------------- clear history and read input ------------->
    history = []
    txt = yield from arxiv_download(chatbot, history, txt)
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = '空空如也的輸入欄'
        report_execption(chatbot, history, a = f"解析項目: {txt}", b = f"找不到本地項目或無權訪問: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"解析項目: {txt}", b = f"找不到任何.tex文件: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    

    # <-------------- if is a zip/tar file ------------->
    project_folder = desend_to_extracted_folder_if_exist(project_folder)


    # <-------------- move latex project away from temp folder ------------->
    project_folder = move_project(project_folder)


    # <-------------- if merge_translate_zh is already generated, skip gpt req ------------->
    if not os.path.exists(project_folder + '/merge_translate_zh.tex'):
        yield from Latex精细分解与转化(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, mode='translate_zh', switch_prompt=switch_prompt)


    # <-------------- compile PDF ------------->
    success = yield from 编译Latex差别(chatbot, history, main_file_original='merge', main_file_modified='merge_translate_zh', 
                             work_folder_original=project_folder, work_folder_modified=project_folder, work_folder=project_folder)

    # <-------------- zip PDF ------------->
    zip_result(project_folder)
    if success:
        chatbot.append((f"成功啦", '請查收結果（壓縮包）...'))
        yield from update_ui(chatbot=chatbot, history=history); time.sleep(1) # 刷新界面
    else:
        chatbot.append((f"失敗了", '雖然PDF生成失敗了, 但請查收結果（壓縮包）, 內含已經翻譯的Tex文檔, 也是可讀的, 您可以到Github Issue區, 用該壓縮包+對話歷史存檔進行反饋 ...'))
        yield from update_ui(chatbot=chatbot, history=history); time.sleep(1) # 刷新界面

    # <-------------- we are done ------------->
    return success
