# HA Rebrand

A Home Assistant custom component that allows you to customize the branding of your Home Assistant instance.

[中文說明](#中文說明)

## Features

- Replace Home Assistant logo with your own
- Custom favicon
- Custom sidebar title
- Custom document (browser tab) title
- **Primary color customization** (login page buttons, UI accents)
- Text replacement mapping (e.g., "Home Assistant" → "My Smart Home")
- Dark mode logo support
- Admin panel with drag-and-drop file upload
- **Security hardened** (XSS and CSS injection prevention)
- **Performance optimized** (pre-compiled regex, smart MutationObserver)

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add this repository URL and select "Integration" as the category
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Copy the `ha_rebrand` folder to your `custom_components` directory
2. Restart Home Assistant

## Configuration

### Option 1: Using the Admin Panel (Recommended)

1. After installation, go to the sidebar and click "Rebrand"
2. Configure your branding using the UI:
   - Upload your logo and favicon
   - Set your brand name and titles
   - Set your primary color (affects buttons and UI accents)
   - Add text replacements
3. Click "Apply Changes" to test your configuration
4. Click "Save to File" to create a permanent configuration

### Option 2: Manual YAML Configuration

Add the following to your `configuration.yaml`:

```yaml
ha_rebrand:
  brand_name: "My Smart Home"
  logo: "/local/my-logo.svg"
  logo_dark: "/local/my-logo-dark.svg"  # Optional
  favicon: "/local/favicon.ico"
  sidebar_title: "My Smart Home"
  document_title: "My Smart Home"
  primary_color: "#6183fc"  # Optional: Custom primary color
  replacements:
    "Home Assistant": "My Smart Home"
    "HA": "MSH"
```

### Enable the Injector Script

To enable automatic branding replacement throughout the interface, add the injector script to your Lovelace configuration.

Add this to your `configuration.yaml`:

```yaml
frontend:
  extra_module_url:
    - /local/ha_rebrand/ha-rebrand-injector.js
```

Then restart Home Assistant.

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `brand_name` | string | "Home Assistant" | The main brand name |
| `logo` | string | null | Path to logo image (supports `/local/` paths and URLs) |
| `logo_dark` | string | null | Path to dark mode logo (optional) |
| `favicon` | string | null | Path to favicon |
| `sidebar_title` | string | brand_name | Title shown in sidebar |
| `document_title` | string | brand_name | Browser tab title |
| `primary_color` | string | null | Primary color for buttons and UI (hex format: `#RRGGBB`) |
| `replacements` | dict | {} | Text replacement mapping |

## File Paths

Place your custom images in the `/config/www/` directory. They will be accessible via `/local/` URLs.

Example:
- File location: `/config/www/my-logo.svg`
- Configuration: `logo: "/local/my-logo.svg"`

Supported image formats:
- PNG
- JPG/JPEG
- SVG
- ICO (for favicon)
- WebP

## How It Works

1. **Backend Component**: Manages configuration, file uploads, and provides WebSocket/HTTP APIs
2. **Admin Panel**: Provides a user-friendly interface to configure branding
3. **Injector Script**: Runs on every page load and:
   - Replaces the favicon
   - Updates the document title
   - Replaces the sidebar logo and title
   - Applies primary color to login page and UI elements
   - Performs text replacements throughout the DOM
   - Monitors for dynamic content changes with optimized MutationObserver

## Security

This component includes security measures to prevent XSS and CSS injection attacks:
- All user-provided values are properly escaped before HTML/JavaScript injection
- Color values are validated against a strict regex pattern
- JavaScript strings are escaped to prevent script injection

## Troubleshooting

### Logo not showing

1. Make sure the file exists in `/config/www/`
2. Clear your browser cache
3. Check browser console for errors

### Text replacements not working

1. Ensure the injector script is loaded (check `frontend.extra_module_url`)
2. Restart Home Assistant after configuration changes
3. Hard refresh your browser (Ctrl+Shift+R)

### Primary color not applying

1. Use hex color format only (e.g., `#6183fc`)
2. Test in an incognito/private browser window to avoid cache issues
3. The primary color affects login page buttons and main UI accent colors

### Admin panel not appearing

1. Check if the component loaded successfully in the logs
2. Ensure you have admin privileges
3. Restart Home Assistant

## Limitations

- Some deeply nested elements in the HA core UI may not be replaced
- Text replacements work on visible text only, not on element attributes
- Changes to configuration require a page refresh to take effect
- Primary color only supports hex format (`#RGB`, `#RRGGBB`, or `#RRGGBBAA`)

## Version History

### 1.1.0
- Added primary color customization for login page and UI
- Security improvements: XSS and CSS injection prevention
- Performance optimization: pre-compiled regex patterns
- Optimized MutationObserver with mutation filtering and debouncing
- Improved code quality and logging

### 1.0.0
- Initial release
- Logo, favicon, and title customization
- Text replacement mapping
- Admin panel with file upload
- Dark mode logo support

## License

MIT License

## Support

For issues and feature requests, please use the GitHub issue tracker.

---

# 中文說明

HA Rebrand 是一個 Home Assistant 自定義組件，讓您可以自定義 Home Assistant 的品牌外觀。

## 功能特色

- 替換 Home Assistant 標誌為您自己的標誌
- 自定義網站圖標 (favicon)
- 自定義側邊欄標題
- 自定義瀏覽器標籤標題
- **主題色自定義**（登入頁面按鈕、UI 強調色）
- 文字替換對應（例如："Home Assistant" → "我的智慧家庭"）
- 深色模式標誌支援
- 管理面板，支援拖放上傳檔案
- **安全加固**（防止 XSS 和 CSS 注入攻擊）
- **效能優化**（預編譯正則表達式、智能 MutationObserver）

## 安裝方式

### HACS（推薦）

1. 在 Home Assistant 中開啟 HACS
2. 點擊「整合」(Integrations)
3. 點擊右上角的三個點，選擇「自定義存儲庫」
4. 添加此存儲庫 URL，並選擇「整合」作為類別
5. 點擊「安裝」
6. 重新啟動 Home Assistant

### 手動安裝

1. 將 `ha_rebrand` 資料夾複製到您的 `custom_components` 目錄
2. 重新啟動 Home Assistant

## 配置方式

### 方式一：使用管理面板（推薦）

1. 安裝後，在側邊欄點擊「Rebrand」
2. 使用 UI 配置您的品牌：
   - 上傳您的標誌和網站圖標
   - 設定品牌名稱和標題
   - 設定主題色（影響按鈕和 UI 強調色）
   - 添加文字替換規則
3. 點擊「套用變更」測試配置
4. 點擊「儲存到檔案」建立永久配置

### 方式二：手動 YAML 配置

在 `configuration.yaml` 中添加：

```yaml
ha_rebrand:
  brand_name: "我的智慧家庭"
  logo: "/local/my-logo.svg"
  logo_dark: "/local/my-logo-dark.svg"  # 可選
  favicon: "/local/favicon.ico"
  sidebar_title: "我的智慧家庭"
  document_title: "我的智慧家庭"
  primary_color: "#6183fc"  # 可選：自定義主題色
  replacements:
    "Home Assistant": "我的智慧家庭"
    "儀表板": "控制台"
```

### 啟用注入腳本

要在整個介面中啟用自動品牌替換，需將注入腳本添加到 Lovelace 配置中。

在 `configuration.yaml` 中添加：

```yaml
frontend:
  extra_module_url:
    - /local/ha_rebrand/ha-rebrand-injector.js
```

然後重新啟動 Home Assistant。

## 配置選項

| 選項 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `brand_name` | 字串 | "Home Assistant" | 主要品牌名稱 |
| `logo` | 字串 | null | 標誌圖片路徑（支援 `/local/` 路徑和 URL） |
| `logo_dark` | 字串 | null | 深色模式標誌路徑（可選） |
| `favicon` | 字串 | null | 網站圖標路徑 |
| `sidebar_title` | 字串 | brand_name | 側邊欄顯示的標題 |
| `document_title` | 字串 | brand_name | 瀏覽器標籤標題 |
| `primary_color` | 字串 | null | 按鈕和 UI 的主題色（十六進制格式：`#RRGGBB`） |
| `replacements` | 字典 | {} | 文字替換對應表 |

## 檔案路徑

將您的自定義圖片放在 `/config/www/` 目錄中，它們將可通過 `/local/` URL 訪問。

範例：
- 檔案位置：`/config/www/my-logo.svg`
- 配置：`logo: "/local/my-logo.svg"`

支援的圖片格式：
- PNG
- JPG/JPEG
- SVG
- ICO（用於網站圖標）
- WebP

## 運作原理

1. **後端組件**：管理配置、檔案上傳，並提供 WebSocket/HTTP API
2. **管理面板**：提供使用者友善的介面來配置品牌
3. **注入腳本**：在每次頁面載入時運行：
   - 替換網站圖標
   - 更新文件標題
   - 替換側邊欄標誌和標題
   - 將主題色應用到登入頁面和 UI 元素
   - 在整個 DOM 中執行文字替換
   - 使用優化的 MutationObserver 監控動態內容變更

## 安全性

此組件包含安全措施以防止 XSS 和 CSS 注入攻擊：
- 所有使用者提供的值在 HTML/JavaScript 注入前都會被正確轉義
- 顏色值會根據嚴格的正則表達式模式進行驗證
- JavaScript 字串會被轉義以防止腳本注入

## 疑難排解

### 標誌未顯示

1. 確保檔案存在於 `/config/www/`
2. 清除瀏覽器快取
3. 檢查瀏覽器控制台是否有錯誤

### 文字替換不起作用

1. 確保注入腳本已載入（檢查 `frontend.extra_module_url`）
2. 配置變更後重新啟動 Home Assistant
3. 強制重新整理瀏覽器（Ctrl+Shift+R）

### 主題色未套用

1. 僅使用十六進制顏色格式（例如：`#6183fc`）
2. 在無痕/私密瀏覽視窗中測試以避免快取問題
3. 主題色會影響登入頁面按鈕和主要 UI 強調色

### 管理面板未出現

1. 檢查組件是否在日誌中成功載入
2. 確保您具有管理員權限
3. 重新啟動 Home Assistant

## 限制

- HA 核心 UI 中某些深層嵌套的元素可能無法被替換
- 文字替換僅適用於可見文字，不適用於元素屬性
- 配置變更需要重新整理頁面才能生效
- 主題色僅支援十六進制格式（`#RGB`、`#RRGGBB` 或 `#RRGGBBAA`）

## 版本歷史

### 1.1.0
- 新增登入頁面和 UI 的主題色自定義功能
- 安全性改進：防止 XSS 和 CSS 注入
- 效能優化：預編譯正則表達式模式
- 優化 MutationObserver，增加變更過濾和防抖動
- 改進程式碼品質和日誌記錄

### 1.0.0
- 初始版本
- 標誌、網站圖標和標題自定義
- 文字替換對應
- 管理面板支援檔案上傳
- 深色模式標誌支援

## 授權條款

MIT License

## 支援

如有問題或功能請求，請使用 GitHub issue tracker。
