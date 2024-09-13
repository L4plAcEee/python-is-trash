import openai
import requests
import datetime

# 设置全局变量
api_key = ""  # 替换为你的 API Key
user_id = "L4place"  # 替换为你的UserID
proxies = None  # 设置 proxies 为 None，表示不使用任何代理

# 设置提示词
prompt = "你是人工智能助手，你更擅长中文和英文的对话，你是计算机领域的专家，你更喜欢用简洁精炼的风格回答问题"

# 测试网络请求
try:
    requests.get('https://api.moonshot.cn/v1', proxies=proxies)
    print("网络请求成功")
except requests.RequestException as e:
    print("网络请求失败:", e)

# 初始化 OpenAI 客户端
client = openai.OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")

# 初始对话内容
conversation = [{"role": "system", "content": prompt}]

print("开始对话，输入 'exit' 退出。")

while True:
    user_input = input(f"{user_id}: ")
    if user_input.lower() == "exit":
        print("对话结束。")
        break

    conversation.append({"role": "user", "content": user_input})

    # 调用 OpenAI API 获取流式回复
    try:
        stream = client.chat.completions.create(
            model="moonshot-v1-auto",
            messages=conversation,
            temperature=0.3,
            stream=True
        )

        print("reply：", end="")
        assistant_reply = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                print(delta.content, end="")
                assistant_reply += delta.content

        print()
        conversation.append({"role": "assistant", "content": assistant_reply})

    except openai.error.OpenAIError as e:
        print(f"请求失败: {e}")
    print(f"----- {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -----")

