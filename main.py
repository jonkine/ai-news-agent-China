from search_engine import NewsSearcher
from summarizer import NewsSummarizer
from datetime import datetime
import time
import config

def run_agent():
    """执行AI新闻助手"""
    print(f"\n{'='*60}")
    print(f"🚀 国内AI新闻助手启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # 检查配置（改用智谱API）
    if not config.ZHIPU_API_KEY:
        print("\n❌ 错误：缺少 智谱AI API Key")
        print("请在.env文件中添加 ZHIPU_API_KEY=你的密钥")
        print("申请地址: https://open.bigmodel.cn")
        return False
    
    # 搜索新闻
    searcher = NewsSearcher()
    news = searcher.search_all()
    
    if not news:
        print("\n⚠️ 未找到新闻，1小时后重试...")
        return False
    
    # 生成报告
    print(f"\n✍️ 正在生成报告...")
    summarizer = NewsSummarizer()
    report = summarizer.create_report(news)
    
    # 保存为文本格式
    filename = "daily_ai_news.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 同时保存Markdown格式
    md_filename = "daily_ai_news.md"
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 完成！")
    print(f"📄 文本报告: {filename}")
    print(f"📄 Markdown报告: {md_filename}")
    print(f"📊 共处理 {len(news)} 条新闻")
    print(f"⏰ 下次更新: 明天 {config.SCHEDULE_TIME}")
    
    # 显示报告预览
    print(f"\n{'='*60}")
    print("📋 报告预览:")
    print(f"{'='*60}")
    print(report[:600] + "...")
    
    return True

def schedule_daily():
    """设置每日定时运行"""
    import schedule
    
    print(f"⏰ 已设置定时任务，每天 {config.SCHEDULE_TIME} 自动运行...")
    print("💡 按 Ctrl+C 停止程序\n")
    
    schedule.every().day.at(config.SCHEDULE_TIME).do(run_agent)
    
    # 立即运行一次测试
    print("🧪 立即运行一次测试...")
    run_agent()
    
    # 保持运行
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # 单次运行模式
        run_agent()
    else:
        # 定时运行模式（默认）
        schedule_daily()
