# 导入依赖库
import os
import getpass
import asyncio
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from message_persistance import create_langgraph_app

def chat_with_groq(user_input, model_name="llama3-8b-8192", thread_id=None, history=None, template_name=None):
    """
    使用Groq模型进行对话，支持对话历史记忆和提示模板
    
    参数:
        user_input (str): 用户输入的文本
        model_name (str): 使用的模型名称，默认为"llama3-8b-8192"
        thread_id (str): 会话ID，用于保存对话历史，默认为None
        history (list): 历史消息列表，默认为None
        template_name (str): 提示模板名称，默认为None（使用默认模板）
        
    返回:
        str: 模型的响应文本
    """
    # 加载环境变量
    load_dotenv(find_dotenv(), override=True)
    
    # 检查GROQ_API_KEY是否存在，如果不存在则提示输入
    if not os.environ.get("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = getpass.getpass("请输入Groq API密钥: ")
    
    # 初始化模型
    model = init_chat_model(model_name, model_provider="groq")
    
    # 导入提示模板
    from prompt_templates import get_prompt_template
    
    # 获取指定的提示模板
    prompt_template = get_prompt_template(template_name)
    
    # 创建当前消息
    message = HumanMessage(content=user_input)
    
    # 如果没有提供历史记录，则创建一个新的消息列表
    if history is None:
        # 使用提示模板格式化消息
        messages = prompt_template.format_messages(messages=[message])
    else:
        # 使用提示模板格式化消息，包含历史记录
        messages = prompt_template.format_messages(messages=history + [message])
    
    # 如果提供了thread_id，使用LangGraph进行对话并保存历史
    if thread_id:
        # 创建LangGraph应用
        app = create_langgraph_app(model)
        
        # 使用异步调用
        async def run_with_memory():
            result = await app.ainvoke({"messages": messages}, {"configurable": {"thread_id": thread_id}})
            return result["messages"]
        
        # 运行异步函数
        response = asyncio.run(run_with_memory())
        # 检查response类型，如果是列表，则返回最后一个消息的内容
        if isinstance(response, list):
            if response and hasattr(response[-1], 'content'):
                return response[-1].content
            else:
                raise ValueError("无法从响应中获取内容")
        # 如果是单个消息对象，则直接返回其内容
        return response.content
    else:
        # 不使用记忆功能，直接调用模型
        response = model.invoke(messages)
        return response.content

def main():
    """
    主函数，提供交互式对话体验，支持对话历史记忆
    """
    print("欢迎使用Groq聊天机器人！输入'退出'结束对话。")
    
    # 生成一个会话ID
    import uuid
    thread_id = str(uuid.uuid4())
    print(f"会话ID: {thread_id}")
    
    # 保存对话历史
    history = []
    
    while True:
        user_input = input("\n请输入您的问题: ")
        
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("感谢使用，再见！")
            break
        
        # 使用thread_id和历史记录进行对话
        response = chat_with_groq(user_input, thread_id=thread_id, history=history)
        print(f"\nGroq回答: {response}")
        
        # 更新历史记录
        history.append(HumanMessage(content=user_input))
        history.append(AIMessage(content=response))

if __name__ == "__main__":
    main()

