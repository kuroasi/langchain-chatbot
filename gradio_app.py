# gradio_app.py - Gradio Web界面应用
import os
import uuid
import re
import gradio as gr
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from groq_chat import chat_with_groq

# 加载环境变量
load_dotenv(find_dotenv(), override=True)

# 可用的模型列表
AVAILABLE_MODELS = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it"
]

# 导入可用的提示模板
from prompt_templates import get_available_templates

# 保存会话状态
class ChatState:
    def __init__(self):
        self.thread_id = str(uuid.uuid4())
        self.history = []
        self.messages = []

# 初始化会话状态
chat_state = ChatState()

def user_input_callback(message, history, model_name, template_name):
    """
    处理用户输入并返回模型响应
    """
    # 确保API密钥已设置
    if not os.environ.get("GROQ_API_KEY"):
        return "", history + [[message, "请先在环境变量中设置GROQ_API_KEY"]]
    
    # 创建一个包含用户消息但AI回复为空的历史记录
    history_with_user_message = history + [[message, None]]
    
    # 立即返回更新后的历史记录，显示用户消息
    yield "", history_with_user_message
    
    try:
        # 调用Groq模型进行对话
        response = chat_with_groq(
            user_input=message,
            model_name=model_name,
            thread_id=chat_state.thread_id,
            history=chat_state.history,
            template_name=template_name
        )
        
        # 更新历史记录
        chat_state.history.append(HumanMessage(content=message))
        chat_state.history.append(AIMessage(content=response))
        
        # 返回空字符串给输入框，更新后的历史给聊天界面
        yield "", history + [[message, response]]
    except Exception as e:
        error_message = f"处理请求时发生错误: {str(e)}"
        print(error_message)
        return "", history + [[message, "⚠️ " + error_message]]

def clear_conversation():
    """
    清除对话历史并创建新的会话ID
    """
    chat_state.thread_id = str(uuid.uuid4())
    chat_state.history = []
    chat_state.messages = []
    # 返回空输入和包含系统消息的历史记录
    return None, [[None, f"✅ 对话已清除，新会话ID: {chat_state.thread_id}"]]

# 创建Gradio界面
with gr.Blocks(title="LangChain 智能聊天机器人", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🤖 LangChain 智能聊天机器人")
    gr.Markdown("基于Groq API的聊天机器人，支持对话历史记忆功能")
    
    with gr.Row():
        with gr.Column(scale=4):
            # 聊天界面
            chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                height=500,
                avatar_images=(None, "🤖"),
            )
            
            # 用户输入
            with gr.Row():
                user_input = gr.Textbox(
                    show_label=False,
                    placeholder="请输入您的问题...",
                    container=False,
                    scale=9
                )
                submit_btn = gr.Button("发送", scale=1)
            
            # 清除按钮
            clear_btn = gr.Button("清除对话")
        
        with gr.Column(scale=1):
            # 模型选择
            model_dropdown = gr.Dropdown(
                choices=AVAILABLE_MODELS,
                value=AVAILABLE_MODELS[0],
                label="选择模型"
            )
            
            # 提示模板选择
            template_dropdown = gr.Dropdown(
                choices=get_available_templates(),
                value=get_available_templates()[0],
                label="选择提示模板"
            )
            
            # 会话ID显示
            gr.Markdown(f"**当前会话ID**: {chat_state.thread_id}")
            
            # 使用说明
            with gr.Accordion("使用说明", open=False):
                gr.Markdown("""
                ### 使用方法
                1. 选择要使用的Groq模型
                2. 选择提示模板风格
                3. 在输入框中输入您的问题
                4. 点击发送按钮或按回车键提交
                5. 查看AI的回答
                
                ### 特性
                - 支持对话历史记忆功能
                - 可选择不同的Groq模型
                - 可选择不同的提示模板风格
                - 清除对话按钮可重置会话
                """)
    
    # 设置事件处理
    submit_btn.click(
        user_input_callback,
        inputs=[user_input, chatbot, model_dropdown, template_dropdown],
        outputs=[user_input, chatbot],
        queue=True  # 启用队列以支持生成器函数
    )
    
    user_input.submit(
        user_input_callback,
        inputs=[user_input, chatbot, model_dropdown, template_dropdown],
        outputs=[user_input, chatbot],
        queue=True  # 启用队列以支持生成器函数
    )
    
    clear_btn.click(
        clear_conversation,
        outputs=[user_input, chatbot]
    )

# 启动应用
if __name__ == "__main__":
    app.launch(share=False, inbrowser=True)