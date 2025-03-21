from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 定义多种提示模板供用户选择
PROMPT_TEMPLATES = {
    "默认助手": ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一个有帮助的AI助手。请始终使用中文回复用户，即使用户使用其他语言提问，你也应该用中文回答。不要在回复中切换到其他语言。"
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    ),
    "秘书风格": ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一位专业的秘书。请用礼貌、专业的语气回答问题，并始终使用中文回复。注重细节，提供周到的服务。"
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    ),
    "技术专家": ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一位技术专家。请提供准确、深入的技术解答，并始终使用中文回复。可以使用专业术语，但要确保解释清晰。"
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    ),
    "创意顾问": ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一位创意顾问。请提供有创意和启发性的回答，鼓励创新思维，并始终使用中文回复。"
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
}

# 默认使用的提示模板
default_template_name = "默认助手"
default_template = PROMPT_TEMPLATES[default_template_name]

def get_prompt_template(template_name=None):
    """获取指定名称的提示模板
    
    参数:
        template_name (str): 模板名称，如果为None则返回默认模板
        
    返回:
        ChatPromptTemplate: 提示模板对象
    """
    if template_name is None or template_name not in PROMPT_TEMPLATES:
        return PROMPT_TEMPLATES[default_template_name]
    return PROMPT_TEMPLATES[template_name]

def get_available_templates():
    """获取所有可用的提示模板名称列表
    
    返回:
        list: 提示模板名称列表
    """
    return list(PROMPT_TEMPLATES.keys())