import os
import requests
from typing import Dict, Any, List
from google.adk.agents import Agent

# --- 新聞查詢工具函數 ---

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_country_news(country_name: str) -> Dict[str, Any]:
    """查詢特定國家的最新新聞頭條。
    
    Args:
        country_name (str): 國家名稱，如 '台灣', '美國', '日本' 等
        
    Returns:
        Dict[str, Any]: 包含新聞資訊的字典，格式為：
            {
                "status": "success" | "error",
                "country": str,
                "articles": [{"title": str, "source": str, "url": str}, ...],
                "message": str (錯誤時使用)
            }
    """
    if not NEWS_API_KEY:
        return {
            "status": "error",
            "country": country_name,
            "message": "錯誤: News API 金鑰未設定。請設定 NEWS_API_KEY 環境變數。"
        }

    # 國家名稱映射
    country_code_map = {
        "台灣": "tw",
        "美國": "us", 
        "日本": "jp",
        "英國": "gb",
        "加拿大": "ca",
        "德國": "de",
        "法國": "fr",
        "義大利": "it",
        "韓國": "kr",
        "澳洲": "au"
    }
    
    country_code = country_code_map.get(country_name.lower(), None)
    
    if not country_code:
        supported_countries = ", ".join(country_code_map.keys())
        return {
            "status": "error",
            "country": country_name,
            "message": f"錯誤: 目前不支援 '{country_name}'。支援的國家: {supported_countries}"
        }
        
    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&pageSize=10&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('articles', [])
        
        if articles:
            news_list = []
            for article in articles:
                news_item = {
                    "title": article.get('title', '無標題'),
                    "source": article.get('source', {}).get('name', '未知來源'),
                    "url": article.get('url', '#'),
                    "description": article.get('description', ''),
                    "publishedAt": article.get('publishedAt', '')
                }
                news_list.append(news_item)
            
            return {
                "status": "success",
                "country": country_name,
                "count": len(news_list),
                "articles": news_list
            }
        else:
            return {
                "status": "error",
                "country": country_name,
                "message": f"未能獲取 {country_name} 的最新新聞。"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "country": country_name,
            "message": f"新聞查詢失敗: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "country": country_name,
            "message": f"發生未知錯誤: {str(e)}"
        }


def get_tech_news() -> Dict[str, Any]:
    """取得最新科技新聞。
    
    Returns:
        Dict[str, Any]: 包含科技新聞的字典，格式為：
            {
                "status": "success" | "error",
                "category": "technology",
                "articles": [{"title": str, "source": str, "url": str}, ...],
                "message": str (錯誤時使用)
            }
    """
    if not NEWS_API_KEY:
        return {
            "status": "error",
            "category": "technology",
            "message": "錯誤: News API 金鑰未設定。"
        }
    
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get('articles', [])
        
        if articles:
            news_list = []
            for article in articles:
                news_item = {
                    "title": article.get('title', '無標題'),
                    "source": article.get('source', {}).get('name', '未知來源'),
                    "url": article.get('url', '#'),
                    "description": article.get('description', ''),
                    "publishedAt": article.get('publishedAt', '')
                }
                news_list.append(news_item)
            
            return {
                "status": "success",
                "category": "technology",
                "count": len(news_list),
                "articles": news_list
            }
        else:
            return {
                "status": "error",
                "category": "technology",
                "message": "未能獲取科技新聞。"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "category": "technology",
            "message": f"科技新聞查詢失敗: {str(e)}"
        }

# --- Agent 定義 (使用最新 ADK 模式) ---

root_agent = Agent(
    name="news_assistant_agent2",
    model="gemini-2.5-flash",
    description=(
        "專業新聞助理代理，提供全球新聞查詢和科技新聞服務。"
        "支援查詢台灣、美國、日本等多個國家的最新新聞頭條，"
        "以及最新的科技新聞資訊。"
    ),
    instruction=(
        "你是一個專業的新聞助理代理。你可以："
        "1. 查詢特定國家的最新新聞 - 使用 get_country_news 函數"
        "2. 取得最新科技新聞 - 使用 get_tech_news 函數"
        "\n"
        "工具函數會返回結構化的字典數據，包含："
        "- status: 'success' 或 'error'"
        "- articles: 新聞文章列表 (包含 title, source, url, description 等)"
        "- count: 新聞數量"
        "- message: 錯誤訊息（當 status 為 'error' 時）"
        "\n"
        "請將返回的結構化數據以清晰易讀的格式呈現給使用者，"
        "包括新聞標題、來源和連結等資訊。"
        "如果使用者沒有指定國家，請詢問他們想了解哪個國家的新聞。"
    ),
    tools=[get_country_news, get_tech_news],
)