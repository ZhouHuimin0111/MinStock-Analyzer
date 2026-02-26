#验证网络环境和 akshare 库能不能正常拉取到行情数据。

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


def fetch_stock_data(symbol, days=30):
    print(f"正在尝试获取 A股 {symbol} 的历史数据...")

    # 计算时间范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    try:
        # 抓取A股日线数据（qfq代表前复权，这是金融分析的规范）
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_str, end_date=end_str, adjust="qfq")

        if df.empty:
            print("错误：未获取到数据，请检查股票代码是否正确。")
            return None

        return df

    except Exception as e:
        print(f"获取数据时发生异常: {e}")
        return None


if __name__ == "__main__":
    # 测试代码：贵州茅台 (600519)
    test_ticker = "600519"

    data = fetch_stock_data(test_ticker)

    if data is not None:
        print("\n数据获取成功。最近5个交易日的数据如下：")
        # 注意：akshare 返回的 DataFrame 列名默认是中文的
        print(data[['日期', '开盘', '最高', '最低', '收盘', '成交量']].tail())