import requests
from typing import List, Dict
import config

class NewsSearcher:
    def __init__(self):
        # 用回 Serper，但只搜索中文
        self.api_key = config.SERPER_API_KEY  # 需要在config.py加回来
        self.url = "https://google.serper.dev/search"
    
    def search(self, query: str) -> List[Dict]:
        """Serper搜索"""
        if not self.api_key:
            print("  ⚠️  缺少 SERPER_API_KEY")
            return []
        
        print(f"  搜索: {query}")
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        data = {
            "q": query,
            "num": 3,
            "tbs": "qdr:d",  # 最近24小时
            "hl": "zh-CN"    # 中文结果
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=data, timeout=10)
            results = response.json()
            
            news_list = []
            for item in results.get('organic', []):
                news_list.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '无摘要'),
                    'date': item.get('date', '近期')
                })
            
            print(f"  ✅ 找到 {len(news_list)} 条")
            return news_list
            
        except Exception as e:
            print(f"  ⚠️  搜索失败: {str(e)[:50]}")
            return []
    
    def search_all(self) -> List[Dict]:
        """搜索所有"""
        all_news = []
        print("🔍 开始搜索AI资讯...\n")
        
        for query in config.SEARCH_QUERIES:
            results = self.search(query)
            all_news.extend(results)
        
        # 去重
        seen = set()
        unique_news = []
        for item in all_news:
            if item['title'] not in seen and len(unique_news) < config.MAX_ARTICLES:
                seen.add(item['title'])
                unique_news.append(item)
        
        print(f"\n📊 总计: {len(unique_news)} 条")
        return unique_news
