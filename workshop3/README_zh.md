# Workshop 3: Agent到Agent (A2A) 通訊與分散式架構

## 概述

本workshop展示如何建立Agent到Agent (A2A) 通訊系統，透過分散式架構讓多個專門化的agent協作完成複雜任務。您將學習如何建立orchestrator (協調器) agent來管理多個remote (遠端) agent。

## 學習目標

- 理解Agent到Agent (A2A) 通訊架構
- 學習建立專門化的遠端agent
- 實作orchestrator pattern進行agent協調
- 掌握分散式agent系統的部署和管理

## 專案結構

```
workshop3/
└── a2a-demo/
    ├── pyproject.toml           # 專案配置
    ├── orchestrator/            # 協調器服務
    │   ├── __main__.py         # 服務入口點
    │   ├── main.py
    │   └── agent/
    │       ├── __init__.py
    │       └── agent.py        # 協調器agent定義
    ├── remote_agents/           # 遠端agent服務
    │   ├── pyproject.toml
    │   ├── sentiment_analyzer_agent/   # 情感分析agent
    │   │   ├── Dockerfile
    │   │   ├── agent.py
    │   │   ├── agent_executor.py
    │   │   └── __init__.py
    │   └── business_analyzer_agent/    # 商業分析agent
    │       ├── Dockerfile
    │       ├── agent.py
    │       ├── agent_executor.py
    │       └── __init__.py
    └── Readme.md
```

## 核心概念

### 1. Agent到Agent (A2A) 通訊

A2A架構允許agent之間直接通訊，enabling:
- **模組化**: 每個agent專注於特定領域
- **可擴展性**: 可以動態添加新的專門agent
- **容錯性**: 單一agent失敗不影響整個系統

### 2. Orchestrator Pattern

Orchestrator agent協調多個specialist agent：

```python
root_agent = Agent(
    model='gemini-2.0-flash',
    name='orchestrator_agent',
    description='Agent that coordinates with remote agents for news analysis.',
    instruction="""
    You are an orchestrator agent that coordinates with specialized remote agents.
    You can delegate tasks to:
    - Sentiment Analyzer Agent: for sentiment analysis of news articles
    - Business Analyzer Agent: for business impact analysis
    """,
)
```

### 3. Remote Agent 特化

每個remote agent專注於特定功能：

**情感分析Agent**:
```python
root_agent = Agent(
    model='gemini-2.0-flash',
    name='sentiment_analyzer_agent',
    description='An agent that analyzes the sentiment of news articles.',
    tools=[get_news_article],
)
```

## 快速開始

### 前置要求

- Python 3.11+
- Docker (可選，用於容器化部署)

### 安裝相依套件

使用pyproject.toml進行套件管理：

```bash
cd workshop3/a2a-demo
pip install -e .
```

這將安裝包含A2A功能的Google ADK相依套件。

### 啟動遠端Agent

#### 啟動情感分析Agent

```bash
cd workshop3/a2a-demo
uvicorn remote_agents.sentiment_analyzer_agent.agent:a2a_app --host 0.0.0.0 --port 8001
```

#### 啟動商業分析Agent (如有需要)

```bash
uvicorn remote_agents.business_analyzer_agent.agent:a2a_app --host 0.0.0.0 --port 8002
```

### 啟動協調器Agent

在新的終端中：

```bash
cd workshop3/a2a-demo
uvicorn orchestrator.__main__:app --host 0.0.0.0 --port 8000
```

### 使用系統

1. 訪問協調器Web界面: `http://localhost:8000`
2. 與orchestrator agent互動
3. Agent會自動將專門任務委託給適當的remote agent

## 系統架構

### 通訊流程

1. **用戶請求** → Orchestrator Agent
2. **任務分析** → Orchestrator決定需要哪些specialist
3. **委託任務** → 向remote agent發送HTTP請求
4. **收集結果** → 從多個remote agent獲取回應
5. **整合回應** → Orchestrator整合結果並回應用戶

### Agent特化領域

- **Orchestrator Agent**: 任務協調和結果整合
- **Sentiment Analyzer Agent**: 新聞文章情感分析
- **Business Analyzer Agent**: 商業影響分析

## 範例使用情境

### 情感分析範例

