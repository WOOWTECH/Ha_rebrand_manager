# HA Rebrand

一個 Home Assistant 自訂組件，讓您可以自訂 Home Assistant 實例的品牌外觀。

## 功能特性

- 用自訂 Logo 替換 Home Assistant 預設標誌（側邊欄、載入畫面、登入頁面、初始設定頁面）
- 自訂網站圖示 (Favicon)
- 自訂側邊欄標題
- 自訂瀏覽器標籤頁標題
- **主題色自訂**（登入頁面按鈕、粒子動畫、UI 強調色）
- **隱藏 Open Home Foundation 標誌**
- 深色模式 Logo 支援
- 管理面板支援拖放上傳檔案
- **安全加固**（防止 XSS 和 CSS 注入攻擊）
- **效能優化**（預編譯正規表示式、智慧 MutationObserver）

## 安裝方法

### HACS 安裝（推薦）

> **前置條件：** 您的 Home Assistant 必須已安裝 [HACS](https://hacs.xyz/)。

#### 步驟 1：新增自訂儲存庫

1. 開啟 Home Assistant 網頁介面
2. 點擊側邊欄的 **HACS**
3. 點擊 **整合** 標籤
4. 點擊右上角的 **三點選單 (⋮)**
5. 選擇 **自訂儲存庫**

#### 步驟 2：輸入儲存庫資訊

1. 在 **儲存庫** 欄位貼上：
   ```
   https://github.com/WOOWTECH/Ha_rebrand_manager
   ```
2. 在 **類別** 下拉選單中選擇 **Integration**
3. 點擊 **新增**
4. 關閉對話框

#### 步驟 3：下載整合

1. 點擊右下角的 **+ 探索並下載儲存庫** 按鈕
2. 搜尋 **HA Rebrand**
3. 點擊它以開啟詳細資訊
4. 點擊 **下載** 按鈕
5. 在彈出視窗中確認下載

#### 步驟 4：重新啟動並設定

1. 前往 **設定** → **系統** → **重新啟動**
2. 等待 Home Assistant 完全重新啟動
3. 前往 **設定** → **裝置與服務**
4. 點擊右下角的 **+ 新增整合**
5. 搜尋 **HA Rebrand** 並選擇它
6. 完成設定精靈

安裝完成後，點擊側邊欄的 **Rebrand** 來設定您的品牌外觀。

### 手動安裝

1. 下載本儲存庫
2. 將 `custom_components/ha_rebrand` 資料夾複製到您的 Home Assistant `config/custom_components/` 目錄
3. 重新啟動 Home Assistant
4. 前往 設定 → 裝置與服務 → 新增整合 → 搜尋 "HA Rebrand"

## 設定方法

### 方式一：使用管理面板（推薦）

1. 安裝完成後，在側邊欄點擊「Rebrand」
2. 使用介面設定您的品牌：
   - 上傳您的 Logo 和網站圖示
   - 設定品牌名稱和標題
   - 設定主題色（影響按鈕和 UI 強調色）
   - 切換「隱藏 Open Home Foundation」選項
3. 點擊「套用變更」測試設定
4. 點擊「儲存到檔案」建立永久設定

### 方式二：YAML 設定檔

在管理面板中點擊「儲存到檔案」時，會在設定目錄中建立 `ha_rebrand.yaml` 檔案。此檔案會在啟動時載入以保留您的設定。

您也可以手動建立或編輯此檔案：

```yaml
# /config/ha_rebrand.yaml
system_name: "我的智慧家居"
logo: "/local/my-logo.svg"
logo_dark: "/local/my-logo-dark.svg"  # 可選
favicon: "/local/favicon.ico"
sidebar_text: "我的智慧家居"
browser_tab_title: "我的智慧家居"
primary_color: "#6183fc"  # 可選：自訂主題色
hide_open_home_foundation: true  # 可選：隱藏 OHF 標誌
```

**注意：**
- 管理面板將執行時設定儲存在 `www/ha_rebrand/config.json`
- 注入腳本會自動載入，無需手動設定 `frontend.extra_module_url`

## 設定選項

| 選項 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `system_name` | 字串 | "Home Assistant" | 用於無障礙功能和系統參考的名稱 |
| `logo` | 字串 | null | Logo 圖片路徑（支援 `/local/` 路徑和 URL） |
| `logo_dark` | 字串 | null | 深色模式 Logo 路徑（可選） |
| `favicon` | 字串 | null | 網站圖示路徑 |
| `sidebar_text` | 字串 | system_name | 顯示在側邊欄頂部的文字 |
| `browser_tab_title` | 字串 | system_name | 顯示在瀏覽器分頁中的名稱 |
| `primary_color` | 字串 | null | 按鈕和 UI 的主題色（十六進位格式：`#RGB`、`#RRGGBB` 或 `#RRGGBBAA`） |
| `hide_open_home_foundation` | 布林 | true | 隱藏 Open Home Foundation 標誌 |

## 檔案路徑說明

**管理面板上傳：** 透過管理面板上傳的檔案會儲存在 `/config/www/ha_rebrand/`，可透過 `/local/ha_rebrand/` URL 存取。

**手動放置：** 您也可以直接將自訂圖片放在 `/config/www/` 目錄中，它們可透過 `/local/` URL 存取。

範例：
- 管理面板上傳：`/config/www/ha_rebrand/logo.png` → `/local/ha_rebrand/logo.png`
- 手動放置：`/config/www/my-logo.svg` → `/local/my-logo.svg`

支援的圖片格式（最大 5MB）：
- PNG
- JPG/JPEG
- SVG
- ICO（用於網站圖示）
- WebP

## 設定顯示位置對照表

| 設定項 | 顯示位置 |
|--------|----------|
| `system_name` | 無障礙功能、系統參考、Logo alt 文字 |
| `sidebar_text` | 側邊欄頂部標題區域 |
| `browser_tab_title` | 瀏覽器標籤頁標題（例如：「總覽 – 名稱」） |
| `logo` | 側邊欄頂部 Logo 區域、載入畫面、登入頁面 |
| `logo_dark` | 深色模式下的 Logo |
| `favicon` | 瀏覽器標籤頁圖示 |
| `primary_color` | 登入頁面按鈕、粒子動畫、UI 強調色 |
| `hide_open_home_foundation` | 隱藏 OHF 標誌 |

## 運作原理

1. **後端組件**：管理設定、檔案上傳，並提供 WebSocket/HTTP API
2. **管理面板**：提供使用者友善的介面來設定品牌
3. **載入畫面**：修補 Home Assistant 的 IndexView，在頁面載入時立即顯示自訂 Logo
4. **登入頁面**：自訂授權視圖替換登入頁面 Logo 並套用主題色（包含粒子動畫）
5. **初始設定頁面**：自訂初始設定視圖在首次設定時套用品牌
6. **注入腳本**：在每次頁面載入時執行：
   - 替換網站圖示
   - 更新文件標題
   - 替換側邊欄 Logo 和標題
   - 將主題色套用到 UI 元素
   - 替換對話框和 QR 碼中的 Logo
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
- 設定變更需要重新整理頁面才能生效
- 主題色僅支援十六進位格式（`#RGB`、`#RRGGBB` 或 `#RRGGBBAA`）
- 切換淺色/深色模式後，需要重新整理頁面才能看到對應的 Logo

## 授權條款

MIT License

## 支援

如有問題或功能建議，請使用 GitHub Issue 追蹤器。
