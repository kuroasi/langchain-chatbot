# LangChain 智能聊天机器人 - Hugging Face Spaces 部署指南

## 部署步骤

1. 在 Hugging Face 上创建一个新的 Space
   - 访问 [Hugging Face Spaces](https://huggingface.co/spaces)
   - 点击 "New Space" 按钮
   - 选择 "Gradio" 作为 SDK
   - 填写 Space 名称和描述

2. 设置环境变量
   - 在 Space 设置中，添加以下环境变量：
     - `GROQ_API_KEY`: 您的 Groq API 密钥

3. 上传代码
   - 使用 Git 将代码推送到 Hugging Face Space 仓库
   - 或者使用 Hugging Face 网页界面上传文件

## 注意事项

- 确保 `requirements.txt` 包含所有必要的依赖
- 应用已配置为使用环境变量中的 `PORT`，这是 Hugging Face Spaces 所需的
- `Procfile` 已正确配置为使用 `python app.py` 启动应用

## 故障排除

如果应用无法启动，请检查：

1. 环境变量是否正确设置
2. 依赖项是否正确安装
3. 查看 Space 日志以获取详细错误信息