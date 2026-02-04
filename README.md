# HA Rebrand

A Home Assistant custom component that allows you to customize the branding of your Home Assistant instance.

## Features

- Replace Home Assistant logo with your own (sidebar, loading screen, login page)
- Custom favicon
- Custom sidebar title
- Custom document (browser tab) title
- **Primary color customization** (login page buttons, UI accents)
- **Hide Open Home Foundation logo**
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
3. Go to Settings → Devices & Services → Add Integration → Search "HA Rebrand"

## Configuration

### Option 1: Using the Admin Panel (Recommended)

1. After installation, go to the sidebar and click "Rebrand"
2. Configure your branding using the UI:
   - Upload your logo and favicon
   - Set your brand name and titles
   - Set your primary color (affects buttons and UI accents)
   - Toggle "Hide Open Home Foundation" option
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
  hide_open_home_foundation: true  # Optional: Hide OHF logo
  replacements:
    "Home Assistant": "My Smart Home"
    "HA": "MSH"
```

**Note:** The injector script is automatically loaded - no manual `frontend.extra_module_url` configuration is needed.

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
| `hide_open_home_foundation` | bool | true | Hide the Open Home Foundation logo |
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
3. **Loading Screen**: Patches Home Assistant's IndexView to show custom logo immediately on page load
4. **Login Page**: Custom authorize view replaces the login page logo and applies primary color
5. **Injector Script**: Runs on every page load and:
   - Replaces the favicon
   - Updates the document title
   - Replaces the sidebar logo and title
   - Applies primary color to UI elements
   - Performs text replacements throughout the DOM
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

### Text replacements not working

1. Restart Home Assistant after configuration changes
2. Hard refresh your browser (Ctrl+Shift+R)

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

### 2.1.0
- Automatic injector script loading (no manual frontend configuration needed)
- Loading screen logo replacement (patches IndexView)
- Custom login/authorize page with branding
- Hide Open Home Foundation option
- Improved security validations

### 2.0.0
- Added Config Flow for UI-based setup
- Added dark/light mode logo support
- Added Traditional Chinese translations
- Fixed sidebar logo injection issues
- Improved error handling

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
