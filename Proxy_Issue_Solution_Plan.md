# Proxy Issue Solution Plan

## Table of Contents
1. [How NPM + Cloudflared + Zero Trust Work Together](#1-how-npm--cloudflared--zero-trust-work-together)
2. [How trusted_proxies Work in Home Assistant](#2-how-trusted_proxies-work-in-home-assistant)
3. [Why ha_rebrand Affects Remote Access](#3-why-ha_rebrand-affects-remote-access)
4. [Solution Plan](#4-solution-plan)

---

## 1. How NPM + Cloudflared + Zero Trust Work Together

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INTERNET                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CLOUDFLARE EDGE (Global CDN)                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    Cloudflare Zero Trust Access                      │    │
│  │  • Enforces authentication (Google, GitHub, SAML, etc.)              │    │
│  │  • Sets CF_Authorization cookie (JWT token)                         │    │
│  │  • Applies access policies (who can access, from where)             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    Cloudflare Tunnel (encrypted, outbound-only)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HOME ASSISTANT SUPERVISOR NETWORK                         │
│                         (Docker: 172.30.32.0/23)                             │
│                                                                              │
│  ┌──────────────────────┐    ┌──────────────────────┐                       │
│  │  Cloudflared Add-on  │───▶│  Nginx Proxy Manager │                       │
│  │   (172.30.33.x)      │    │    (172.30.33.x)     │                       │
│  │                      │    │                      │                       │
│  │  • Receives tunnel   │    │  • SSL termination   │                       │
│  │  • Forwards to NPM   │    │  • WebSocket upgrade │                       │
│  │    or HA directly    │    │  • Proxy headers     │                       │
│  └──────────────────────┘    └──────────────────────┘                       │
│                                       │                                      │
│                                       ▼                                      │
│                         ┌──────────────────────┐                            │
│                         │  Home Assistant Core │                            │
│                         │    (172.30.32.1)     │                            │
│                         │      Port: 8123      │                            │
│                         │                      │                            │
│                         │  • HTTP API          │                            │
│                         │  • WebSocket API     │                            │
│                         │  • Frontend serving  │                            │
│                         └──────────────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

#### Cloudflare Zero Trust Access
- **Authentication Gateway**: Requires users to authenticate (Google, GitHub, etc.) before accessing the tunnel
- **Session Management**: Issues `CF_Authorization` JWT cookie upon successful auth
- **Policy Enforcement**: Controls who can access based on email, groups, IP, device posture
- **Cookie Attributes**: Sets `SameSite`, `Secure`, `HttpOnly` flags on auth cookies

#### Cloudflared (Tunnel Agent)
- **Outbound Connection**: Establishes persistent outbound connection to Cloudflare edge (no inbound firewall rules needed)
- **Traffic Forwarding**: Receives requests from Cloudflare and forwards to local service
- **Configuration Options**:
  ```yaml
  # Option A: Direct to HA (simpler, but no NPM features)
  service: http://homeassistant:8123

  # Option B: Through NPM (SSL termination, multiple domains)
  service: http://nginxproxymanager:80
  ```

#### Nginx Proxy Manager (NPM)
- **Reverse Proxy**: Forwards requests to backend services
- **WebSocket Support**: Upgrades HTTP connections to WebSocket for `/api/websocket`
- **Header Management**: Adds `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Real-IP` headers
- **SSL/TLS**: Can handle SSL termination (optional with Cloudflare)

### Request Flow (Step by Step)

```
1. User visits: https://ha.example.com
                    │
2. Cloudflare Edge receives request
                    │
3. Zero Trust checks for CF_Authorization cookie
   ├── Cookie missing/expired → Redirect to auth page
   └── Cookie valid → Continue to tunnel
                    │
4. Request sent through Cloudflare Tunnel
                    │
5. Cloudflared receives request in local network
                    │
6. Cloudflared forwards to configured service (NPM or HA)
                    │
7. NPM (if configured):
   ├── Matches domain to proxy host
   ├── Adds proxy headers (X-Forwarded-*)
   ├── Upgrades WebSocket if /api/websocket
   └── Forwards to HA at 172.30.32.1:8123
                    │
8. Home Assistant:
   ├── Reads X-Forwarded-For header (if trusted_proxies configured)
   ├── Processes request
   └── Returns response
                    │
9. Response travels back through: HA → NPM → Cloudflared → Tunnel → Edge → User
```

### WebSocket Connection Flow

The WebSocket connection for real-time updates is critical:

```
1. Frontend loads at /
2. JavaScript initiates WebSocket: ws://ha.example.com/api/websocket
3. Browser sends HTTP Upgrade request with headers:
   - Connection: Upgrade
   - Upgrade: websocket
   - Sec-WebSocket-Key: [random]
   - Cookie: CF_Authorization=xxx (if Cloudflare auth)

4. Each proxy must handle the upgrade:
   - Cloudflare Edge: Passes through
   - Cloudflared: Maintains persistent connection
   - NPM: Upgrades connection (requires WebSocket Support toggle ON)
   - HA: Accepts upgrade, establishes WebSocket

5. If ANY hop fails to upgrade → "Loading data" spinner forever
```

---

## 2. How trusted_proxies Work in Home Assistant

### Purpose

Home Assistant needs to know which IP addresses are trusted reverse proxies. Without this:
- All requests appear to come from the proxy's IP, not the real user
- Rate limiting, banning, and logging become useless
- Security features like IP-based restrictions fail

### How It Works

```yaml
# configuration.yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.30.32.0/23   # Supervisor network (Core + Add-ons)
    - 127.0.0.1        # Localhost
    - ::1              # IPv6 localhost
```

#### `use_x_forwarded_for: true`
- Tells HA to read client IP from `X-Forwarded-For` header
- Only works if the request comes from a trusted_proxies IP

#### `trusted_proxies`
- List of IP addresses/CIDR ranges that HA trusts to set proxy headers
- If request comes from unlisted IP, `X-Forwarded-*` headers are **ignored**

### Home Assistant Supervisor Network Architecture

```
172.30.32.0/23 (Supervisor-managed network)
├── 172.30.32.0/24 (Core services)
│   ├── 172.30.32.1  - Home Assistant Core
│   ├── 172.30.32.2  - Supervisor
│   ├── 172.30.32.3  - DNS
│   └── 172.30.32.6  - Observer
│
└── 172.30.33.0/24 (Add-ons)
    ├── 172.30.33.x  - Nginx Proxy Manager
    ├── 172.30.33.x  - Cloudflared
    └── 172.30.33.x  - Other add-ons
```

### Why 172.30.32.0/23 is Correct

| CIDR | Range | Covers |
|------|-------|--------|
| 172.30.32.0/24 | 172.30.32.0 - 172.30.32.255 | Core services only |
| 172.30.33.0/24 | 172.30.33.0 - 172.30.33.255 | Add-ons only |
| **172.30.32.0/23** | 172.30.32.0 - 172.30.33.255 | **Both ranges** |

Using `/23` ensures both Core services AND add-ons (including NPM) are trusted.

### Request Processing with Proxy Headers

```
Request arrives from NPM (172.30.33.5):
Headers:
  X-Forwarded-For: 203.0.113.50, 162.158.0.1
  X-Forwarded-Proto: https
  X-Real-IP: 203.0.113.50

HA Processing:
1. Check if 172.30.33.5 is in trusted_proxies
   └── Yes (172.30.32.0/23 includes it)
2. Read X-Forwarded-For header
3. Use 203.0.113.50 as the real client IP
4. Log: "Request from 203.0.113.50"
```

### Common Misconfigurations

| Configuration | Problem |
|---------------|---------|
| `trusted_proxies: []` | No proxy trusted, all headers ignored |
| `trusted_proxies: 172.30.33.0/24` | Core services not trusted if routing through them |
| `trusted_proxies: 127.0.0.1` | Only localhost trusted, Docker containers not trusted |
| `use_x_forwarded_for: false` | Proxy headers completely ignored |

### Security Implications

**Never** add public IPs to trusted_proxies:
```yaml
# DANGEROUS - DO NOT DO THIS
http:
  trusted_proxies:
    - 0.0.0.0/0  # Trusts the entire internet!
```

This would allow anyone to spoof their IP address by setting `X-Forwarded-For`.

---

## 3. Why ha_rebrand Affects Remote Access

### What ha_rebrand Does

The `ha_rebrand` custom component modifies Home Assistant's frontend to allow custom branding:
- Custom logo on loading screen and login page
- Custom favicon
- Custom sidebar title
- Text replacements throughout the UI

### Critical Code Path: RebrandAuthorizeView

The component registers a **custom HTTP view** that replaces the standard `/auth/authorize` endpoint:

```python
# From __init__.py lines 651-783
class RebrandAuthorizeView(HomeAssistantView):
    url = "/auth/authorize"
    name = "api:ha_rebrand:authorize"
    requires_auth = False  # Must be accessible without auth
```

This view:
1. **Removes** the original static `/auth/authorize` route
2. **Registers** a dynamic view that modifies the HTML
3. **Serves** customized `authorize.html` with branding

### How Route Replacement Works

```python
# From __init__.py lines 289-345
def _unregister_authorize_static_path(hass: HomeAssistant) -> bool:
    """Remove the existing /auth/authorize static path."""
    app = hass.http.app
    router = app.router

    # Find and remove the resource for /auth/authorize
    for resource in router.resources():
        if hasattr(resource, "_path") and resource._path == "/auth/authorize":
            resources_to_remove.append(resource)

    # Remove from router
    for resource in resources_to_remove:
        if hasattr(router, "_resources"):
            router._resources.remove(resource)
```

This manipulates aiohttp's internal router state, which can cause issues with:
- Router indexing
- Resource lookup
- URL generation

### Response Headers Added

The `RebrandAuthorizeView` adds specific headers (lines 777-782):

```python
headers={
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
    "X-Content-Type-Options": "nosniff",
}
```

These headers are **correct** for proxy compatibility, but...

### Potential Issues with Proxies

#### Issue 1: Route Registration Order

When ha_rebrand unregisters the original route and registers a new one, the timing matters:
- If NPM or Cloudflare caches the route resolution
- If the route removal fails silently
- If another component tries to access `/auth/authorize` during the transition

#### Issue 2: WebSocket Interaction

The component also patches the IndexView (lines 348-446):

```python
def _patch_index_view(hass: HomeAssistant) -> None:
    """Patch IndexView to inject early branding script for loading screen."""
    original_get_template = frontend.IndexView.get_template

    def patched_get_template(self):
        tpl = original_get_template(self)
        # ... modify template ...
```

This patching:
- Injects JavaScript that runs before the main app
- Uses MutationObserver to monitor DOM changes
- Could interfere with WebSocket initialization timing

#### Issue 3: JavaScript Injection

The injected JavaScript (lines 408-433):

```javascript
var obs=new MutationObserver(fix);
obs.observe(document.body,{childList:true,subtree:true});
setTimeout(function(){obs.disconnect();},15000);
```

- Observes ALL DOM mutations for 15 seconds
- Could affect performance during initial load
- May interfere with HA's own initialization code

### Why Incognito Mode is More Affected

1. **No Cached Resources**: Regular Chrome has cached JavaScript, CSS, and tokens
2. **Fresh Authentication Flow**: Must complete full Cloudflare + HA auth
3. **Timing Sensitivity**: The patched views must work perfectly on first load
4. **No localStorage Fallback**: Token storage falls back to memory-only

### Diagnostic: Check if ha_rebrand is the Cause

```bash
# Temporarily disable ha_rebrand
# In HA: Settings → Devices & Services → ha_rebrand → Disable

# Or remove from configuration.yaml if using YAML config
# ha_rebrand:
#   brand_name: "My Home"

# Restart HA and test incognito mode
```

If incognito works after disabling ha_rebrand, the component is contributing to the issue.

---

## 4. Solution Plan

### Phase 1: Verify Home Assistant Configuration

```yaml
# configuration.yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 172.30.32.0/23
    - 127.0.0.1
    - ::1
```

### Phase 2: NPM Configuration

**Step 1.1: NPM Custom Config**
1. Open NPM Admin Panel (`http://<ha-ip>:81`)
2. Edit proxy host for homeassistant
    - Go to **Details** tab : Enable **Websockets Support**
    - Go to **Advanced** tab : **Delete ALL custom nginx configuration**
3. Save

**Step 1.2: Test**
- Regular browser: Should work
- If "Congratulations" page appears, NPM hostname resolution failed

**Step 1.3: If Hostname Resolution Fails**
Change Forward Hostname from `homeassistant` to `172.30.32.1`:
1. Edit proxy host in NPM
2. Change **Forward Hostname / IP** to `172.30.32.1`
3. Keep **Forward Port** as `8123`
4. Save
