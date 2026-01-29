# HA Rebrand - 產品需求文件 (PRD)

## 版本: 1.5.0
## 最後更新: 2026-01-29

---

## 1. 產品概述

**HA Rebrand** 是一個 Home Assistant 自訂組件，允許用戶將 Home Assistant 介面中的所有品牌元素替換為自訂品牌。

### 1.1 目標用戶
- 智慧家居系統整合商
- 企業/組織內部部署
- 個人用戶想要個性化介面

### 1.2 核心功能
1. 替換側邊欄標題 (Sidebar Title)
2. 替換瀏覽器標題 (Document Title)
3. 替換 Logo 圖片（支援深淺色模式）
4. 替換 Favicon
5. 文字替換對應表 (Text Replacements)

---

## 2. 品牌替換位置詳細說明

### 2.1 側邊欄區域 (Sidebar)

| 位置 | 元素 | 選擇器 | 替換方式 |
|------|------|--------|----------|
| 側邊欄頂部標題 | "Home Assistant" 文字 | `ha-sidebar` → shadowRoot → `.title` | 直接替換 textContent |
| 側邊欄 Logo | HA 圖示 | `ha-sidebar` → shadowRoot → `.menu .logo` | 隱藏原始 Logo，插入自訂 `<img>` |

### 2.2 瀏覽器標題 (Document Title)

| 位置 | 元素 | 選擇器 | 替換方式 |
|------|------|--------|----------|
| 瀏覽器標籤頁標題 | `<title>` | `document.title` | 使用 MutationObserver 監控並替換 |

### 2.3 Favicon

| 位置 | 元素 | 選擇器 | 替換方式 |
|------|------|--------|----------|
| 網站圖示 | `<link rel="icon">` | `link[rel*="icon"]` | 替換 href 屬性 |
| Apple Touch Icon | `<link rel="apple-touch-icon">` | `link[rel="apple-touch-icon"]` | 替換或建立 |

### 2.4 文字替換 (Text Replacements)

| 位置 | 範圍 | 替換方式 |
|------|------|----------|
| 主文件 | `document.body` 內所有文字節點 | TreeWalker 遍歷並替換 |
| Shadow DOM | 所有自訂元素的 shadowRoot | 遞迴遍歷 shadowRoot |
| 動態內容 | 新增的 DOM 元素 | MutationObserver 監控 |

---

## 3. 架構設計

### 3.1 檔案結構

```
custom_components/ha_rebrand/
├── __init__.py              # 主要後端邏輯
├── manifest.json            # 組件定義
├── frontend/
│   ├── ha-rebrand-panel.js  # 管理員 UI 面板
│   └── ha-rebrand-injector.js # 品牌注入腳本
├── PRD.md                   # 本文件
└── README.md                # 使用說明
```

### 3.2 資料流

```
┌─────────────────────────────────────────────────────────────────┐
│                        Home Assistant                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  configuration.yaml         __init__.py                          │
│  ┌──────────────┐          ┌──────────────────┐                 │
│  │ ha_rebrand:  │ ──────▶  │ async_setup()    │                 │
│  │   brand_name │          │   - 載入設定      │                 │
│  │   logo       │          │   - 註冊 API      │                 │
│  │   favicon    │          │   - 註冊 Panel    │                 │
│  │   ...        │          └────────┬─────────┘                 │
│  └──────────────┘                   │                            │
│                                     ▼                            │
│                    ┌────────────────────────────────┐           │
│                    │      HTTP API Endpoints        │           │
│                    ├────────────────────────────────┤           │
│                    │ GET /api/ha_rebrand/config     │◀──┐       │
│                    │ POST /api/ha_rebrand/upload    │   │       │
│                    │ POST /api/ha_rebrand/save_config│  │       │
│                    └────────────────────────────────┘   │       │
│                                                          │       │
│                    ┌────────────────────────────────┐   │       │
│                    │     WebSocket Commands         │   │       │
│                    ├────────────────────────────────┤   │       │
│                    │ ha_rebrand/get_config          │   │       │
│                    │ ha_rebrand/update_config       │   │       │
│                    └────────────────────────────────┘   │       │
│                                                          │       │
└──────────────────────────────────────────────────────────┼───────┘
                                                           │
┌──────────────────────────────────────────────────────────┼───────┐
│                        瀏覽器端                           │       │
├──────────────────────────────────────────────────────────┼───────┤
│                                                          │       │
│  ha-rebrand-injector.js                                  │       │
│  ┌─────────────────────────────────────────────────┐    │       │
│  │ 1. fetchConfig() ─────────────────────────────────────┘       │
│  │ 2. replaceFavicon()                              │            │
│  │ 3. replaceDocumentTitle()                        │            │
│  │ 4. replaceSidebar()                              │            │
│  │ 5. replaceText()                                 │            │
│  │ 6. setupMutationObserver()                       │            │
│  └─────────────────────────────────────────────────┘            │
│                                                                  │
│  ha-rebrand-panel.js (管理員面板)                                │
│  ┌─────────────────────────────────────────────────┐            │
│  │ - 顯示/編輯品牌設定                               │            │
│  │ - 上傳 Logo/Favicon                              │            │
│  │ - 保存設定到檔案                                  │            │
│  └─────────────────────────────────────────────────┘            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. 當前問題分析

### 4.1 問題 1: Sidebar 標題未更新為 "woowtech"

**症狀**: 在 Panel 中設定 brand_name = "woowtech"，但側邊欄仍顯示 "My Smart Home"

**根本原因**:
1. `configuration.yaml` 中設定為 `"My Smart Home"`
2. Panel 只更新記憶體中的設定，未寫入 configuration.yaml
3. 重啟後會從 configuration.yaml 重新載入，覆蓋 Panel 的設定

**解決方案**:
- 需要修改 configuration.yaml 中的設定
- 或使用 "Save to File" 功能保存設定

### 4.2 問題 2: "Failed to save configuration to file"

**症狀**: 點擊保存按鈕時顯示錯誤

**根本原因**:
- 檔案寫入權限問題
- 或 YAML 序列化錯誤

**解決方案**:
- 檢查 `/config/` 目錄寫入權限
- 在 `_write_yaml` 中加入更詳細的錯誤處理

### 4.3 問題 3: Injector 腳本無法取得設定

**症狀**: Injector 可能無法正確載入設定

**根本原因**:
1. `requires_auth = True` 需要認證
2. fetch() 未傳送 credentials

**解決方案**:
```javascript
// 修正前
const response = await fetch(REBRAND_CONFIG_URL);

