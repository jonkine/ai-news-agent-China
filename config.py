import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# API密钥配置（二选一）
# ============================================

# 方案1：国内方案 - 智谱AI（推荐，国内快）
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

# 方案2：国外方案 - OpenAI（需要VPN）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 搜索API（二选一）
# 方案A：Serper（国外，稳定，需要VPN但比OpenAI快）
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# 方案B：国内搜索（无需VPN，但可能不稳定）
# 暂时不用配置，代码里直接用必应

# ============================================
# 搜索配置
# ============================================

# 搜索关键词（中文）
SEARCH_QUERIES = [
    "人工智能最新资讯",
    "AI技术突破", 
    "大模型发布",
    "AI应用落地",
    "OpenAI动态"
]

# 或者英文关键词（如果用Serper）
# SEARCH_QUERIES = [
#     "artificial intelligence latest news",
#     "AI breakthrough 2024",
#     "OpenAI news",
#     "machine learning research"
# ]

# ============================================
# 输出配置
# ============================================

SUMMARY_LANGUAGE = "zh"  # zh=中文, en=英文
MAX_ARTICLES = 5         # 每次收集几条新闻

# ============================================
# 定时配置
# ============================================

SCHEDULE_TIME = "09:00"  # 每天早上9点运行