```
用戶: "分析這個新聞連結的情感: https://example.com/news-article"

流程:
1. Orchestrator接收請求
2. 識別需要情感分析
3. 委託給Sentiment Analyzer Agent
4. Sentiment Agent使用get_news_article工具獲取內容
5. 分析情感並返回結果
6. Orchestrator整合結果回應用戶
```

### 多Agent協作範例

```
用戶: "分析這篇文章的情感和商業影響"

流程:
1. Orchestrator識別需要兩種分析
2. 並行委託給Sentiment和Business Analyzer
3. 收集兩個agent的結果
4. 整合comprehensive analysis回應
```

## Docker部署

### 建立Agent容器

每個remote agent都包含Dockerfile：

```bash
# 建立sentiment analyzer映像
cd workshop3/a2a-demo/remote_agents/sentiment_analyzer_agent
docker build -t sentiment-analyzer .

# 建立business analyzer映像
cd ../business_analyzer_agent
docker build -t business-analyzer .

# 建立orchestrator映像
cd ../../orchestrator
docker build -t orchestrator .
```

### 使用Docker Compose

建立docker-compose.yml來協調所有服務：

```yaml
version: '3.8'
services:
  sentiment-analyzer:
    image: sentiment-analyzer
    ports:
      - "8001:8001"
  
  business-analyzer:
    image: business-analyzer
    ports:
      - "8002:8002"
  
  orchestrator:
    image: orchestrator
    ports:
      - "8000:8000"
    depends_on:
      - sentiment-analyzer
      - business-analyzer
```

## 進階功能

### 環境配置

使用.env檔案配置remote agent URLs：

```
SENTIMENT_ANALYZER_URL=http://localhost:8001
BUSINESS_ANALYZER_URL=http://localhost:8002
```

### 錯誤處理與容錯

- **超時處理**: 設定適當的HTTP請求超時
- **重試機制**: 實作自動重試失敗的agent呼叫
- **降級策略**: 當remote agent不可用時的備用方案

### 負載平衡

- 為每種agent type部署多個實例
- 實作round-robin或智能路由

### 監控與日誌

- 添加distributed tracing
- 實作health check端點
- 集中化日誌收集

## 擴展練習

1. **新增Agent類型**:
   - 建立新的specialist agent (例如: 翻譯agent, 摘要agent)
   - 更新orchestrator以使用新agent

2. **改進協調邏輯**:
   - 實作條件式路由
   - 添加agent能力發現

3. **安全增強**:
   - 實作agent間認證
   - 添加API金鑰管理

4. **效能優化**:
   - 實作agent回應快取
   - 並行化多agent請求

## 疑難排解

### 常見問題

1. **Remote Agent連接失敗**:
   ```bash
   # 檢查agent是否運行
   curl http://localhost:8001/health
   ```

2. **埠號衝突**:
   ```bash
   # 檢查埠號使用情況
   lsof -i :8000
   ```

3. **相依套件問題**:
   ```bash
   # 重新安裝套件
   pip install -e . --force-reinstall
   ```

### 日誌檢查

啟用詳細日誌以診斷問題：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 部署到生產環境

### Google Cloud Run部署

1. **部署Remote Agent**:
```bash
gcloud run deploy sentiment-analyzer \
  --source ./remote_agents/sentiment_analyzer_agent \
  --platform managed \
  --region us-central1
```

2. **部署Orchestrator**:
```bash
gcloud run deploy orchestrator \
  --source ./orchestrator \
  --platform managed \
  --region us-central1 \
  --set-env-vars="SENTIMENT_ANALYZER_URL=https://sentiment-analyzer-xxx.run.app"
```

### 服務網格考量

在production環境中考慮使用Istio或類似服務網格來管理:
- 服務發現
- 流量管理  
- 安全策略
- 可觀測性

## 下一步

完成此workshop後，繼續學習：
- Workshop 4: 進階agent功能與外部模型整合
- 微服務架構最佳實踐
- Kubernetes上的agent部署

## 參考資源

- [Google ADK A2A文檔](https://docs.google.com/adk/a2a)
- [分散式系統設計模式](https://microservices.io/patterns/)
- [容器編排最佳實踐](https://kubernetes.io/docs/concepts/)