# app.py - Web应用程序入口点
import os
import gradio as gr
from dotenv import load_dotenv, find_dotenv
from gradio_app import app as gradio_app

# 加载环境变量
load_dotenv(find_dotenv(), override=True)

# 设置端口
port = int(os.environ.get("PORT", 7860))

# 启动应用
if __name__ == "__main__":
    gradio_app.launch(server_name="0.0.0.0", server_port=port, share=False)