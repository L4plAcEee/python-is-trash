import openai
import requests

# 设置全局变量
api_key = ""  # 替换为你的 API Key
user_id = "L4place"  # 替换为你的UserID
proxies = {}  # 设置 proxies 为 None，表示不使用任何代理
# 设置提示词
prompt = "你是人工智能助手，你更擅长中文和英文的对话，你是计算机领域的专家，你更喜欢用简洁精炼的风格回答问题"
# 测试网络请求
try:
    response = requests.get('https://api.moonshot.cn/v1', proxies=proxies)
    print("网络请求成功")
except requests.RequestException as e:
    print("网络请求失败:", e)

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",  # 使用 Moonshot 的 API 地址
)
conversation = [
    {"role": "system",
     "content": f"{prompt}"},
]
user_input = ""
print("开始对话，输入 'exit' 退出。")
while True:
    user_input += input(f"{user_id}: ")  # 获取用户输入
    if user_input.lower() == "exit":
        print("对话结束。")
        break
    conversation.append({"role": "user", "content": user_input})
    stream = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=conversation,
        temperature=0.3,
        stream=True
    )
    print("reply：", end="")
    for chunk in stream:
        # 在这里，每个 chunk 的结构都与之前的 completion 相似，但 message 字段被替换成了 delta 字段
        delta = chunk.choices[0].delta  # <-- message 字段被替换成了 delta 字段
        if delta.content:
            # 我们在打印内容时，由于是流式输出，为了保证句子的连贯性，我们不人为地添加
            # 换行符，因此通过设置 end="" 来取消 print 自带的换行符。
            print(delta.content, end="")
            user_input += delta.content
    print()
    print("-----------------------------------------------------------------------------------------------------------")
