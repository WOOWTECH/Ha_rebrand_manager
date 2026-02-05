# HA Rebrand

A Home Assistant custom component that allows you to customize the branding of your Home Assistant instance.

## Features

- Replace Home Assistant logo with your own (sidebar, loading screen, login page, onboarding page)
- Custom favicon
- Custom sidebar title
- Custom document (browser tab) title
- **Primary color customization** (login page buttons, particles animation, UI accents)
- **Hide Open Home Foundation logo**
- Dark mode logo support
- Admin panel with drag-and-drop file upload
- **Security hardened** (XSS and CSS injection prevention)
- **Performance optimized** (pre-compiled regex, smart MutationObserver)

## Installation

### HACS (Recommended)

> **Prerequisites:** [HACS](https://hacs.xyz/) must be installed in your Home Assistant instance.

#### Step 1: Add Custom Repository

1. Open your Home Assistant web interface
2. Click on **HACS** in the sidebar
3. Click on **Integrations** tab
4. Click the **three dots menu (⋮)** in the top right corner
5. Select **Custom repositories**

#### Step 2: Enter Repository Information

1. In the **Repository** field, paste:
   ```
   https://github.com/WOOWTECH/Ha_rebrand_manager
   ```
2. In the **Category** dropdown, select **Integration**
3. Click **Add**
4. Close the dialog

#### Step 3: Download the Integration

1. Click **+ Explore & Download Repositories** button (bottom right)
2. Search for **HA Rebrand**
3. Click on it to open the details
4. Click **Download** button
5. Confirm the download in the popup

#### Step 4: Restart and Configure

1. Go to **Settings** → **System** → **Restart**
2. Wait for Home Assistant to fully restart
3. Go to **Settings** → **Devices & Services**
4. Click **+ Add Integration** (bottom right)
5. Search for **HA Rebrand** and select it
6. Complete the setup wizard

After installation, click **Rebrand** in the sidebar to configure your branding.

### Manual Installation

1. Download this repository
2. Copy the `custom_components/ha_rebrand` folder to your Home Assistant's `config/custom_components/` directory
3. Restart Home Assistant
4. Go to Settings → Devices & Services → Add Integration → Search "HA Rebrand"

## Configuration

### Option 1: Using the Admin Panel (Recommended)

1. After installation, go to the sidebar and click "Rebrand"
2. Configure your branding using the UI:
   - Upload your logo and favicon
   - Set your brand name and titles
   - Set your primary color (affects buttons and UI accents)
   - Toggle "Hide Open Home Foundation" option
3. Click "Apply Changes" to test your configuration
4. Click "Save to File" to create a permanent configuration

### Option 2: YAML Configuration File

When you click "Save to File" in the Admin Panel, a `ha_rebrand.yaml` file is created in your config directory. This file persists your settings and is loaded on startup.

You can also manually create or edit this file:

```yaml
# /config/ha_rebrand.yaml
system_name: "My Smart Home"
logo: "/local/my-logo.svg"
logo_dark: "/local/my-logo-dark.svg"  # Optional
favicon: "/local/favicon.ico"
sidebar_text: "My Smart Home"
browser_tab_title: "My Smart Home"
primary_color: "#6183fc"  # Optional: Custom primary color
hide_open_home_foundation: true  # Optional: Hide OHF logo
```

**Note:**
- The Admin Panel stores runtime configuration in `www/ha_rebrand/config.json`
- The injector script is automatically loaded - no manual `frontend.extra_module_url` configuration is needed

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `system_name` | string | "Home Assistant" | The name used for accessibility and system references |
| `logo` | string | null | Path to logo image (supports `/local/` paths and URLs) |
| `logo_dark` | string | null | Path to dark mode logo (optional) |
| `favicon` | string | null | Path to favicon |
| `sidebar_text` | string | system_name | The text displayed at the top of the sidebar |
| `browser_tab_title` | string | system_name | The name shown in browser tabs |
| `primary_color` | string | null | Primary color for buttons and UI (hex format: `#RGB`, `#RRGGBB`, or `#RRGGBBAA`) |
| `hide_open_home_foundation` | bool | true | Hide the Open Home Foundation logo |

## File Paths

**Admin Panel uploads:** Files uploaded via the Admin Panel are stored in `/config/www/ha_rebrand/` and accessible via `/local/ha_rebrand/` URLs.

**Manual placement:** You can also place custom images in `/config/www/` directly. They will be accessible via `/local/` URLs.

Example:
- Admin Panel upload: `/config/www/ha_rebrand/logo.png` → `/local/ha_rebrand/logo.png`
- Manual placement: `/config/www/my-logo.svg` → `/local/my-logo.svg`

Supported image formats (max 5MB):
- PNG
- JPG/JPEG
- SVG
- ICO (for favicon)
- WebP

## How It Works

1. **Backend Component**: Manages configuration, file uploads, and provides WebSocket/HTTP APIs
2. **Admin Panel**: Provides a user-friendly interface to configure branding
3. **Loading Screen**: Patches Home Assistant's IndexView to show custom logo immediately on page load
4. **Login Page**: Custom authorize view replaces the login page logo and applies primary color (including particles animation)
5. **Onboarding Page**: Custom onboarding view applies branding during initial setup
6. **Injector Script**: Runs on every page load and:
   - Replaces the favicon
   - Updates the document title
   - Replaces the sidebar logo and title
   - Applies primary color to UI elements
   - Replaces logos in dialogs and QR codes
   - Monitors for dynamic content changes with optimized MutationObserver

## Security

This component includes security measures to prevent XSS and CSS injection attacks:
- All user-provided values are properly escaped before HTML/JavaScript injection
- Color values are validated against a strict regex pattern
- JavaScript strings are escaped to prevent script injection
- File uploads are validated for type, extension, and size (max 5MB)

## Troubleshooting

### Logo not showing

1. Make sure the file exists in `/config/www/`
2. Clear your browser cache
3. Check browser console for errors

### Primary color not applying

1. Use hex color format only (e.g., `#6183fc`)
2. Test in an incognito/private browser window to avoid cache issues
3. The primary color affects login page buttons and main UI accent colors

### Admin panel not appearing

1. Check if the component loaded successfully in the logs
2. Ensure you have admin privileges
3. Restart Home Assistant

### Remote access not working (stuck on "Loading data")

If you're using a reverse proxy (Nginx Proxy Manager, Cloudflare Tunnel, etc.) and remote access fails while local access works:

**1. Configure `trusted_proxies` in Home Assistant**

Add the following to your `configuration.yaml`:

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.30.32.0/23   # Supervisor network (Core + Add-ons)
    - 127.0.0.1        # Localhost
    - ::1              # IPv6 localhost
```

**Why `172.30.32.0/23`?** This CIDR covers both:
- `172.30.32.0/24` - Home Assistant Core services
- `172.30.33.0/24` - Add-ons (including Nginx Proxy Manager, Cloudflared)

**2. Configure Nginx Proxy Manager**

1. Open NPM Admin Panel (`http://<ha-ip>:81`)
2. Edit your proxy host for Home Assistant
3. In **Details** tab: Enable **WebSockets Support**
4. In **Advanced** tab: **Delete ALL custom nginx configuration** (NPM handles WebSocket automatically)
5. Save

**3. If you see "Congratulations" page instead of Home Assistant**

This means NPM cannot resolve the hostname. Change the Forward Hostname:
1. Edit proxy host in NPM
2. Change **Forward Hostname / IP** from `homeassistant` to `172.30.32.1`
3. Keep **Forward Port** as `8123`
4. Save

**4. Verify ha_rebrand is not the cause**

Temporarily disable ha_rebrand to test:
- Go to Settings → Devices & Services → HA Rebrand → Disable
- Restart Home Assistant and test remote access
- If it works after disabling, please report the issue on GitHub

For detailed technical explanation, see [Proxy_Issue_Solution_Plan.md](Proxy_Issue_Solution_Plan.md).

## Limitations

- Some deeply nested elements in the HA core UI may not be replaced
- Changes to configuration require a page refresh to take effect
- Primary color only supports hex format (`#RGB`, `#RRGGBB`, or `#RRGGBBAA`)
- If you switch between Light/Dark mode, you need to refresh the page to see the updated logo

## License

MIT License

## Support

For issues and feature requests, please use the GitHub issue tracker.
