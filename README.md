# HA Rebrand Manager

A Home Assistant custom component that allows you to customize the branding of your Home Assistant instance.

## Features

- **Custom Logo** - Replace Home Assistant logo with your own (supports light/dark mode)
- **Custom Favicon** - Change the browser tab icon
- **Custom Titles** - Set sidebar title and browser tab title
- **Text Replacement** - Replace text throughout the interface (e.g., "Home Assistant" → "Your Brand")
- **Config Flow** - Easy setup via Home Assistant UI (Settings → Devices & Services → Add Integration)
- **Admin Panel** - User-friendly configuration panel with drag-and-drop file upload
- **Dark/Light Mode Support** - Header bar automatically adapts to your theme
- **Multi-language** - Supports English and Traditional Chinese

## Screenshots

### Admin Panel
The admin panel provides detailed descriptions for each setting location.

### Sidebar Branding
Your custom logo and brand name appear in the sidebar.

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add this repository URL: `https://github.com/WOOWTECH/Ha_rebrand_manager`
5. Select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Download the `ha_rebrand` folder from this repository
2. Copy it to your `config/custom_components/` directory
3. Restart Home Assistant

## Setup

### Step 1: Add the Integration

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for "HA Rebrand"
4. Click to add

### Step 2: Enable the Injector Script

Add this to your `configuration.yaml`:

```yaml
frontend:
  extra_module_url:
    - /local/ha_rebrand/ha-rebrand-injector.js
```

Then restart Home Assistant.

### Step 3: Configure Your Branding

1. Click "Rebrand" in the sidebar
2. Set your brand name and titles
3. Upload your logo and favicon
4. (Optional) Add text replacements
5. Click "Save Configuration"
6. Restart Home Assistant to apply changes

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `brand_name` | string | "Home Assistant" | The main brand name |
| `sidebar_title` | string | (uses brand_name) | Title shown in sidebar |
| `document_title` | string | (uses brand_name) | Browser tab title |
| `logo` | string | null | Path to logo image |
| `logo_dark` | string | null | Path to dark mode logo (optional) |
| `favicon` | string | null | Path to favicon |
| `replacements` | dict | {} | Text replacement mapping |

## File Paths

Place your custom images in the `/config/www/ha_rebrand/` directory.

Supported image formats:
- PNG, JPG/JPEG, SVG, ICO, WebP

## Where Settings Apply

| Setting | Location |
|---------|----------|
| Brand Name | Settings page title, About page, System info |
| Sidebar Title | Top of the sidebar, replaces "Home Assistant" text |
| Document Title | Browser tab title (e.g., "Overview – Your Brand") |
| Logo | Sidebar logo area |
| Logo (Dark) | Sidebar logo in dark mode |
| Favicon | Browser tab icon |
| Text Replacements | All pages including Shadow DOM content |

## Troubleshooting

### Branding not showing after restart

1. Clear browser cache with `Ctrl+Shift+R`
2. Check if injector is loaded in `configuration.yaml`
3. Verify config.json exists in `/config/www/ha_rebrand/`

### Logo not appearing

1. Check file exists in `/config/www/ha_rebrand/`
2. Verify file permissions
3. Check browser console for errors

### Admin panel not appearing

1. Ensure integration is added via Settings → Devices & Services
2. Check Home Assistant logs for errors
3. Verify you have admin privileges

## Version History

### 2.0.0
- Add Config Flow for UI-based integration setup
- Add dark/light mode support for header bar
- Add detailed Chinese descriptions for each setting
- Fix sidebar logo injection for newer HA versions
- Fix Shadow DOM traversal for sidebar title replacement
- Improve error handling for file uploads

### 1.0.0
- Initial release
- Logo, favicon, and title customization
- Text replacement mapping
- Admin panel with file upload
- Dark mode logo support

## License

MIT License

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/WOOWTECH/Ha_rebrand_manager/issues).
