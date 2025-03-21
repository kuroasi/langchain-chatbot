# groq_memory_example.py - 展示如何使用带有对话记忆功能的Groq聊天模块

from groq_chat import chat_with_groq
from langchain_core.messages import HumanMessage, AIMessage

def demo_with_memory():
    """
    演示如何使用带有记忆功能的Groq聊天
    """
    # 生成一个会话ID
    import uuid
    thread_id = str(uuid.uuid4())
    print(f"会话ID: {thread_id}")
    
    # 初始化历史记录
    history = []
    
    # 第一轮对话
    query1 = "你好，我是小明"
    print(f"\n用户: {query1}")
    response1 = chat_with_groq(query1, thread_id=thread_id, history=history)
    print(f"Groq: {response1}")
    
    # 更新历史记录
    history.append(HumanMessage(content=query1))
    history.append(AIMessage(content=response1))
    
    # 第二轮对话，模型应该记得用户是小明
    query2 = "你还记得我是谁吗？"
    print(f"\n用户: {query2}")
    response2 = chat_with_groq(query2, thread_id=thread_id, history=history)
    print(f"Groq: {response2}")
    
    # 更新历史记录
    history.append(HumanMessage(content=query2))
    history.append(AIMessage(content=response2))
    
    # 第三轮对话
    query3 = "请给我讲一个关于人工智能的小故事"
    print(f"\n用户: {query3}")
    response3 = chat_with_groq(query3, thread_id=thread_id, history=history)
    print(f"Groq: {response3}")

def demo_without_memory():
    """
    演示不使用记忆功能的Groq聊天
    """
    print("\n不使用记忆功能的对话示例:")
    
    # 第一轮对话
    query1 = "你好，我是小明"
    print(f"\n用户: {query1}")
    response1 = chat_with_groq(query1)
    print(f"Groq: {response1}")
    
    # 第二轮对话，模型不应该记得用户是小明
    query2 = "你还记得我是谁吗？"
    print(f"\n用户: {query2}")
    response2 = chat_with_groq(query2)
    print(f"Groq: {response2}")

if __name__ == "__main__":
    print("使用记忆功能的对话示例:")
    demo_with_memory()
    
    print("\n" + "-"*50)
    
    demo_without_memory()