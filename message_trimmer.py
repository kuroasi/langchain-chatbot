# message_trimmer.py - 消息修剪模块
from typing import List, Optional, Callable, Union, Dict, Any
from langchain_core.messages import BaseMessage, SystemMessage

def trim_messages(
    messages: List[BaseMessage],
    max_messages: int = 10,
    keep_system_message: bool = True,
    strategy: str = "last"
) -> List[BaseMessage]:
    """
    修剪消息列表以控制上下文窗口大小
    
    参数:
        messages (List[BaseMessage]): 要修剪的消息列表
        max_messages (int): 保留的最大消息数量，默认为10
        keep_system_message (bool): 是否始终保留系统消息，默认为True
        strategy (str): 修剪策略，可选值为"last"(保留最后的消息)或"first"(保留最早的消息)，默认为"last"
        
    返回:
        List[BaseMessage]: 修剪后的消息列表
    """
    # 如果消息数量未超过限制，直接返回
    if len(messages) <= max_messages:
        return messages
    
    # 分离系统消息和其他消息
    system_messages = []
    other_messages = []
    
    for message in messages:
        if isinstance(message, SystemMessage) and keep_system_message:
            system_messages.append(message)
        else:
            other_messages.append(message)
    
    # 根据策略选择要保留的消息
    if strategy == "last":
        # 计算需要保留的非系统消息数量
        remaining_slots = max_messages - len(system_messages)
        # 保留最后的消息
        trimmed_other_messages = other_messages[-remaining_slots:] if remaining_slots > 0 else []
    elif strategy == "first":
        # 计算需要保留的非系统消息数量
        remaining_slots = max_messages - len(system_messages)
        # 保留最早的消息
        trimmed_other_messages = other_messages[:remaining_slots] if remaining_slots > 0 else []
    else:
        raise ValueError(f"不支持的修剪策略: {strategy}，可选值为'last'或'first'")
    
    # 合并系统消息和修剪后的其他消息
    return system_messages + trimmed_other_messages