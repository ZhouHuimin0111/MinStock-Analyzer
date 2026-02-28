#测试大模型的 API 接口能否正常通信

from openai import OpenAI

# 1. 把这里替换成你刚刚复制的那一长串字符
API_KEY = "da951b276ff4dc4bdfa0f1933ab6ce.GMZXPR2ghPUnLACJ"

# 2. 智谱 AI 的官方接口地址和免费模型名称
BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
MODEL_NAME = "glm-4-flash"


def test_llm_connection():
    print("正在连接大模型，验证 API...")

    try:
        # 初始化客户端
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

        # 发起基础对话请求
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个资深的金融量化分析师。"},
                {"role": "user", "content": "请用一句话概括股市中'量价齐升'代表的市场信号。"}
            ],
            temperature=0.3  # 金融分析需要客观严谨，将温度调低，减少AI的幻觉发挥
        )

        print("\nAPI 调用成功！模型返回内容：")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"\nAPI 调用失败，错误信息: {e}")
        print("请检查你的网络连接、API Key 是否正确，以及 BASE_URL 是否填写规范。")


if __name__ == "__main__":
    test_llm_connection()
