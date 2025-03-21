from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.messages import HumanMessage
import os

llm = QianfanChatEndpoint(
    qianfan_ak=os.getenv('ERNIE_CLIENT_ID'),
    qianfan_sk=os.getenv('ERNIE_CLIENT_SECRET')
)

messages = [
    HumanMessage(content="介绍一下你自己")
]