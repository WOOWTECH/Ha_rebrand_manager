# HA Rebrand

一個 Home Assistant 自訂組件，讓您可以自訂 Home Assistant 實例的品牌外觀。

## 功能特性

- 用自訂 Logo 替換 Home Assistant 預設標誌（側邊欄、載入畫面、登入頁面）
- 自訂網站圖示 (Favicon)
- 自訂側邊欄標題
- 自訂瀏覽器標籤頁標題
- **主題色自訂**（登入頁面按鈕、UI 強調色）
- **隱藏 Open Home Foundation 標誌**
- 文字替換對應（例如：「Home Assistant」→「我的智慧家居」）
- 深色模式 Logo 支援
- 管理面板支援拖放上傳檔案
- **安全加固**（防止 XSS 和 CSS 注入攻擊）
- **效能優化**（預編譯正規表示式、智慧 MutationObserver）

## 安裝方法

### HACS 安裝（推薦）

1. 在 Home Assistant 中開啟 HACS
2. 點擊「整合」
3. 點擊右上角的三個點，選擇「自訂儲存庫」
4. 新增本儲存庫 URL，類別選擇「Integration」
5. 點擊「安裝」
6. 重新啟動 Home Assistant

### 手動安裝

1. 將 `ha_rebrand` 資料夾複製到您的 `custom_components` 目錄
2. 重新啟動 Home Assistant
3. 前往 設定 → 裝置與服務 → 新增整合 → 搜尋 "HA Rebrand"

## 設定方法

### 方式一：使用管理面板（推薦）

1. 安裝完成後，在側邊欄點擊「Rebrand」
2. 使用介面設定您的品牌：
   - 上傳您的 Logo 和網站圖示
   - 設定品牌名稱和標題
   - 設定主題色（影響按鈕和 UI 強調色）
   - 切換「隱藏 Open Home Foundation」選項
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
  primary_color: "#6183fc"  # 可選：自訂主題色
  hide_open_home_foundation: true  # 可選：隱藏 OHF 標誌
  replacements:
    "Home Assistant": "我的智慧家居"
    "HA": "智家"
```

**注意：** 注入腳本會自動載入，無需手動設定 `frontend.extra_module_url`。

## 設定選項

| 選項 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `brand_name` | 字串 | "Home Assistant" | 主品牌名稱 |
| `logo` | 字串 | null | Logo 圖片路徑（支援 `/local/` 路徑和 URL） |
| `logo_dark` | 字串 | null | 深色模式 Logo 路徑（可選） |
| `favicon` | 字串 | null | 網站圖示路徑 |
| `sidebar_title` | 字串 | brand_name | 側邊欄顯示的標題 |
| `document_title` | 字串 | brand_name | 瀏覽器標籤頁標題 |
| `primary_color` | 字串 | null | 按鈕和 UI 的主題色（十六進位格式：`#RRGGBB`） |
| `hide_open_home_foundation` | 布林 | true | 隱藏 Open Home Foundation 標誌 |
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
| `logo` | 側邊欄頂部 Logo 區域、載入畫面、登入頁面 |
| `logo_dark` | 深色模式下的 Logo |
| `favicon` | 瀏覽器標籤頁圖示 |
| `primary_color` | 登入頁面按鈕、UI 強調色 |
| `hide_open_home_foundation` | 隱藏 OHF 標誌 |
| `replacements` | 整個介面中符合的文字 |

## 運作原理

1. **後端組件**：管理設定、檔案上傳，並提供 WebSocket/HTTP API
2. **管理面板**：提供使用者友善的介面來設定品牌
3. **載入畫面**：修補 Home Assistant 的 IndexView，在頁面載入時立即顯示自訂 Logo
4. **登入頁面**：自訂授權視圖替換登入頁面 Logo 並套用主題色
5. **注入腳本**：在每次頁面載入時執行：
   - 替換網站圖示
   - 更新文件標題
   - 替換側邊欄 Logo 和標題
   - 將主題色套用到 UI 元素
   - 在整個 DOM 中執行文字替換
   - 使用優化的 MutationObserver 監控動態內容變化

## 安全性

