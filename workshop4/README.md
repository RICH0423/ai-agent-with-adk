# Workshop 4: 進階 Agent 開發 - LiteLLM 與 Ollama 整合

## 概述

本workshop展示如何建立進階AI Agent，整合LiteLLM和Ollama來使用自託管的語言模型。您將學習如何設定本地模型服務、配置agent使用外部LLM端點，以及實作更複雜的NLP功能。

## 學習目標

- 理解LiteLLM框架與Google ADK整合
- 學習Ollama本地模型部署
- 掌握多模型環境配置
- 實作進階NLP工具整合 (NLTK)
- 建立production-ready agent服務

## 專案結構

```
workshop4/
├── news_agent_service/       # 主要agent服務
│   ├── Dockerfile
│   ├── main.py              # FastAPI應用程式入口
│   ├── requirements.txt     # Python相依套件
│   └── news_agent/
│       ├── __init__.py
│       └── agent.py         # LiteLLM agent定義
└── ollama-server/           # Ollama模型服務
    ├── Dockerfile
    └── requirements.txt
```

## 核心概念

### 1. LiteLLM 整合

LiteLLM提供統一介面來使用不同的語言模型：

```python
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

root_agent = LlmAgent(
   model=LiteLlm(
       model=OLLAMA_MODEL,           # "ollama/gemma:2b"
       api_base=OLLAMA_SERVICE_URL,  # 自託管端點
       api_key=API_KEY
   ),
   name="ollama_agent",
   instruction="You are a helpful assistant running on a self-hosted vLLM endpoint.",
)
```

### 2. Ollama 模型服務

Ollama允許在本地運行開源LLM模型：

- **輕量級部署**: 簡化的模型管理
- **API相容性**: 提供OpenAI相容的API
- **模型管理**: 自動下載和版本管理

### 3. 進階工具整合

Workshop4包含更豐富的工具集：

- **LiteLLM**: 多模型支援
- **Requests**: HTTP客戶端功能  
- **NLTK**: 自然語言處理工具
- **python-dotenv**: 環境配置管理

## 快速開始

### 前置要求

- Python 3.11+
- Docker和Docker Compose
- 至少8GB RAM (用於運行本地模型)

### 環境設定

1. 建立環境變數檔案 (.env)：
```bash
OLLAMA_SERVICE_URL=http://localhost:11434
GOOGLE_API_KEY=your_api_key_here
OLLAMA_MODEL=ollama/gemma:2b
```

### 啟動Ollama服務

#### 方法1: 使用Docker

```bash
cd workshop4/ollama-server
docker build -t ollama-server .
docker run -d -p 11434:11434 --name ollama-service ollama-server
```

#### 方法2: 本地安裝

```bash
# 安裝Ollama (macOS)
brew install ollama

# 啟動Ollama服務
ollama serve

# 拉取模型
ollama pull gemma:2b
```

### 啟動Agent服務

```bash
cd workshop4/news_agent_service
pip install -r requirements.txt

# 啟動agent服務
python main.py
```

服務將在 `http://localhost:8080` 啟動，包含Web UI。

## 系統架構

### 服務配置

```
[用戶] → [Agent Service:8080] → [Ollama Service:11434] → [Gemma 2B Model]
```

### 環境變數配置

- `OLLAMA_SERVICE_URL`: Ollama API端點
- `GOOGLE_API_KEY`: 備用API密鑰
- `OLLAMA_MODEL`: 指定使用的模型

## 進階功能

### 1. 多模型支援

LiteLLM允許在運行時切換模型：

```python
# 支援多種模型提供者
models = [
    "ollama/gemma:2b",           # 本地Ollama
    "openai/gpt-3.5-turbo",      # OpenAI
    "anthropic/claude-3-sonnet", # Anthropic
    "google/gemini-pro"          # Google
]
```

### 2. 進階NLP工具

整合NLTK進行文本處理：

```python
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    return scores
```

### 3. 客製化模型配置

調整模型參數以優化效能：

```python
root_agent = LlmAgent(
    model=LiteLlm(
        model=OLLAMA_MODEL,
        api_base=OLLAMA_SERVICE_URL,
        temperature=0.7,          # 控制創造性
        max_tokens=1000,          # 限制回應長度
        timeout=30                # 請求超時
    ),
    # ... 其他配置
)
```

## Docker Compose 部署

建立 `docker-compose.yml` 來協調所有服務：

```yaml
version: '3.8'
services:
  ollama-server:
    build: ./ollama-server
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    
  news-agent:
    build: ./news_agent_service
    ports:
      - "8080:8080"
    environment:
      - OLLAMA_SERVICE_URL=http://ollama-server:11434
      - PORT=8080
    depends_on:
      - ollama-server

volumes:
  ollama_data:
```

啟動完整環境：

```bash
docker-compose up -d
```

## 使用範例

### 基本對話

```
用戶: "你好，請介紹一下自己"
Agent: "我是運行在自託管Ollama端點上的AI助手，使用Gemma 2B模型為您提供幫助。"
```

### 新聞分析

