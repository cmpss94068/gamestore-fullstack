# 🎮 GameStore-Fullstack: 多平台遊戲資訊電商系統

本專案是一個整合 **JavaScript 數據爬蟲**、**Django REST Framework 後端** 與 **React 前端** 的全端 Side Project。主要目標是自動化抓取 PlayStation 與 Nintendo Switch 的遊戲資訊，並提供一個直觀的電商平台介面。

## 🚀 技術架構
- **Crawler**: 使用 Node.js + Axios + Cheerio 實現多平台資料抓取。
- **Backend**: 基於 Django 4.1 與 MySQL，實作 RESTful API 與 JWT 身份驗證。
- **Frontend**: React.js 構建的 SPA 介面，支援商品查詢與會員管理。

## 🛠️ 開發亮點
1. **資料自動化整合**：統一不同平台的日期與價格格式，自動匯入資料庫。
2. **安全性實作**：使用 `.env` 管理敏感資訊，並實作 JWT Token 驗證機制。
3. **系統擴展性**：後端預留了購物車與訂單模組的擴充空間。