此組件包含安全措施以防止 XSS 和 CSS 注入攻擊：
- 所有使用者提供的值在 HTML/JavaScript 注入前都會被正確跳脫
- 顏色值會根據嚴格的正規表示式模式進行驗證
- JavaScript 字串會被跳脫以防止腳本注入
- 檔案上傳會驗證類型、副檔名和大小（最大 5MB）

## 常見問題排解

### Logo 不顯示

1. 確保檔案存在於 `/config/www/` 目錄
2. 清除瀏覽器快取
3. 檢查瀏覽器主控台是否有錯誤

### 文字替換不生效

1. 設定變更後重新啟動 Home Assistant
2. 強制重新整理瀏覽器（Ctrl+Shift+R）

### 主題色未套用

1. 僅使用十六進位顏色格式（例如：`#6183fc`）
2. 在無痕/私密瀏覽視窗中測試以避免快取問題
3. 主題色會影響登入頁面按鈕和主要 UI 強調色

### 管理面板不顯示

1. 檢查日誌中組件是否成功載入
2. 確保您具有管理員權限
3. 重新啟動 Home Assistant

### 遠端存取無法使用（卡在「載入資料中」）

如果您使用反向代理（Nginx Proxy Manager、Cloudflare Tunnel 等），且遠端存取失敗但本機存取正常：

**1. 在 Home Assistant 中設定 `trusted_proxies`**

在您的 `configuration.yaml` 中新增以下內容：

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.30.32.0/23   # Supervisor 網路（Core + Add-ons）
    - 127.0.0.1        # 本機
    - ::1              # IPv6 本機
```

**為什麼是 `172.30.32.0/23`？** 此 CIDR 涵蓋：
- `172.30.32.0/24` - Home Assistant Core 服務
- `172.30.33.0/24` - 附加元件（包括 Nginx Proxy Manager、Cloudflared）

**2. 設定 Nginx Proxy Manager**

1. 開啟 NPM 管理面板（`http://<ha-ip>:81`）
2. 編輯您的 Home Assistant 代理主機
3. 在 **Details** 標籤頁：啟用 **WebSockets Support**
4. 在 **Advanced** 標籤頁：**刪除所有自訂 nginx 設定**（NPM 會自動處理 WebSocket）
5. 儲存

**3. 如果看到「Congratulations」頁面而非 Home Assistant**

這表示 NPM 無法解析主機名稱。請變更轉發主機名稱：
1. 在 NPM 中編輯代理主機
2. 將 **Forward Hostname / IP** 從 `homeassistant` 改為 `172.30.32.1`
3. **Forward Port** 保持 `8123`
4. 儲存

**4. 確認問題是否由 ha_rebrand 引起**

暫時停用 ha_rebrand 進行測試：
- 前往 設定 → 裝置與服務 → HA Rebrand → 停用
- 重新啟動 Home Assistant 並測試遠端存取
- 如果停用後恢復正常，請在 GitHub 上回報問題

詳細技術說明請參閱 [Proxy_Issue_Solution_Plan.md](Proxy_Issue_Solution_Plan.md)。

## 限制說明

- HA 核心 UI 中某些深層巢狀的元素可能無法被替換
- 文字替換僅作用於可見文字，不影響元素屬性
- 設定變更需要重新整理頁面才能生效
- 主題色僅支援十六進位格式（`#RGB`、`#RRGGBB` 或 `#RRGGBBAA`）
- 切換淺色/深色模式後，需要重新整理頁面才能看到對應的 Logo

## 版本歷史

### 2.1.0
- 自動載入注入腳本（無需手動設定 frontend）
- 載入畫面 Logo 替換（修補 IndexView）
- 自訂登入/授權頁面品牌
- 隱藏 Open Home Foundation 選項
- 改進安全性驗證

### 2.0.0
- 新增 Config Flow 支援 UI 設定
- 新增深色/淺色模式支援
- 新增繁體中文翻譯
- 修復側邊欄 Logo 注入問題
- 改進錯誤處理

### 1.1.0
- 新增登入頁面和 UI 的主題色自訂功能
- 安全性改進：防止 XSS 和 CSS 注入
- 效能優化：預編譯正規表示式模式
- 優化 MutationObserver，增加變更過濾和防抖動
- 改進程式碼品質和日誌記錄

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
