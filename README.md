# MinStock-Analyzer

这是一个基于大语言模型（LLM）的股市分析微应用。主要作为寒假“AI+微应用”的实践项目开发。

通过抓取真实的A股历史交易数据，并结合预设的分析提示词，调用大模型输出包含趋势概述、关键点位、风险提示和操作建议的结构化报告。

## 主要功能

* 行情获取：自动抓取指定A股代码的近期历史日线数据。
* 智能分析：大模型结合真实行情数据生成技术面解读。
* 极简交互：基于 Streamlit 构建的 Web 界面，输入代码即可生成报告。

## 核心技术栈

* Python
* Streamlit (前端渲染)
* akshare (数据源抓取)
* openai (大模型 API 调用协议)

## 运行说明

1. 克隆代码库：
   git clone https://github.com/zhouhuimin0111-hash/MinStock-Analyzer.git
   cd MinStock-Analyzer

2. 配置虚拟环境并安装依赖：
   pip install -r requirements.txt

3. 环境变量配置：
   在项目根目录创建 .env 文件，写入大模型 API 密钥：
   ZHIPU_API_KEY=your_api_key_here

4. 启动应用：
   streamlit run app.py

## 免责声明

本项目及 AI 生成的股市分析报告仅供代码开发测试与学术交流使用，绝对不构成任何投资理财建议。开发者不对使用本项目信息造成的任何直接或间接损失负责。

## 开发者

周慧敏 - 杭州师范大学