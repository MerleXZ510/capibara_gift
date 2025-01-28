# Python 驗證碼辨識系統

## 功能需求
- 建立一個 API endpoint 用於接收:
  - 遊戲 ID
  - 序號
  - 驗證碼圖片

## 環境建置
使用 Docker Compose 進行開發和部署:

### 開發環境
```bash
# 啟動服務
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

### 生產環境
```bash
# 建構映像檔
docker build -t captcha-service .

# 運行容器
docker run -d -p 8000:8000 captcha-service
```

## API 使用說明

### 驗證碼辨識 API
- 端點: `POST /api/captcha`
- Content-Type: `multipart/form-data`

請求參數:
- game_id: string (必填)
- serial_number: string (必填)
- image: file (必填)

回應格式:
```json
{
    "success": true,
    "result": "辨識結果",
    "message": "處理訊息"
}
```

使用範例:
```bash
curl -X POST "http://localhost:8000/api/captcha" \
     -F "game_id=game123" \
     -F "serial_number=SN123" \
     -F "image=@/path/to/captcha.png"
```

## 開發注意事項
1. 確保圖片處理效能
2. 實作適當的錯誤處理機制
3. 加入日誌記錄功能
4. 考慮加入速率限制
5. 實作基本的安全防護措施

## 待辦事項
- [x] 建立基本 API 架構
- [x] 實作圖片上傳功能
- [x] 整合 OCR 辨識功能
- [x] 加入錯誤處理
- [ ] 撰寫單元測試
- [ ] 優化辨識準確度

## 系統需求
- Python 3.9+
- Docker
- tesseract-ocr

## 開發工具
- FastAPI
- Pytesseract
- Pillow
- Loguru

## API 文檔
系統運行後，可以通過以下網址訪問 Swagger 文檔：
- http://localhost:8000/docs
- http://localhost:8000/redoc