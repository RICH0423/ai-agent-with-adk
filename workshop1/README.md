# Workshop 1: 基本 AI Agent 開發

## 概述

這個workshop將教您如何使用Google Agent Development Kit (ADK) 建立一個基本的AI Agent。本例建立了一個新聞助手agent，可以根據城市名稱取得新聞資訊。

## 學習目標

- 了解Google ADK的基本概念
- 學習如何定義Agent工具函數
- 建立FastAPI應用程式來服務Agent
- 部署到Google Cloud Run

## 專案結構

```
workshop1/
├── main.py                    # FastAPI 應用程式入口點
├── requirements.txt           # Python 相依套件
└── news_assistant_agent/      # Agent 定義目錄
    ├── __init__.py
    └── agent.py              # Agent 和工具定義
```

## 核心概念

### 1. Agent 定義

在 `news_assistant_agent/agent.py` 中，我們定義了一個基本的AI agent：

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="news_assistant_agent",
    model="gemini-2.0-flash",
    description="Agent to retrieve news for any particular city.",
    instruction="You are a helpful agent who can answer user questions related to news of any city.",
    tools=[get_news],
)
```

### 2. 工具函數 - news_assistant_agent

工具函數讓Agent能夠執行特定任務：

```python
def get_news(city: str) -> dict:
    """Retrieves the news of a particular city.
    Args:
        city (str): The name of the city for which to retrieve the news.
    Returns:
        dict: headline and content of the news, or error message.
    """
```

### 3. FastAPI 整合

使用 `google.adk.cli.fast_api.get_fast_api_app()` 創建Web界面：

```python
from google.adk.cli.fast_api import get_fast_api_app

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_SERVICE_URI,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)
```

## 快速開始

### 前置要求

- Python 3.11+
- Google Cloud SDK (可選，用於部署)

### 本地運行

1. 安裝相依套件：
```bash
cd workshop1
pip install -r requirements.txt
```

2. 設定API Key
```
export GOOGLE_API_KEY=$GOOGLE_API_KEY
```

3. 啟動服務：
```bash
python main.py
```
或
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

4. 打開瀏覽器訪問 `http://localhost:8000` 來使用Web界面

---

### 使用Tools串接外部API (news_assistant_agent2)

1. 註冊News API並取得API Key
2. 設定API Key
```
export NEWS_API_KEY=$NEWS_API_KEY
```

### 使用Agent

啟動服務後，您可以：

1. 透過Web界面與agent互動
2. 詢問特定城市的新聞，例如："告訴我班加羅爾的新聞"
3. Agent會使用 `get_news` 工具函數來回應

## 關鍵特色

- **簡單的工具整合**: 示範如何將Python函數作為agent工具
- **Web界面**: 提供即用的聊天界面
- **會話管理**: 使用SQLite進行會話儲存
- **CORS支援**: 配置跨域請求
- **Cloud Run準備**: 環境變數配置適合雲端部署

## 擴展練習

1. **新增更多城市**: 修改 `get_news` 函數以支援更多城市
2. **新增新工具**: 創建額外的工具函數 (例如天氣查詢)
3. **改進錯誤處理**: 增強錯誤訊息和異常處理
4. **客製化回應**: 修改agent指令以改變回應風格

## 部署到 Google Cloud Run

1. 確保您有有效的 Google Cloud 專案
2. 使用 Google Cloud Build 或 Docker 建立容器映像
3. 部署到 Cloud Run 服務

## 疑難排解

- 確保所有相依套件正確安裝
- 檢查埠號是否可用 (預設: 8080)
- 驗證agent目錄結構正確

## 下一步

完成這個workshop後，您可以繼續學習：
- Workshop 2: Google Cloud Storage 整合
- Workshop 3: Agent到Agent通訊
- Workshop 4: 進階agent功能
