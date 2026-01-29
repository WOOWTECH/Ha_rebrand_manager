# HA Rebrand

一個 Home Assistant 自訂組件，讓您可以自訂 Home Assistant 實例的品牌外觀。

## 功能特性

- 用自訂 Logo 替換 Home Assistant 預設標誌
- 自訂網站圖示 (Favicon)
- 自訂側邊欄標題
- 自訂瀏覽器標籤頁標題
- 文字替換對應（例如：「Home Assistant」→「我的智慧家居」）
- 深色模式 Logo 支援
- 管理面板支援拖放上傳檔案

## 安裝方法

### HACS 安裝（推薦）

1. 在 Home Assistant 中開啟 HACS
2. 點擊「整合」
3. 點擊右上角的三個點，選擇「自訂儲存庫」
4. 新增本儲存庫 URL，類別選擇「Integration」
5. 點擊「安裝」
6. 重新啟動 Home Assistant

### 手動安裝

1. 將本儲存庫複製到您的 `custom_components/ha_rebrand` 目錄
2. 重新啟動 Home Assistant

## 設定方法

### 方式一：使用管理面板（推薦）

1. 安裝完成後，在側邊欄點擊「Rebrand」
2. 使用介面設定您的品牌：
   - 上傳您的 Logo 和網站圖示
   - 設定品牌名稱和標題
   - 新增文字替換規則
3. 點擊「套用變更」測試設定
4. 點擊「儲存到檔案」建立永久設定

### 方式二：手動 YAML 設定

在 `configuration.yaml` 中新增以下內容：

```yaml
ha_rebrand:
  brand_name: "我的智慧家居"
  logo: "/local/my-logo.svg"
  logo_dark: "/local/my-logo-dark.svg"  # 可選
  favicon: "/local/favicon.ico"
  sidebar_title: "我的智慧家居"
  document_title: "我的智慧家居"
  replacements:
    "Home Assistant": "我的智慧家居"
    "HA": "智家"
```

### 啟用注入腳本

要在整個介面啟用自動品牌替換，需要將注入腳本新增到 Lovelace 設定中。

在 `configuration.yaml` 中新增：

```yaml
frontend:
  extra_module_url:
    - /local/ha_rebrand/ha-rebrand-injector.js
```

然後重新啟動 Home Assistant。

## 設定選項

| 選項 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `brand_name` | 字串 | "Home Assistant" | 主品牌名稱 |
| `logo` | 字串 | null | Logo 圖片路徑（支援 `/local/` 路徑和 URL） |
| `logo_dark` | 字串 | null | 深色模式 Logo 路徑（可選） |
| `favicon` | 字串 | null | 網站圖示路徑 |
| `sidebar_title` | 字串 | brand_name | 側邊欄顯示的標題 |
| `document_title` | 字串 | brand_name | 瀏覽器標籤頁標題 |
| `replacements` | 字典 | {} | 文字替換對應 |

## 檔案路徑說明

將自訂圖片放在 `/config/www/` 目錄中，它們可以透過 `/local/` URL 存取。

範例：
- 檔案位置：`/config/www/my-logo.svg`
- 設定寫法：`logo: "/local/my-logo.svg"`

支援的圖片格式：
- PNG
- JPG/JPEG
- SVG
- ICO（用於網站圖示）
- WebP

## 設定顯示位置對照表

| 設定項 | 顯示位置 |
|--------|----------|
| `brand_name` | 設定頁面標題、關於頁面、系統資訊 |
| `sidebar_title` | 側邊欄頂部標題區域 |
| `document_title` | 瀏覽器標籤頁標題（例如：「總覽 – 品牌名稱」） |
| `logo` | 側邊欄頂部 Logo 區域 |
| `logo_dark` | 深色模式下的側邊欄 Logo |
| `favicon` | 瀏覽器標籤頁圖示 |
| `replacements` | 整個介面中符合的文字 |

## 運作原理

1. **後端組件**：管理設定、檔案上傳，並提供 WebSocket/HTTP API
2. **管理面板**：提供使用者友善的介面來設定品牌
3. **注入腳本**：在每次頁面載入時執行，執行以下操作：
   - 替換網站圖示
   - 更新文件標題
   - 替換側邊欄 Logo 和標題
   - 在整個 DOM 中執行文字替換
   - 監控動態內容變化

## 常見問題排解

### Logo 不顯示

1. 確保檔案存在於 `/config/www/` 目錄
2. 清除瀏覽器快取
3. 檢查瀏覽器主控台是否有錯誤

### 文字替換不生效

1. 確保注入腳本已載入（檢查 `frontend.extra_module_url`）
2. 設定變更後重新啟動 Home Assistant
3. 強制重新整理瀏覽器（Ctrl+Shift+R）

### 管理面板不顯示

1. 檢查日誌中組件是否成功載入
2. 確保您具有管理員權限
3. 重新啟動 Home Assistant

## 限制說明

- HA 核心 UI 中某些深層巢狀的元素可能無法被替換
- 文字替換僅作用於可見文字，不影響元素屬性
- 設定變更需要重新整理頁面才能生效

## 版本歷史

### 2.0.0
- 新增 Config Flow 支援 UI 設定
- 新增深色/淺色模式支援
- 新增繁體中文翻譯
- 修復側邊欄 Logo 注入問題
- 改進錯誤處理

### 1.0.0
- 初始版本
- Logo、網站圖示和標題自訂
- 文字替換對應
- 管理面板支援檔案上傳
- 深色模式 Logo 支援

## 授權條款

MIT License

## 支援

如有問題或功能建議，請使用 GitHub Issue 追蹤器。
