# 此Dockerfile适用于“无本地模型”的环境构建，如果需要使用chatglm等本地模型或者latex运行依赖，请参考 docker-compose.yml
# 如何构建: 先修改 `config.py`， 然后 `docker build -t gpt-academic . `
# 如何运行(Linux下): `docker run --rm -it --net=host gpt-academic `
# 如何运行(其他操作系统，选择任意一个固定端口50923): `docker run --rm -it -e WEB_PORT=50923 -p 50923:50923 gpt-academic `
FROM python:3.11

RUN echo '[global]' > /etc/pip.conf && \
    echo 'index-url = https://mirrors.aliyun.com/pypi/simple/' >> /etc/pip.conf && \
    echo 'trusted-host = mirrors.aliyun.com' >> /etc/pip.conf


WORKDIR /gpt




# 安装依赖
COPY requirements.txt ./
COPY ./docs/gradio-3.32.2-py3-none-any.whl ./docs/gradio-3.32.2-py3-none-any.whl
RUN pip3 install -r requirements.txt
# 装载项目文件
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install -r request_llm/requirements_slackclaude.txt
RUN pip3 install --upgrade moviepy

# 可选步骤，用于预热模块
RUN python3  -c 'from check_proxy import warm_up_modules; warm_up_modules()'

# 启动
CMD ["python3", "-u", "main.py"]
