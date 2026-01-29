# HA Rebrand

A Home Assistant custom component that allows you to customize the branding of your Home Assistant instance.

## Features

- Replace Home Assistant logo with your own
- Custom favicon
- Custom sidebar title
- Custom document (browser tab) title
- Text replacement mapping (e.g., "Home Assistant" → "My Smart Home")
- Dark mode logo support
- Admin panel with drag-and-drop file upload

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
   - Performs text replacements throughout the DOM
   - Monitors for dynamic content changes

## Troubleshooting

### Logo not showing

1. Make sure the file exists in `/config/www/`
2. Clear your browser cache
3. Check browser console for errors

### Text replacements not working

1. Ensure the injector script is loaded (check `frontend.extra_module_url`)
2. Restart Home Assistant after configuration changes
3. Hard refresh your browser (Ctrl+Shift+R)

### Admin panel not appearing

1. Check if the component loaded successfully in the logs
2. Ensure you have admin privileges
3. Restart Home Assistant

## Limitations

- Some deeply nested elements in the HA core UI may not be replaced
- Text replacements work on visible text only, not on element attributes
- Changes to configuration require a page refresh to take effect

## Version History

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
