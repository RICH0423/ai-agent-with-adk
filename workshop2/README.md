# Workshop 2: Google Cloud Storage 整合與 MCP 伺服器

## 概述

本workshop示範如何建立整合Google Cloud Storage (GCS) 的AI Agent，透過Model Control Protocol (MCP) 伺服器架構實現agent與雲端儲存服務的互動。

## 學習目標

- 理解MCP (Model Control Protocol) 架構
- 學習Google Cloud Storage API整合
- 建立分散式agent服務架構
- 掌握環境變數管理和服務間通訊

## 專案結構

```
workshop2/
├── gcs-mcp-server/           # MCP 伺服器服務
│   ├── Dockerfile
│   ├── main.py              # GCS MCP 伺服器實作
│   └── requirements.txt
└── news-gcs-agent-service/   # Agent 服務
    ├── main.py              # Agent FastAPI 應用程式
    ├── requirements.txt
    └── news_assistant_agent/
        ├── __init__.py
        └── agent.py         # Agent 定義與MCP整合
```

## 核心概念

### 1. MCP 伺服器架構

MCP (Model Control Protocol) 允許agent與外部服務安全互動：

```python
from fastmcp import FastMCP
from google.cloud import storage

mcp = FastMCP("GCS MCP Server")

@mcp.tool()
async def create_gcs_file(bucket_name: str, destination_blob_name: str, content: str):
    """在GCS bucket中建立新檔案"""
```

### 2. Agent 與 MCP 整合

Agent通過MCPToolset連接到MCP伺服器：

```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseConnectionParams

gcs_toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url=f"{GCS_MCP_SERVER_URL}/sse",
        headers={"Accept": "text/event-stream, application/json"},
        timeout=30
    ),
    tool_filter=['create_gcs_file', 'list_gcs_files']
)
```

### 3. 雲端儲存操作

提供兩個主要GCS操作：

1. **create_gcs_file**: 建立新檔案到GCS bucket
2. **list_gcs_files**: 列出GCS bucket中的檔案

## 快速開始

### 前置要求

- Python 3.11+
- Google Cloud SDK
- 有效的Google Cloud專案
- GCS bucket權限

### 環境設定

1. 設定Google Cloud認證：
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. 建立環境變數檔案 (.env)：
```
GCS_MCP_SERVER_URL=https://your-mcp-server-url
GOOGLE_CLOUD_PROJECT=your-project-id
```

### 啟動 GCS MCP 伺服器

1. 進入MCP伺服器目錄：
```bash
cd workshop2/gcs-mcp-server
pip install -r requirements.txt
```

2. 啟動MCP伺服器：
```bash
python main.py
```

服務將在端口8080上運行，提供SSE端點用於agent連接。

### 啟動 Agent 服務

1. 進入agent服務目錄：
```bash
cd workshop2/news-gcs-agent-service
pip install -r requirements.txt
```

2. 啟動agent服務：
```bash
python main.py
```

3. 訪問 `http://localhost:8080` 使用Web界面

## 服務互動流程

1. **Agent接收用戶請求** → 生成新聞摘要
2. **Agent呼叫MCP工具** → 透過SSE連接到MCP伺服器
3. **MCP伺服器執行** → Google Cloud Storage API操作
4. **回傳結果** → Agent收到操作結果並回應用戶

## 關鍵功能

### GCS MCP 伺服器功能

- **檔案建立**: `create_gcs_file(bucket_name, filename, content)`
- **檔案列表**: `list_gcs_files(bucket_name, prefix=None)`
- **錯誤處理**: 完整的異常處理和日誌記錄
- **SSE通訊**: Server-Sent Events用於即時通訊

### Agent 功能

- **新聞生成**: 基於內建知識生成新聞摘要
- **自動存檔**: 自動將生成的內容存儲到GCS
- **雙步驟工作流程**:
  1. 生成內容 (模型任務)
  2. 存檔內容 (工具任務)

## Docker 部署

### 建立 MCP 伺服器映像

```bash
cd workshop2/gcs-mcp-server
docker build -t gcs-mcp-server .
docker run -p 8080:8080 -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json gcs-mcp-server
```

### 部署到 Google Cloud Run

```bash
# 部署MCP伺服器
gcloud run deploy gcs-mcp-server --source . --platform managed --region us-central1

# 部署Agent服務
cd ../news-gcs-agent-service
gcloud run deploy news-gcs-agent --source . --platform managed --region us-central1
```

## 使用範例

1. **生成並儲存新聞**:
   - "請生成關於AI發展的新聞摘要並儲存到GCS"
   
2. **查看已儲存檔案**:
   - "列出我的新聞bucket中的所有檔案"

3. **建立特定內容**:
   - "建立一個科技新聞摘要並存為'tech-news-summary.txt'"

## 進階配置

### 客製化MCP工具

您可以擴展MCP伺服器功能：

```python
@mcp.tool()
async def delete_gcs_file(bucket_name: str, blob_name: str):
    """刪除GCS檔案"""
    # 實作刪除邏輯
```

### Agent行為客製化

修改agent指令以改變其行為：

```python
root_agent = LlmAgent(
    name="custom_news_agent",
    instruction="您的客製化指令...",
    tools=all_tools,
)
```

## 疑難排解

### 常見問題

1. **MCP連接失敗**:
   - 確認MCP伺服器正在運行
   - 檢查URL配置正確

2. **GCS權限錯誤**:
   - 驗證Google Cloud認證
   - 確認bucket存在且有適當權限

3. **環境變數問題**:
   - 檢查.env檔案設定
   - 確認所有必需變數已設定

### 日誌檢查

```bash
# 查看MCP伺服器日誌
docker logs <mcp-container-id>

# 查看Agent服務日誌
docker logs <agent-container-id>
```

## 安全考量

- 使用Google Cloud IAM進行權限管理
- 不在程式碼中硬編碼憑證
- 使用環境變數管理敏感資訊
- 定期輪換API金鑰

## 下一步

完成此workshop後，建議繼續學習：
- Workshop 3: Agent到Agent通訊
- Workshop 4: 進階agent與外部模型整合

## 參考資源

- [Google ADK 文檔](https://docs.google.com/adk)
- [Google Cloud Storage API](https://cloud.google.com/storage/docs)
- [FastMCP 文檔](https://github.com/fastmcp/fastmcp)