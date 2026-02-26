import requests
import config
import concurrent.futures
import time

class NewsSummarizer:
    def __init__(self):
        self.api_key = config.ZHIPU_API_KEY
        self.url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    def summarize_one(self, article: dict, index: int) -> tuple:
        """单篇总结（带超时）"""
        title = article['title']
        content = article['snippet'][:400]  # 减少字数，更快
        
        print(f"  📝 [{index+1}/5] {title[:20]}...")
        
        if not self.api_key:
            return (index, "⚠️ 缺少API Key")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 用最快的模型 glm-4-flash，简化prompt
        data = {
            "model": "glm-4-flash",
            "messages": [{
                "role": "user",
                "content": f"总结这条AI新闻，30字以内：{title}。内容：{content}"
            }],
            "max_tokens": 50,  # 减少token，更快返回
            "temperature": 0.1  # 几乎确定性的输出，最快
        }
        
        try:
            start = time.time()
            # 严格5秒超时
            response = requests.post(self.url, headers=headers, json=data, timeout=5)
            result = response.json()['choices'][0]['message']['content']
            elapsed = time.time() - start
            print(f"  ✅ [{index+1}] 完成 ({elapsed:.1f}s)")
            return (index, result)
            
        except Exception as e:
            # 超时或失败，用原文前80字
            print(f"  ⚡ [{index+1}] 超时/失败，用原文")
            return (index, f"【速览】{content[:80]}...")
    
    def create_report(self, articles: list) -> str:
        """并行总结所有文章"""
        print(f"\n🚀 智谱AI并行总结 {len(articles)} 篇（每篇最多5秒）...")
        start_total = time.time()
        
        # 同时处理5篇，不用等
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.summarize_one, a, i) 
                      for i, a in enumerate(articles)]
            results = [f.result() for f in futures]
        
        # 按顺序排列
        results.sort(key=lambda x: x[0])
        summaries = [r[1] for r in results]
        
        total_time = time.time() - start_total
        print(f"\n⏱️  总结总耗时: {total_time:.1f}秒")
        
        # 生成报告
        lines = [
            "=" * 60,
            "🤖 AI每日资讯简报",
            "=" * 60,
            f"更新时间: {time.strftime('%Y-%m-%d %H:%M')}",
            f"来源: 实时搜索 | 共{len(articles)}条 | 耗时{total_time:.0f}秒",
            "=" * 60,
            ""
        ]
        
        for i, (article, summary) in enumerate(zip(articles, summaries), 1):
            lines.extend([
                f"【{i}】{article['title']}",
                "-" * 60,
                f"🔗 {article['link']}",
                f"📅 {article['date']}",
                "",
                f"💡 {summary}",
                "",
                "=" * 60,
                ""
            ])
        
        return "\n".join(lines)
