# HA Rebrand

一个 Home Assistant 自定义组件，让您可以自定义 Home Assistant 实例的品牌外观。

## 功能特性

- 用自定义 Logo 替换 Home Assistant 默认标志
- 自定义网站图标 (Favicon)
- 自定义侧边栏标题
- 自定义浏览器标签页标题
- 文字替换映射（例如："Home Assistant" → "我的智能家居"）
- 深色模式 Logo 支持
- 管理面板支持拖放上传文件

## 安装方法

### HACS 安装（推荐）

1. 在 Home Assistant 中打开 HACS
2. 点击"集成"
3. 点击右上角的三个点，选择"自定义存储库"
4. 添加本仓库 URL，类别选择"Integration"
5. 点击"安装"
6. 重启 Home Assistant

### 手动安装

1. 将本仓库复制到您的 `custom_components/ha_rebrand` 目录
2. 重启 Home Assistant

## 配置方法

### 方式一：使用管理面板（推荐）

1. 安装完成后，在侧边栏点击"Rebrand"
2. 使用界面配置您的品牌：
   - 上传您的 Logo 和网站图标
   - 设置品牌名称和标题
   - 添加文字替换规则
3. 点击"应用更改"测试配置
4. 点击"保存到文件"创建永久配置

### 方式二：手动 YAML 配置

在 `configuration.yaml` 中添加以下内容：

```yaml
ha_rebrand:
  brand_name: "我的智能家居"
  logo: "/local/my-logo.svg"
  logo_dark: "/local/my-logo-dark.svg"  # 可选
  favicon: "/local/favicon.ico"
  sidebar_title: "我的智能家居"
  document_title: "我的智能家居"
  replacements:
    "Home Assistant": "我的智能家居"
    "HA": "智家"
```

### 启用注入脚本

要在整个界面启用自动品牌替换，需要将注入脚本添加到 Lovelace 配置中。

在 `configuration.yaml` 中添加：

```yaml
frontend:
  extra_module_url:
    - /local/ha_rebrand/ha-rebrand-injector.js
```

然后重启 Home Assistant。

## 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `brand_name` | 字符串 | "Home Assistant" | 主品牌名称 |
| `logo` | 字符串 | null | Logo 图片路径（支持 `/local/` 路径和 URL） |
| `logo_dark` | 字符串 | null | 深色模式 Logo 路径（可选） |
| `favicon` | 字符串 | null | 网站图标路径 |
| `sidebar_title` | 字符串 | brand_name | 侧边栏显示的标题 |
| `document_title` | 字符串 | brand_name | 浏览器标签页标题 |
| `replacements` | 字典 | {} | 文字替换映射 |

## 文件路径说明

将自定义图片放在 `/config/www/` 目录中，它们可以通过 `/local/` URL 访问。

示例：
- 文件位置：`/config/www/my-logo.svg`
- 配置写法：`logo: "/local/my-logo.svg"`

支持的图片格式：
- PNG
- JPG/JPEG
- SVG
- ICO（用于网站图标）
- WebP

## 设置显示位置对照表

| 设置项 | 显示位置 |
|--------|----------|
| `brand_name` | 设置页面标题、关于页面、系统信息 |
| `sidebar_title` | 侧边栏顶部标题区域 |
| `document_title` | 浏览器标签页标题（例如：「总览 – 品牌名称」） |
| `logo` | 侧边栏顶部 Logo 区域 |
| `logo_dark` | 深色模式下的侧边栏 Logo |
| `favicon` | 浏览器标签页图标 |
| `replacements` | 整个界面中匹配的文字 |

## 工作原理

1. **后端组件**：管理配置、文件上传，并提供 WebSocket/HTTP API
2. **管理面板**：提供用户友好的界面来配置品牌
3. **注入脚本**：在每次页面加载时运行，执行以下操作：
   - 替换网站图标
   - 更新文档标题
   - 替换侧边栏 Logo 和标题
   - 在整个 DOM 中执行文字替换
   - 监控动态内容变化

## 常见问题排查

### Logo 不显示

1. 确保文件存在于 `/config/www/` 目录
2. 清除浏览器缓存
3. 检查浏览器控制台是否有错误

### 文字替换不生效

1. 确保注入脚本已加载（检查 `frontend.extra_module_url`）
2. 配置更改后重启 Home Assistant
3. 强制刷新浏览器（Ctrl+Shift+R）

### 管理面板不显示

1. 检查日志中组件是否成功加载
2. 确保您具有管理员权限
3. 重启 Home Assistant

## 限制说明

- HA 核心 UI 中某些深层嵌套的元素可能无法被替换
- 文字替换仅作用于可见文本，不影响元素属性
- 配置更改需要刷新页面才能生效

## 版本历史

### 2.0.0
- 添加 Config Flow 支持 UI 配置
- 添加深色/浅色模式支持
- 添加中文翻译
- 修复侧边栏 Logo 注入问题
- 改进错误处理

### 1.0.0
- 初始版本
- Logo、网站图标和标题自定义
- 文字替换映射
- 管理面板支持文件上传
- 深色模式 Logo 支持

## 许可证

MIT License

## 支持

如有问题或功能建议，请使用 GitHub Issue 追踪器。