```
用戶: "分析這篇新聞的主要觀點"
Agent: [使用本地模型處理並分析提供的新聞內容]
```

### NLP任務

```
用戶: "幫我總結這段文字的情感"
Agent: [使用NLTK工具進行情感分析]
```

## 效能優化

### 1. 模型選擇建議

| 模型 | 大小 | RAM需求 | 速度 | 準確度 |
|------|------|---------|------|--------|
| gemma:2b | 1.4GB | 3GB | 快 | 中等 |
| gemma:7b | 4.8GB | 8GB | 中等 | 高 |
| llama2:7b | 3.8GB | 6GB | 中等 | 高 |
| llama2:13b | 7.3GB | 12GB | 慢 | 很高 |

### 2. 快取策略

實作回應快取以提升效能：

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_model_call(prompt):
    return model.generate(prompt)
```

### 3. 並行處理

使用異步處理提升throughput：

```python
import asyncio

async def process_multiple_requests(requests):
    tasks = [process_request(req) for req in requests]
    return await asyncio.gather(*tasks)
```

## 監控與日誌

### 健康檢查

實作服務健康檢查端點：

```python
@app.get("/health")
async def health_check():
    try:
        # 檢查Ollama連接
        response = requests.get(f"{OLLAMA_SERVICE_URL}/api/tags")
        return {"status": "healthy", "ollama": "connected"}
    except:
        return {"status": "unhealthy", "ollama": "disconnected"}
```

### 效能監控

追蹤關鍵指標：

```python
import time
import logging

def log_request_duration(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logging.info(f"Request processed in {duration:.2f}s")
        return result
    return wrapper
```

## 疑難排解

### 常見問題

1. **Ollama模型下載失敗**:
   ```bash
   # 手動拉取模型
   ollama pull gemma:2b
   
   # 檢查可用模型
   ollama list
   ```

2. **記憶體不足**:
   ```bash
   # 使用較小的模型
   export OLLAMA_MODEL=ollama/gemma:2b
   
   # 監控記憶體使用
   docker stats
   ```

3. **連接超時**:
   ```bash
   # 增加超時設定
   export OLLAMA_TIMEOUT=60
   
   # 檢查服務狀態
   curl http://localhost:11434/api/tags
   ```

### 日誌檢查

```bash
# Docker容器日誌
docker logs ollama-service
docker logs news-agent-service

# 應用程式日誌
tail -f /var/log/agent.log
```

## 安全考量

### 1. API金鑰管理

```python
import os
from cryptography.fernet import Fernet

# 加密API金鑰
key = Fernet.generate_key()
f = Fernet(key)
encrypted_key = f.encrypt(os.environ['API_KEY'].encode())
```

### 2. 網路安全

- 使用HTTPS進行生產部署
- 實作API速率限制
- 配置適當的防火牆規則

### 3. 模型安全

- 驗證輸入以防止prompt injection
- 實作內容過濾
- 監控異常請求模式

## 生產部署

### Google Cloud Run部署

1. **建立容器映像**:
```bash
# 建立Ollama服務映像
cd ollama-server
gcloud builds submit --tag gcr.io/PROJECT_ID/ollama-server

# 建立Agent服務映像  
cd ../news_agent_service
gcloud builds submit --tag gcr.io/PROJECT_ID/news-agent
```

2. **部署服務**:
```bash
# 部署Ollama服務
gcloud run deploy ollama-server \
  --image gcr.io/PROJECT_ID/ollama-server \
  --platform managed \
  --memory 4Gi \
  --cpu 2

# 部署Agent服務
gcloud run deploy news-agent \
  --image gcr.io/PROJECT_ID/news-agent \
  --platform managed \
  --set-env-vars="OLLAMA_SERVICE_URL=https://ollama-server-xxx.run.app"
```

### Kubernetes部署

建立Kubernetes配置：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ollama-server:latest
        ports:
        - containerPort: 11434
        resources:
          requests:
            memory: "4Gi"
            cpu: "1"
          limits:
            memory: "8Gi" 
            cpu: "2"
```

## 擴展練習

1. **模型比較**:
   - 實作多模型A/B測試
   - 比較不同模型的效能和準確度

2. **進階工具整合**:
   - 添加向量搜尋功能
   - 整合文檔處理工具

3. **效能優化**:
   - 實作模型量化
   - 添加GPU加速支援

4. **監控儀表板**:
   - 建立Grafana儀表板
   - 實作預警系統

## 下一步

完成此workshop後，您可以探索：

- **向量資料庫整合** (Weaviate, Pinecone)
- **多模態AI** (圖像和文字處理)
- **分散式推理** (模型分片和負載平衡)
- **自動化模型微調** (LoRA, QLoRA)

## 參考資源

- [LiteLLM文檔](https://litellm.ai/docs/)
- [Ollama文檔](https://ollama.ai/docs)
- [Google ADK LiteLLM整合](https://docs.google.com/adk/litellm)
- [NLTK文檔](https://www.nltk.org/)
- [Docker最佳實踐](https://docs.docker.com/develop/dev-best-practices/)