#负责把前面跑通的数据抓取和大模型调用这两个模块拼装在一起

#大模型看不懂复杂的 Python 数据对象（比如 DataFrame），它只懂文本。所以我们需要在代码里，把抓到的历史行情转换成结构化的字符串，然后嵌入到预设的 Prompt（提示词）中，最后发给大模型。
import os
from dotenv import load_dotenv

# 加载 .env 文件里的隐藏变量
load_dotenv()

# 用这种方式安全获取 API Key
API_KEY = os.getenv("ZHIPU_API_KEY")
#让程序去 .env 文件里“偷偷”拿钥匙，而不是直接暴露在代码里

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI

BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
MODEL_NAME = "glm-4-flash"


def fetch_stock_data(symbol, days=30):
    """从 akshare 获取 A股 日线数据 (使用新浪数据源作为备用方案)"""
    print(f"1/3 正在通过新浪接口抓取代码 {symbol} 的历史数据...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    try:
        # 新浪接口的特点：股票代码前必须加上 sh(上交所) 或 sz(深交所) 前缀
        # 6开头的股票是上交所，0或3开头是深交所
        prefix = "sh" if symbol.startswith("6") else "sz"
        full_symbol = prefix + symbol

        # 调用新浪的数据接口 stock_zh_a_daily
        df = ak.stock_zh_a_daily(symbol=full_symbol, start_date=start_str, end_date=end_str, adjust="qfq")

        if df.empty:
            print("获取数据失败：返回为空。")
            return None

        # 新浪接口默认返回英文列名，为了兼容我们大模型的 Prompt，这里手动把列名转成中文
        df.rename(columns={
            'date': '日期', 'open': '开盘', 'high': '最高',
            'low': '最低', 'close': '收盘', 'volume': '成交量'
        }, inplace=True)

        return df
    except Exception as e:
        print(f"数据抓取异常: {e}")
        return None

def generate_analysis(symbol, df):
    """将数据转换为文本，并调用大模型生成分析"""
    print("2/3 数据抓取完毕，正在拼接 Prompt...")

    # 取最近10个交易日的数据。给大模型的数据不宜过多，容易超出上下文限制且稀释注意力
    recent_data = df[['日期', '开盘', '最高', '最低', '收盘', '成交量']].tail(10)

    # 核心步骤：把 DataFrame 转换成纯文本的表格字符串
    data_str = recent_data.to_string(index=False)

    # 设计系统提示词
    prompt = f"""
    你是一个资深的 A股 量化分析师。请根据以下股票（代码：{symbol}）最近10个交易日的日线数据，给出一份简明的技术面分析报告。

    近期交易数据如下：
    {data_str}

    请按以下结构输出报告：
    1. 趋势概述：总结近期的价格走势和成交量变化。
    2. 关键点位：估算当前的大致支撑位和阻力位。
    3. 风险提示：指出当前盘面的潜在技术面风险。
    4. 操作建议：给出客观的参考建议。

    要求：语言专业、客观、精炼。必须在末尾注明“本分析由 AI 生成，仅供代码测试与学习参考，绝不构成任何投资建议”。
    """

    print("3/3 正在请求大模型生成报告，请稍候...")
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个严谨的金融数据分析师。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # 温度设低，保证输出的逻辑性和稳定性
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"大模型调用失败: {e}"


if __name__ == "__main__":
    # 测试主逻辑
    test_symbol = "600519"  # 贵州茅台

    stock_df = fetch_stock_data(test_symbol)

    if stock_df is not None:
        report = generate_analysis(test_symbol, stock_df)
        print("\n" + "=" * 20 + " AI 股市分析报告 " + "=" * 20)
        print(report)
        print("=" * 56)
    else:
        print("流程终止：缺少前置数据。")
