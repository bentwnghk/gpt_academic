
def check_proxy(proxies):
    import requests
    proxies_https = proxies['https'] if proxies is not None else '無'
    try:
        response = requests.get("https://ipapi.co/json/",
                                proxies=proxies, timeout=4)
        data = response.json()
        print(f'查詢代理的地理位置，返回的結果是{data}')
        if 'country_name' in data:
            country = data['country_name']
            result = f"代理配置 {proxies_https}, 代理所在地：{country}"
        elif 'error' in data:
            result = f"代理配置 {proxies_https}, 代理所在地：未知，IP查詢頻率受限"
        else:
            result = f"代理配置 {proxies_https}, 代理數據解析失敗：{data}"
        print(result)
        return result
    except:
        result = f"代理配置 {proxies_https}, 代理所在地查詢超時，代理可能無效"
        print(result)
        return result


def backup_and_download(current_version, remote_version):
    """
    一键更新协议：备份和下载
    """
    from toolbox import get_conf
    import shutil
    import os
    import requests
    import zipfile
    os.makedirs(f'./history', exist_ok=True)
    backup_dir = f'./history/backup-{current_version}/'
    new_version_dir = f'./history/new-version-{remote_version}/'
    if os.path.exists(new_version_dir):
        return new_version_dir
    os.makedirs(new_version_dir)
    shutil.copytree('./', backup_dir, ignore=lambda x, y: ['history'])
    proxies, = get_conf('proxies')
    r = requests.get(
        'https://github.com/binary-husky/chatgpt_academic/archive/refs/heads/master.zip', proxies=proxies, stream=True)
    zip_file_path = backup_dir+'/master.zip'
    with open(zip_file_path, 'wb+') as f:
        f.write(r.content)
    dst_path = new_version_dir
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        for zip_info in zip_ref.infolist():
            dst_file_path = os.path.join(dst_path, zip_info.filename)
            if os.path.exists(dst_file_path):
                os.remove(dst_file_path)
            zip_ref.extract(zip_info, dst_path)
    return new_version_dir


def patch_and_restart(path):
    """
    一键更新协议：覆盖和重启
    """
    from distutils import dir_util
    import shutil
    import os
    import sys
    import time
    import glob
    from colorful import print亮黄, print亮绿, print亮红
    # if not using config_private, move origin config.py as config_private.py
    if not os.path.exists('config_private.py'):
        print亮黄('由於您沒有設置config_private.py私密配置，現將您的現有配置移動至config_private.py以防止配置丟失，',
              '另外您可以隨時在history子文件夾下找回舊版的程序。')
        shutil.copyfile('config.py', 'config_private.py')
    path_new_version = glob.glob(path + '/*-master')[0]
    dir_util.copy_tree(path_new_version, './')
    print亮绿('代碼已經更新，即將更新pip包依賴……')
    for i in reversed(range(5)): time.sleep(1); print(i)
    try: 
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except:
        print亮红('pip包依賴安裝出現問題，需要手動安裝新增的依賴庫 `python -m pip install -r requirements.txt`，然後在用常規的`python main.py`的方式啟動。')
    print亮绿('更新完成，您可以隨時在history子文件夾下找回舊版的程序，5s之後重啟。')
    print亮红('假如重啟失敗，您可能需要手動安裝新增的依賴庫 `python -m pip install -r requirements.txt`，然後在用常規的`python main.py`的方式啟動。')
    print(' ------------------------------ -----------------------------------')
    for i in reversed(range(8)): time.sleep(1); print(i)
    os.execl(sys.executable, sys.executable, *sys.argv)


def get_current_version():
    import json
    try:
        with open('./version', 'r', encoding='utf8') as f:
            current_version = json.loads(f.read())['version']
    except:
        current_version = ""
    return current_version


def auto_update(raise_error=False):
    """
    一键更新协议：查询版本和用户意见
    """
    try:
        from toolbox import get_conf
        import requests
        import time
        import json
        proxies, = get_conf('proxies')
        response = requests.get(
            "https://raw.githubusercontent.com/binary-husky/chatgpt_academic/master/version", proxies=proxies, timeout=5)
        remote_json_data = json.loads(response.text)
        remote_version = remote_json_data['version']
        if remote_json_data["show_feature"]:
            new_feature = "新功能：" + remote_json_data["new_feature"]
        else:
            new_feature = ""
        with open('./version', 'r', encoding='utf8') as f:
            current_version = f.read()
            current_version = json.loads(current_version)['version']
        if (remote_version - current_version) >= 0.01-1e-5:
            from colorful import print亮黄
            print亮黄(
                f'\n新版本可用。新版本:{remote_version}，當前版本:{current_version}。{new_feature}')
            print('（1）Github更新地址:\nhttps://github.com/binary-husky/chatgpt_academic\n')
            user_instruction = input('（2）是否一鍵更新代碼（Y+回車=確認，輸入其他/無輸入+回車=不更新）？')
            if user_instruction in ['Y', 'y']:
                path = backup_and_download(current_version, remote_version)
                try:
                    patch_and_restart(path)
                except:
                    msg = '更新失敗'
                    if raise_error:
                        from toolbox import trimmed_format_exc
                        msg += trimmed_format_exc()
                    print(msg)
            else:
                print('自動更新程序：已禁用')
                return
        else:
            return
    except:
        msg = '自動更新程序：已禁用。建議排查：代理網絡配置。'
        if raise_error:
            from toolbox import trimmed_format_exc
            msg += trimmed_format_exc()
        print(msg)

def warm_up_modules():
    print('正在執行一些模塊的預熱...')
    from request_llm.bridge_all import model_info
    enc = model_info["gpt-3.5-turbo"]['tokenizer']
    enc.encode("模塊預熱", disallowed_special=())
    enc = model_info["gpt-4"]['tokenizer']
    enc.encode("模塊預熱", disallowed_special=())

if __name__ == '__main__':
    import os
    os.environ['no_proxy'] = '*'  # 避免代理网络产生意外污染
    from toolbox import get_conf
    proxies, = get_conf('proxies')
    check_proxy(proxies)
