/**
 * HA Rebrand Panel
 *
 * Admin panel for managing custom branding in Home Assistant
 */

import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

class HaRebrandPanel extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      narrow: { type: Boolean },
      panel: { type: Object },
      _config: { type: Object },
      _loading: { type: Boolean },
      _saving: { type: Boolean },
      _uploadingLogo: { type: Boolean },
      _uploadingLogoDark: { type: Boolean },
      _uploadingFavicon: { type: Boolean },
      _message: { type: Object },
      _newReplaceKey: { type: String },
      _newReplaceValue: { type: String },
    };
  }

  static get styles() {
    return css`
      :host {
        display: block;
        padding: 16px;
        background: var(--primary-background-color);
        min-height: 100vh;
        box-sizing: border-box;
      }

      .top-bar {
        display: flex;
        align-items: center;
        height: 56px;
        padding: 0 16px;
        background: var(--app-header-background-color, var(--primary-background-color));
        color: var(--app-header-text-color, var(--primary-text-color));
        border-bottom: 1px solid var(--divider-color);
        position: sticky;
        top: 0;
        z-index: 100;
        gap: 12px;
        margin: -16px -16px 16px -16px;
      }

      .top-bar-sidebar-btn {
        width: 40px;
        height: 40px;
        border: none;
        background: transparent;
        color: inherit;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background 0.2s;
        flex-shrink: 0;
      }

      .top-bar-sidebar-btn:hover {
        background: var(--secondary-background-color);
      }

      .top-bar-sidebar-btn svg {
        width: 24px;
        height: 24px;
      }

      .top-bar-title {
        flex: 1;
        font-size: 20px;
        font-weight: 500;
        margin: 0;
      }

      .content {
        max-width: 800px;
        margin: 0 auto;
      }

      .card {
        background: var(--card-background-color);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: var(--ha-card-box-shadow, 0 2px 4px rgba(0,0,0,0.1));
      }

      .card-title {
        font-size: 18px;
        font-weight: 500;
        color: var(--primary-text-color);
        margin: 0 0 16px 0;
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .card-title svg {
        width: 24px;
        height: 24px;
        color: var(--primary-color);
      }

      .form-group {
        margin-bottom: 20px;
      }

      .form-group:last-child {
        margin-bottom: 0;
      }

      .form-group label {
        display: block;
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .form-group .hint {
        font-size: 12px;
        color: var(--secondary-text-color);
        margin-top: 4px;
      }

      .form-group input[type="text"] {
        width: 100%;
        padding: 12px;
        border: 1px solid var(--divider-color);
        border-radius: 8px;
        font-size: 14px;
        background: var(--primary-background-color);
        color: var(--primary-text-color);
        box-sizing: border-box;
      }

      .form-group input[type="text"]:focus {
        outline: none;
        border-color: var(--primary-color);
      }

      .upload-area {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px;
        border: 2px dashed var(--divider-color);
        border-radius: 8px;
        background: var(--primary-background-color);
        transition: all 0.2s;
      }

      .upload-area:hover {
        border-color: var(--primary-color);
        background: var(--secondary-background-color);
      }

      .upload-area.dragover {
        border-color: var(--primary-color);
        background: rgba(var(--rgb-primary-color, 3, 169, 244), 0.1);
      }

      .preview-image {
        width: 80px;
        height: 80px;
        object-fit: contain;
        background: var(--card-background-color);
        border-radius: 8px;
        border: 1px solid var(--divider-color);
      }

      .preview-placeholder {
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--card-background-color);
        border-radius: 8px;
        border: 1px solid var(--divider-color);
        color: var(--secondary-text-color);
      }

      .preview-placeholder svg {
        width: 32px;
        height: 32px;
      }

      .upload-info {
        flex: 1;
      }

      .upload-info p {
        margin: 0 0 8px 0;
        color: var(--secondary-text-color);
        font-size: 14px;
      }

      .upload-actions {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }

      .btn {
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
      }

      .btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }

      .btn-primary {
        background: var(--primary-color);
        color: white;
      }

      .btn-primary:hover:not(:disabled) {
        opacity: 0.9;
      }

      .btn-secondary {
        background: var(--secondary-background-color);
        color: var(--primary-text-color);
      }

      .btn-secondary:hover:not(:disabled) {
        background: var(--divider-color);
      }

      .btn-danger {
        background: var(--error-color, #db4437);
        color: white;
      }

      .btn-danger:hover:not(:disabled) {
        opacity: 0.9;
      }

      .btn-small {
        padding: 6px 12px;
        font-size: 12px;
      }

      input[type="file"] {
        display: none;
      }

      .replacements-list {
        border: 1px solid var(--divider-color);
        border-radius: 8px;
        overflow: hidden;
      }

      .replacement-item {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        border-bottom: 1px solid var(--divider-color);
        gap: 12px;
      }

      .replacement-item:last-child {
        border-bottom: none;
      }

      .replacement-item .key {
        flex: 1;
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .replacement-item .arrow {
        color: var(--secondary-text-color);
      }

      .replacement-item .value {
        flex: 1;
        color: var(--secondary-text-color);
      }

      .replacement-item .delete-btn {
        padding: 4px;
        border: none;
        background: none;
        color: var(--secondary-text-color);
        cursor: pointer;
        border-radius: 4px;
      }

      .replacement-item .delete-btn:hover {
        background: var(--error-color);
        color: white;
      }

      .add-replacement {
        display: flex;
        gap: 8px;
        padding: 12px 16px;
        background: var(--secondary-background-color);
        align-items: center;
      }

      .add-replacement input {
        flex: 1;
        padding: 8px 12px;
        border: 1px solid var(--divider-color);
        border-radius: 6px;
        font-size: 14px;
        background: var(--card-background-color);
        color: var(--primary-text-color);
      }

      .add-replacement input:focus {
        outline: none;
        border-color: var(--primary-color);
      }

      .message {
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
      }

      .message.success {
        background: rgba(76, 175, 80, 0.1);
        color: #4caf50;
        border: 1px solid rgba(76, 175, 80, 0.3);
      }

      .message.error {
        background: rgba(244, 67, 54, 0.1);
        color: #f44336;
        border: 1px solid rgba(244, 67, 54, 0.3);
      }

      .message.info {
        background: rgba(33, 150, 243, 0.1);
        color: #2196f3;
        border: 1px solid rgba(33, 150, 243, 0.3);
      }

      .actions-bar {
        display: flex;
        gap: 12px;
        justify-content: flex-end;
        padding-top: 16px;
        border-top: 1px solid var(--divider-color);
        margin-top: 24px;
      }

      .loading {
        display: flex;
        justify-content: center;
        padding: 48px;
      }

      .spinner {
        width: 40px;
        height: 40px;
        border: 3px solid var(--divider-color);
        border-top-color: var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }

      @keyframes spin {
        to { transform: rotate(360deg); }
      }

      .current-path {
        font-size: 12px;
        color: var(--secondary-text-color);
        word-break: break-all;
        margin-top: 4px;
      }

      .toggle-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid var(--divider-color);
      }

      .toggle-row:last-child {
        border-bottom: none;
      }

      .toggle-label {
        flex: 1;
      }

      .toggle-label .title {
        font-weight: 500;
        color: var(--primary-text-color);
        margin-bottom: 4px;
      }

      .toggle-label .description {
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      .toggle-switch {
        position: relative;
        width: 48px;
        height: 24px;
        flex-shrink: 0;
      }

      .toggle-switch input {
        opacity: 0;
        width: 0;
        height: 0;
      }

      .toggle-slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: var(--divider-color);
        transition: 0.3s;
        border-radius: 24px;
      }

      .toggle-slider:before {
        position: absolute;
        content: "";
        height: 18px;
        width: 18px;
        left: 3px;
        bottom: 3px;
        background-color: white;
        transition: 0.3s;
        border-radius: 50%;
      }

      .toggle-switch input:checked + .toggle-slider {
        background-color: var(--primary-color);
      }

      .toggle-switch input:checked + .toggle-slider:before {
        transform: translateX(24px);
      }
    `;
  }

  constructor() {
    super();
    this._config = {
      brand_name: "",
      logo: "",
      logo_dark: "",
      favicon: "",
      sidebar_title: "",
      document_title: "",
      replacements: {},
      hide_open_home_foundation: true,
    };
    this._loading = true;
    this._saving = false;
    this._uploadingLogo = false;
    this._uploadingLogoDark = false;
    this._uploadingFavicon = false;
    this._message = null;
    this._newReplaceKey = "";
    this._newReplaceValue = "";
  }

  _toggleSidebar() {
    this.dispatchEvent(new CustomEvent("hass-toggle-menu", { bubbles: true, composed: true }));
  }

  async firstUpdated() {
    await this._loadConfig();
  }

  async _loadConfig() {
    this._loading = true;
    try {
      const result = await this.hass.callWS({
        type: "ha_rebrand/get_config",
      });
      this._config = {
        brand_name: result.brand_name || "",
        logo: result.logo || "",
        logo_dark: result.logo_dark || "",
        favicon: result.favicon || "",
        sidebar_title: result.sidebar_title || "",
        document_title: result.document_title || "",
        replacements: result.replacements || {},
        hide_open_home_foundation: result.hide_open_home_foundation !== false,
      };
    } catch (error) {
      console.error("Failed to load config:", error);
      this._showMessage("error", "Failed to load configuration");
    }
    this._loading = false;
  }

  // Helper to strip cache buster query params from paths
  _stripCacheBuster(path) {
    if (!path) return path;
    return path.split('?')[0];
  }

  async _saveToFile() {
    this._saving = true;
    try {
      // Prepare config without cache busters for saving
      const configToSave = {
        ...this._config,
        logo: this._stripCacheBuster(this._config.logo),
        logo_dark: this._stripCacheBuster(this._config.logo_dark),
        favicon: this._stripCacheBuster(this._config.favicon),
      };

      // First, update config in memory and write config.json via WebSocket
      await this.hass.callWS({
        type: "ha_rebrand/update_config",
        ...configToSave,
      });

      // Then save to YAML file for persistence across restarts
      const response = await fetch("/api/ha_rebrand/save_config", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.hass.auth.data.access_token}`,
          "Content-Type": "application/json",
        },
      });
      const result = await response.json();

      if (result.success) {
        // Trigger rebrand refresh if available
        if (window.HARebrand) {
          await window.HARebrand.reloadConfig();
        }
        this._showMessage("success", "Configuration saved! Refresh the page to see changes.");
      } else {
        throw new Error(result.error || "Failed to save");
      }
    } catch (error) {
      console.error("Failed to save configuration:", error);
      this._showMessage("error", "Failed to save configuration: " + error.message);
    }
    this._saving = false;
  }

  async _uploadFile(type, file) {
    const uploadingKey = `_uploading${type.charAt(0).toUpperCase() + type.slice(1).replace('_', '')}`;
    this[uploadingKey] = true;

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("type", type);

      const response = await fetch("/api/ha_rebrand/upload", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.hass.auth.data.access_token}`,
        },
        body: formData,
      });

      // Check HTTP status first
      if (!response.ok) {
        let errorMsg = `HTTP ${response.status}`;
        try {
          const errorResult = await response.json();
          errorMsg = errorResult.error || errorMsg;
        } catch (e) {
          // Response is not JSON, use status text
          errorMsg = response.statusText || errorMsg;
        }
        throw new Error(errorMsg);
      }

      const result = await response.json();

      if (result.success) {
        // Update config with new path (add cache buster for preview)
        const configKey = type === "logo_dark" ? "logo_dark" : type;
        const cacheBuster = `?t=${Date.now()}`;
        this._config = { ...this._config, [configKey]: result.path + cacheBuster };
        this._showMessage("success", `${type} 上傳成功！`);
      } else {
        throw new Error(result.error || "上傳失敗");
      }
    } catch (error) {
      console.error("Upload failed:", error);
      this._showMessage("error", `${type} 上傳失敗: ${error.message}`);
    }

    this[uploadingKey] = false;
  }

  _handleFileSelect(type, event) {
    const file = event.target.files[0];
    if (file) {
      this._uploadFile(type, file);
    }
  }

  _handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add("dragover");
  }

  _handleDragLeave(event) {
    event.currentTarget.classList.remove("dragover");
  }

  _handleDrop(type, event) {
    event.preventDefault();
    event.currentTarget.classList.remove("dragover");

    const file = event.dataTransfer.files[0];
    if (file) {
      this._uploadFile(type, file);
    }
  }

  _clearImage(type) {
    this._config = { ...this._config, [type]: "" };
  }

  _updateConfig(field, value) {
    this._config = { ...this._config, [field]: value };
  }

  _addReplacement() {
    if (!this._newReplaceKey.trim() || !this._newReplaceValue.trim()) return;

    const replacements = { ...this._config.replacements };
    replacements[this._newReplaceKey.trim()] = this._newReplaceValue.trim();

    this._config = { ...this._config, replacements };
    this._newReplaceKey = "";
    this._newReplaceValue = "";
  }

  _removeReplacement(key) {
    const replacements = { ...this._config.replacements };
    delete replacements[key];
    this._config = { ...this._config, replacements };
  }

  _showMessage(type, text) {
    this._message = { type, text };
    setTimeout(() => {
      this._message = null;
    }, 5000);
  }

  render() {
    if (this._loading) {
      return html`
        <div class="top-bar">
          <button class="top-bar-sidebar-btn" @click=${this._toggleSidebar}>
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"/></svg>
          </button>
          <h1 class="top-bar-title">HA Rebrand</h1>
        </div>
        <div class="loading">
          <div class="spinner"></div>
        </div>
      `;
    }

    return html`
      <div class="top-bar">
        <button class="top-bar-sidebar-btn" @click=${this._toggleSidebar}>
          <svg viewBox="0 0 24 24"><path fill="currentColor" d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"/></svg>
        </button>
        <h1 class="top-bar-title">HA Rebrand</h1>
      </div>

      <div class="content">
        ${this._message ? html`
          <div class="message ${this._message.type}">
            ${this._message.text}
          </div>
        ` : ""}

        <!-- Brand Name Card -->
        <div class="card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M5,4V7H10.5V19H13.5V7H19V4H5Z"/></svg>
            Brand Name & Titles
          </h2>

          <div class="form-group">
            <label>Brand Name</label>
            <input
              type="text"
              .value=${this._config.brand_name}
              @input=${(e) => this._updateConfig("brand_name", e.target.value)}
              placeholder="My Smart Home"
            />
            <p class="hint"><strong>顯示位置：</strong>設定頁面標題、關於頁面、系統資訊中的品牌名稱</p>
          </div>

          <div class="form-group">
            <label>Sidebar Title</label>
            <input
              type="text"
              .value=${this._config.sidebar_title}
              @input=${(e) => this._updateConfig("sidebar_title", e.target.value)}
              placeholder="My Smart Home"
            />
            <p class="hint"><strong>顯示位置：</strong>側邊欄頂部標題區域，取代原本的「Home Assistant」文字</p>
          </div>

          <div class="form-group">
            <label>Document Title</label>
            <input
              type="text"
              .value=${this._config.document_title}
              @input=${(e) => this._updateConfig("document_title", e.target.value)}
              placeholder="My Smart Home"
            />
            <p class="hint"><strong>顯示位置：</strong>瀏覽器標籤頁標題（例如：「總覽 – 品牌名稱」）</p>
          </div>
        </div>

        <!-- Logo Card -->
        <div class="card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M21,3H3C2,3 1,4 1,5V19A2,2 0 0,0 3,21H21C22,21 23,20 23,19V5C23,4 22,3 21,3M5,17L8.5,12.5L11,15.5L14.5,11L19,17H5Z"/></svg>
            Logo
          </h2>

          <div class="form-group">
            <label>Logo (Light Mode)</label>
            <p class="hint" style="margin-bottom: 8px;"><strong>顯示位置：</strong>側邊欄頂部 Logo 區域，取代原本的 Home Assistant Logo</p>
            <div
              class="upload-area"
              @dragover=${this._handleDragOver}
              @dragleave=${this._handleDragLeave}
              @drop=${(e) => this._handleDrop("logo", e)}
            >
              ${this._config.logo ? html`
                <img class="preview-image" src="${this._config.logo}" alt="Logo preview" />
              ` : html`
                <div class="preview-placeholder">
                  <svg viewBox="0 0 24 24"><path fill="currentColor" d="M21,3H3C2,3 1,4 1,5V19A2,2 0 0,0 3,21H21C22,21 23,20 23,19V5C23,4 22,3 21,3M5,17L8.5,12.5L11,15.5L14.5,11L19,17H5Z"/></svg>
                </div>
              `}
              <div class="upload-info">
                <p>Drag & drop an image here or click to upload</p>
                <div class="upload-actions">
                  <label class="btn btn-primary btn-small">
                    ${this._uploadingLogo ? "Uploading..." : "Choose File"}
                    <input
                      type="file"
                      accept="image/*"
                      @change=${(e) => this._handleFileSelect("logo", e)}
                      ?disabled=${this._uploadingLogo}
                    />
                  </label>
                  ${this._config.logo ? html`
                    <button class="btn btn-danger btn-small" @click=${() => this._clearImage("logo")}>
                      Remove
                    </button>
                  ` : ""}
                </div>
                ${this._config.logo ? html`
                  <p class="current-path">Current: ${this._config.logo}</p>
                ` : ""}
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>Logo (Dark Mode) - Optional</label>
            <p class="hint" style="margin-bottom: 8px;"><strong>顯示位置：</strong>深色模式下的側邊欄 Logo，若未設定則使用淺色模式 Logo</p>
            <div
              class="upload-area"
              @dragover=${this._handleDragOver}
              @dragleave=${this._handleDragLeave}
              @drop=${(e) => this._handleDrop("logo_dark", e)}
            >
              ${this._config.logo_dark ? html`
                <img class="preview-image" src="${this._config.logo_dark}" alt="Dark logo preview" style="background: #333;" />
              ` : html`
                <div class="preview-placeholder" style="background: #333;">
                  <svg viewBox="0 0 24 24"><path fill="currentColor" d="M21,3H3C2,3 1,4 1,5V19A2,2 0 0,0 3,21H21C22,21 23,20 23,19V5C23,4 22,3 21,3M5,17L8.5,12.5L11,15.5L14.5,11L19,17H5Z"/></svg>
                </div>
              `}
              <div class="upload-info">
                <p>深色模式專用 Logo（可選）</p>
                <div class="upload-actions">
                  <label class="btn btn-primary btn-small">
                    ${this._uploadingLogoDark ? "Uploading..." : "Choose File"}
                    <input
                      type="file"
                      accept="image/*"
                      @change=${(e) => this._handleFileSelect("logo_dark", e)}
                      ?disabled=${this._uploadingLogoDark}
                    />
                  </label>
                  ${this._config.logo_dark ? html`
                    <button class="btn btn-danger btn-small" @click=${() => this._clearImage("logo_dark")}>
                      Remove
                    </button>
                  ` : ""}
                </div>
                ${this._config.logo_dark ? html`
                  <p class="current-path">Current: ${this._config.logo_dark}</p>
                ` : ""}
              </div>
            </div>
          </div>
        </div>

        <!-- Advanced Settings Card -->
        <div class="card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/></svg>
            Advanced Settings
          </h2>

          <div class="toggle-row">
            <div class="toggle-label">
              <div class="title">Hide Open Home Foundation</div>
              <div class="description">隱藏載入畫面底部的「Open Home Foundation」標誌</div>
            </div>
            <label class="toggle-switch">
              <input
                type="checkbox"
                .checked=${this._config.hide_open_home_foundation}
                @change=${(e) => this._updateConfig("hide_open_home_foundation", e.target.checked)}
              />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>

        <!-- Favicon Card -->
        <div class="card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8Z"/></svg>
            Favicon
          </h2>

          <div class="form-group">
            <label>Favicon</label>
            <p class="hint" style="margin-bottom: 8px;"><strong>顯示位置：</strong>瀏覽器標籤頁圖示（建議尺寸：32x32 或 64x64 像素）</p>
            <div
              class="upload-area"
              @dragover=${this._handleDragOver}
              @dragleave=${this._handleDragLeave}
              @drop=${(e) => this._handleDrop("favicon", e)}
            >
              ${this._config.favicon ? html`
                <img class="preview-image" src="${this._config.favicon}" alt="Favicon preview" style="width: 48px; height: 48px;" />
              ` : html`
                <div class="preview-placeholder" style="width: 48px; height: 48px;">
                  <svg viewBox="0 0 24 24" style="width: 24px; height: 24px;"><path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/></svg>
                </div>
              `}
              <div class="upload-info">
                <p>支援格式：.ico, .png, .svg</p>
                <div class="upload-actions">
                  <label class="btn btn-primary btn-small">
                    ${this._uploadingFavicon ? "Uploading..." : "Choose File"}
                    <input
                      type="file"
                      accept=".ico,.png,.svg"
                      @change=${(e) => this._handleFileSelect("favicon", e)}
                      ?disabled=${this._uploadingFavicon}
                    />
                  </label>
                  ${this._config.favicon ? html`
                    <button class="btn btn-danger btn-small" @click=${() => this._clearImage("favicon")}>
                      Remove
                    </button>
                  ` : ""}
                </div>
                ${this._config.favicon ? html`
                  <p class="current-path">Current: ${this._config.favicon}</p>
                ` : ""}
              </div>
            </div>
          </div>
        </div>

        <!-- Text Replacements Card -->
        <div class="card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M12.87,15.07L10.33,12.56L10.36,12.53C12.1,10.59 13.34,8.36 14.07,6H17V4H10V2H8V4H1V6H12.17C11.5,7.92 10.44,9.75 9,11.35C8.07,10.32 7.3,9.19 6.69,8H4.69C5.42,9.63 6.42,11.17 7.67,12.56L2.58,17.58L4,19L9,14L12.11,17.11L12.87,15.07M18.5,10H16.5L12,22H14L15.12,19H19.87L21,22H23L18.5,10M15.88,17L17.5,12.67L19.12,17H15.88Z"/></svg>
            Text Replacements
          </h2>

          <p class="hint" style="margin-bottom: 16px;">
            <strong>功能說明：</strong>在整個 Home Assistant 介面中搜尋並替換指定文字。<br>
            <strong>常見用途：</strong>將「Home Assistant」替換為您的品牌名稱。<br>
            <strong>注意事項：</strong>文字替換會套用到所有頁面，包括 Shadow DOM 內的內容。
          </p>

          <div class="replacements-list">
            ${Object.entries(this._config.replacements).map(([key, value]) => html`
              <div class="replacement-item">
                <span class="key">${key}</span>
                <span class="arrow">→</span>
                <span class="value">${value}</span>
                <button class="delete-btn" @click=${() => this._removeReplacement(key)}>
                  <svg viewBox="0 0 24 24" style="width: 18px; height: 18px;"><path fill="currentColor" d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"/></svg>
                </button>
              </div>
            `)}

            <div class="add-replacement">
              <input
                type="text"
                placeholder="Search text (e.g., Home Assistant)"
                .value=${this._newReplaceKey}
                @input=${(e) => this._newReplaceKey = e.target.value}
                @keydown=${(e) => e.key === "Enter" && this._addReplacement()}
              />
              <span style="color: var(--secondary-text-color);">→</span>
              <input
                type="text"
                placeholder="Replace with"
                .value=${this._newReplaceValue}
                @input=${(e) => this._newReplaceValue = e.target.value}
                @keydown=${(e) => e.key === "Enter" && this._addReplacement()}
              />
              <button class="btn btn-primary btn-small" @click=${this._addReplacement}>
                Add
              </button>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="card">
          <div class="actions-bar" style="border-top: none; margin-top: 0; padding-top: 0;">
            <button class="btn btn-primary" @click=${this._saveToFile} ?disabled=${this._saving}>
              ${this._saving ? "Saving..." : "Save Configuration"}
            </button>
          </div>
          <p class="hint" style="text-align: center; margin-top: 12px;">
            Saves configuration to ha_rebrand.yaml.<br>
            Restart Home Assistant to apply changes.
          </p>
        </div>
      </div>
    `;
  }
}

customElements.define("ha-rebrand-panel", HaRebrandPanel);
