import streamlit as st
import analyzer  # 导入我们刚刚写好的后端逻辑

# 设置网页的基本属性
st.set_page_config(page_title="MinStock-Analyzer", layout="centered")

# 页面标题和说明
st.title("MinStock-Analyzer 股市分析微应用")
st.write("这是一个基于大语言模型构建的轻量级股市分析工具。请输入 A股 代码获取极简的技术面分析。")
st.markdown("---")

# 用户输入区域
symbol = st.text_input("请输入6位股票代码 (例如: 600519 代表贵州茅台)", value="600519", max_chars=6)

# 当用户点击按钮时触发运行
if st.button("生成 AI 分析报告"):
    if len(symbol) != 6 or not symbol.isdigit():
        st.warning("请输入格式正确的 6 位纯数字股票代码。")
    else:
        # 使用 spinner 显示加载动画，优化用户体验
        with st.spinner(f"正在抓取 {symbol} 的最新行情并呼叫 AI，请稍候..."):

            # 1. 调用 analyzer.py 中的函数获取数据
            df = analyzer.fetch_stock_data(symbol)

            if df is None or df.empty:
                st.error("行情数据获取失败，请检查网络或股票代码是否有效。")
            else:
                # 2. 在网页上展示获取到的最近几天的数据表
                st.subheader("近期行情数据 (展示前5天)")
                st.dataframe(df.tail(5), use_container_width=True)

                # 3. 调用大模型生成报告并在网页上渲染
                st.subheader("AI 综合分析报告")
                report = analyzer.generate_analysis(symbol, df)
                st.markdown(report)

st.markdown("---")
st.caption("免责声明：本应用由 AI 生成内容，仅作为大作业代码测试与学习参考，绝不构成任何真实的投资理财建议。")