// 修正後
const response = await fetch(REBRAND_CONFIG_URL, {
  credentials: 'same-origin'  // 傳送認證 cookie
});
```

---

## 5. 設定方式

### 5.1 方式一: configuration.yaml（推薦）

```yaml
# configuration.yaml

frontend:
  extra_module_url:
    - /ha_rebrand/ha-rebrand-injector.js

ha_rebrand:
  brand_name: "woowtech"
  sidebar_title: "woowtech"
  document_title: "woowtech"
  logo: "/local/ha_rebrand/logo.png"
  logo_dark: "/local/ha_rebrand/logo_dark.png"
  favicon: "/local/ha_rebrand/favicon.ico"
  replacements:
    "Home Assistant": "woowtech"
```

### 5.2 方式二: 管理員 Panel

1. 導航到 側邊欄 → Rebrand
2. 填寫品牌資訊
3. 上傳 Logo/Favicon
4. 點擊 "Save to File" 保存
5. 重啟 Home Assistant

---

## 6. API 參考

### 6.1 HTTP Endpoints

| 端點 | 方法 | 認證 | 描述 |
|------|------|------|------|
| `/api/ha_rebrand/config` | GET | 是 | 取得品牌設定 |
| `/api/ha_rebrand/upload` | POST | 是(管理員) | 上傳檔案 |
| `/api/ha_rebrand/save_config` | POST | 是(管理員) | 保存設定到檔案 |

### 6.2 WebSocket Commands

| 命令 | 權限 | 描述 |
|------|------|------|
| `ha_rebrand/get_config` | 任何已認證用戶 | 取得設定 |
| `ha_rebrand/update_config` | 管理員 | 更新設定 |

---

## 7. 安全考量

### 7.1 已實施的安全措施

- [x] HTTP 端點需要認證 (`requires_auth = True`)
- [x] 更新設定需要管理員權限 (`@websocket_api.require_admin`)
- [x] 檔案上傳大小限制 (5MB)
- [x] 檔案類型白名單 (logo, logo_dark, favicon)
- [x] 副檔名白名單 (.png, .jpg, .jpeg, .svg, .ico, .webp)
- [x] 非同步 I/O 避免阻塞事件循環
- [x] Injector 重試次數限制

### 7.2 注意事項

- 設定檔路徑僅限 `/local/` 或外部 URL
- 不支援任意路徑以防止路徑遍歷攻擊

---

## 8. 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.0.0 | 2026-01-29 | 初始版本 |
| 1.4.0 | 2026-01-29 | 安全修正：認證、檔案限制、管理員權限 |
| 1.5.0 | 2026-01-29 | 修正 injector fetch credentials 問題 |

---

## 9. 待辦事項

- [ ] 修正 injector fetch 需要傳送 credentials
- [ ] 改善 "Save to File" 錯誤處理
- [ ] 新增即時預覽功能
- [ ] 支援更多 HA 介面元素的品牌替換
- [ ] 本地化 LitElement 依賴（移除 CDN）
