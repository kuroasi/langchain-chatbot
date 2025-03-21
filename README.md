# LangChain 智能聊天机器人

这是一个基于LangChain框架的智能聊天机器人应用，集成了多种大语言模型，支持对话记忆功能和Web界面交互。本项目利用LangChain的强大功能，为用户提供流畅、智能的对话体验。

## 项目更新记录

### 2025-03-20 ver0.0.6 (commit id: 8d79536)
- 优化Gradio Web界面功能
- 更新应用程序文件
- 修复已知问题

### 2025-03-19 ver0.0.5
- 优化Gradio Web界面布局
- 添加会话ID显示功能
- 增强用户交互体验
- 添加使用说明文档

### 2025-03-19 ver0.0.4
- 添加Gradio Web界面应用
- 实现模型选择功能
- 优化对话记忆功能
- 更新依赖项列表，添加gradio>=4.0.0

### 2025-03-19 ver0.0.3
- 添加Groq和百度千帆聊天模型支持
- 实现对话记忆功能
- 添加message_persistance.py实现消息持久化
- 更新依赖项列表

### 2025-03-19 ver0.0.2
- 添加Groq模型集成支持
- 实现对话记忆功能
- 更新依赖项列表
- 创建models目录

### 2025-03-19 ver0.0.1
- 初始化项目
- 设置Python虚拟环境
- 初始化Git仓库
- 创建.gitignore文件
- 创建README.md文件

## 项目结构

```
├── venv/                    # Python虚拟环境
├── .gitignore               # Git忽略文件配置
├── README.md                # 项目说明文档
├── groq_chat.py             # Groq模型集成实现
├── groq_memory_example.py   # Groq对话记忆功能示例
├── message_persistance.py   # 消息持久化实现
├── qianfan_chat.py          # 百度千帆聊天模型实现
└── requirements.txt         # 项目依赖项列表
```

## 环境设置

1. 克隆仓库
```bash
git clone [仓库URL]
cd langchain_chatbot
```

2. 激活虚拟环境
```bash
# 在Windows上
venv\Scripts\activate

# 在macOS/Linux上
source venv/bin/activate
```

## 使用说明

### 安装依赖
```bash
pip install -r requirements.txt
```

### 使用Groq模型
```python
# 导入Groq聊天模块
from groq_chat import chat_with_groq

# 使用Groq模型进行对话
response = chat_with_groq("你好，请介绍一下自己")
print(response)
```

### 使用对话记忆功能
```python
# 导入必要的模块
from groq_chat import chat_with_groq
from langchain_core.messages import HumanMessage, AIMessage

# 创建会话ID
import uuid
thread_id = str(uuid.uuid4())

# 初始化历史记录
history = []

# 进行对话
query = "你好，我是小明"
response = chat_with_groq(query, thread_id=thread_id, history=history)
print(response)

# 更新历史记录
history.append(HumanMessage(content=query))
history.append(AIMessage(content=response))
```