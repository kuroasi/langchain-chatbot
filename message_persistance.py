# langgraph_app.py - LangGraph应用模块
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, END, MessagesState, StateGraph
from langchain_core.messages import HumanMessage
from message_trimmer import trim_messages

def create_langgraph_app(model, memory=None):
    """创建LangGraph应用（仅异步版本）
    
    Args:
        model: 语言模型实例
        memory: 可选的内存存储器
    
    Returns:
        编译后的LangGraph应用
    """
    if memory is None:
        memory = MemorySaver()
    
    # 异步版本的模型调用函数
    async def call_model_async(state: MessagesState):
        try:
            # 在调用模型前修剪消息，防止上下文窗口溢出
            trimmed_messages = trim_messages(
                messages=state["messages"],
                max_messages=20,  # 保留最多20条消息
                keep_system_message=True,  # 始终保留系统消息
                strategy="last"  # 保留最近的消息
            )
            response = await model.ainvoke(trimmed_messages)
            return {"messages": response}
        except Exception as e:
            print(f"异步调用模型时出错: {e}")
            raise
    
    # 定义工作流
    workflow = StateGraph(state_schema=MessagesState)
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model_async)  # 只使用异步函数
    workflow.add_edge("model", END)
    
    # 编译应用
    app = workflow.compile(checkpointer=memory)
    return app