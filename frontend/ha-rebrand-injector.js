/**
 * HA Rebrand Injector
 *
 * This script injects into the Home Assistant frontend and replaces
 * brand elements (logo, favicon, sidebar title, text) with custom branding.
 *
 * Usage: Add this script to your Home Assistant frontend via extra_module_url
 */

(function() {
  'use strict';

  // Use static JSON file instead of API endpoint to avoid routing issues
  const REBRAND_CONFIG_URL = '/local/ha_rebrand/config.json';
  const CONFIG_RETRY_INTERVAL = 2000; // ms between config fetch retries
  const MAX_CONFIG_RETRIES = 5; // Maximum config fetch retry attempts
  const OBSERVER_TIMEOUT = 300000; // 5 minutes - disconnect observer after this time

  let config = null;
  let configRetryCount = 0;
  let isInitialized = false;
  let mainObserver = null;

  // Cached element references for performance
  let cachedSidebar = null;
  let cachedHaMain = null;

  /**
   * Fetch rebrand configuration from the API
   * Uses browser caching for better performance - config.json is updated on save
   */
  async function fetchConfig() {
    try {
      const response = await fetch(REBRAND_CONFIG_URL, {
        credentials: 'same-origin'  // Include auth cookies
      });
      if (response.ok) {
        config = await response.json();
        console.log('[HA Rebrand] Configuration loaded:', config);
        return true;
      } else {
        console.warn('[HA Rebrand] Config fetch failed with status:', response.status);
      }
    } catch (error) {
      console.warn('[HA Rebrand] Failed to fetch config:', error);
    }
    return false;
  }

  /**
   * Replace favicon
   */
  function replaceFavicon() {
    if (!config?.favicon) return;

    // Find and update existing favicons
    const favicons = document.querySelectorAll('link[rel*="icon"]');
    favicons.forEach(link => {
      link.href = config.favicon;
    });

    // If no favicon exists, create one
    if (favicons.length === 0) {
      const link = document.createElement('link');
      link.rel = 'icon';
      link.href = config.favicon;
      document.head.appendChild(link);
    }

    // Also update apple-touch-icon if logo exists
    if (config.logo) {
      let appleIcon = document.querySelector('link[rel="apple-touch-icon"]');
      if (!appleIcon) {
        appleIcon = document.createElement('link');
        appleIcon.rel = 'apple-touch-icon';
        document.head.appendChild(appleIcon);
      }
      appleIcon.href = config.logo;
    }
  }

  /**
   * Replace document title
   */
  function replaceDocumentTitle() {
    if (!config?.document_title) return;

    const originalTitle = document.title;

    // Replace "Home Assistant" in title
    if (originalTitle.includes('Home Assistant')) {
      document.title = originalTitle.replace(/Home Assistant/gi, config.document_title);
    } else if (originalTitle === '' || originalTitle === 'Home Assistant') {
      document.title = config.document_title;
    }

    // Monitor title changes
    const titleObserver = new MutationObserver(() => {
      if (document.title.includes('Home Assistant')) {
        document.title = document.title.replace(/Home Assistant/gi, config.document_title);
      }
    });

    const titleElement = document.querySelector('title');
    if (titleElement) {
      titleObserver.observe(titleElement, { childList: true, characterData: true, subtree: true });
    }
  }

  /**
   * Replace sidebar logo and title
   * Uses cached element references for better performance
   */
  function replaceSidebar() {
    // Use cached sidebar if still in DOM
    if (cachedSidebar && cachedSidebar.isConnected) {
      // Check if shadowRoot is still accessible
      if (cachedSidebar.shadowRoot) {
        return applySidebarChanges(cachedSidebar.shadowRoot);
      }
    }

    // Try to find the sidebar through Shadow DOM hierarchy
    let sidebar = document.querySelector('ha-sidebar');

    // If not found directly, try through home-assistant shadow DOM
    if (!sidebar) {
      const ha = document.querySelector('home-assistant');
      if (ha?.shadowRoot) {
        // Use cached haMain or find it
        if (!cachedHaMain || !cachedHaMain.isConnected) {
          cachedHaMain = ha.shadowRoot.querySelector('home-assistant-main');
        }
        if (cachedHaMain?.shadowRoot) {
          sidebar = cachedHaMain.shadowRoot.querySelector('ha-sidebar');
        }
      }
    }

    if (!sidebar) return false;

    // Cache the sidebar reference
    cachedSidebar = sidebar;

    const shadowRoot = sidebar.shadowRoot;
    if (!shadowRoot) return false;

    return applySidebarChanges(shadowRoot);
  }

  /**
   * Apply sidebar changes (extracted for reuse with cached element)
   */
  function applySidebarChanges(shadowRoot) {

    // Replace sidebar title
    if (config?.sidebar_title) {
      const titleElement = shadowRoot.querySelector('.title');
      if (titleElement && titleElement.textContent !== config.sidebar_title) {
        titleElement.textContent = config.sidebar_title;
      }
    }

    // Replace sidebar logo
    if (config?.logo) {
      const menu = shadowRoot.querySelector('.menu');
      if (menu) {
        // Check if we already replaced it
        let customLogo = menu.querySelector('.ha-rebrand-logo');
        if (!customLogo) {
          // Hide original logo if exists (older HA versions)
          const logoContainer = menu.querySelector('.logo');
          if (logoContainer) {
            const originalLogo = logoContainer.querySelector('img, ha-icon-button, ha-svg-icon');
            if (originalLogo) {
              originalLogo.style.display = 'none';
            }
          }

          // Create custom logo element
          customLogo = document.createElement('img');
          customLogo.className = 'ha-rebrand-logo';
          customLogo.src = config.logo;
          customLogo.alt = config.brand_name || 'Logo';
          customLogo.style.cssText = 'height: 40px; width: auto; max-width: 180px; object-fit: contain; margin: 12px 12px 4px 12px; display: block;';

          // Support dark mode logo
          if (config.logo_dark) {
            const isDarkMode = document.body.classList.contains('dark') ||
                              window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (isDarkMode) {
              customLogo.src = config.logo_dark;
            }

            // Listen for theme changes (single observer, stored to avoid duplicates)
            if (!window._rebrandThemeObserver) {
              window._rebrandThemeObserver = new MutationObserver(() => {
                const isDark = document.body.classList.contains('dark');
                const logos = document.querySelectorAll('.ha-rebrand-logo');
                logos.forEach(logo => {
                  if (logo.tagName === 'IMG') {
                    logo.src = isDark ? config.logo_dark : config.logo;
                  }
                });
              });
              window._rebrandThemeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
            }
          }

          // Insert logo at the beginning of menu (before title)
          const titleElement = menu.querySelector('.title');
          if (titleElement) {
            menu.insertBefore(customLogo, titleElement);
          } else {
            menu.prepend(customLogo);
          }
        }
      }
    }

    return true;
  }

  /**
   * Replace text throughout the page using replacements config
   */
  function replaceText() {
    if (!config?.replacements || Object.keys(config.replacements).length === 0) return;

    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );

    const nodesToUpdate = [];
    let node;

    while (node = walker.nextNode()) {
      const text = node.textContent;
      let newText = text;

      for (const [search, replace] of Object.entries(config.replacements)) {
        if (newText.includes(search)) {
          newText = newText.split(search).join(replace);
        }
      }

      if (newText !== text) {
        nodesToUpdate.push({ node, newText });
      }
    }

    // Apply updates
    nodesToUpdate.forEach(({ node, newText }) => {
      node.textContent = newText;
    });

    // Also check shadow DOMs of custom elements
    replaceShadowDOMText(document.body);
  }

  /**
   * Recursively replace text in shadow DOMs
   */
  function replaceShadowDOMText(root) {
    if (!config?.replacements) return;

    const elements = root.querySelectorAll('*');
    elements.forEach(el => {
      if (el.shadowRoot) {
        const walker = document.createTreeWalker(
          el.shadowRoot,
          NodeFilter.SHOW_TEXT,
          null,
          false
        );

        let node;
        while (node = walker.nextNode()) {
          let text = node.textContent;
          let changed = false;

          for (const [search, replace] of Object.entries(config.replacements)) {
            if (text.includes(search)) {
              text = text.split(search).join(replace);
              changed = true;
            }
          }

          if (changed) {
            node.textContent = text;
          }
        }

        // Recurse into shadow DOM
        replaceShadowDOMText(el.shadowRoot);
      }
    });
  }

  /**
   * Replace HA logo in various locations
   * Note: Loading screen logo is now handled by server-side HTML injection in __init__.py
   */
  function replaceLogos() {
    if (!config?.logo) return;

    // Common logo selectors
    const logoSelectors = [
      'ha-icon-button[slot="navigationIcon"]',
      '.ha-logo',
      'img[alt="Home Assistant"]',
      'img[src*="home-assistant"]',
    ];

    logoSelectors.forEach(selector => {
      const elements = document.querySelectorAll(selector);
      elements.forEach(el => {
        if (el.tagName === 'IMG') {
          el.src = config.logo;
          el.alt = config.brand_name || 'Logo';
        }
      });
    });

    // Replace login page logo (ha-authorize)
    replaceLoginLogo();

    // Note: replaceLoadingScreenLogo() removed - handled by server-side CSS/JS injection
  }

  /**
   * Replace logo on the login/authorize page
   */
  function replaceLoginLogo() {
    if (!config?.logo) return;

    // Find ha-authorize element
    const haAuthorize = document.querySelector('ha-authorize');
    if (!haAuthorize?.shadowRoot) return;

    // Find the logo SVG or image in the shadow DOM
    const shadowRoot = haAuthorize.shadowRoot;

    // Look for the HA logo (typically an SVG in ha-icon-button or standalone)
    const logoSelectors = [
      'ha-icon-button[slot="navigationIcon"]',
      '.logo',
      'ha-svg-icon',
      'svg',
      'img[alt="Home Assistant"]',
    ];

    // Try to find and replace the logo container
    let replaced = false;

    // Method 1: Find the SVG logo directly
    const svgLogos = shadowRoot.querySelectorAll('ha-svg-icon, svg');
    svgLogos.forEach(svg => {
      // Check if this looks like the HA logo (house shape)
      if (svg.closest('.logo') || svg.getAttribute('viewBox')?.includes('24') || svg.parentElement?.classList.contains('logo')) {
        if (!svg.classList.contains('ha-rebrand-hidden')) {
          svg.classList.add('ha-rebrand-hidden');
          svg.style.display = 'none';

          // Create replacement image
          const img = document.createElement('img');
          img.src = config.logo;
          img.alt = config.brand_name || 'Logo';
          img.className = 'ha-rebrand-login-logo';
          img.style.cssText = 'height: 80px; width: auto; max-width: 200px; object-fit: contain;';

          // Support dark mode
          if (config.logo_dark) {
            const isDarkMode = document.documentElement.classList.contains('dark') ||
                              document.body.classList.contains('dark') ||
                              window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (isDarkMode) {
              img.src = config.logo_dark;
            }
          }

          svg.parentElement.insertBefore(img, svg);
          replaced = true;
        }
      }
    });

    // Method 2: Look for the authorize page structure
    if (!replaced) {
      const authorizeContainer = shadowRoot.querySelector('.card-content, .content, .authorize');
      if (authorizeContainer) {
        // Find any existing logo image or icon
        const existingLogo = authorizeContainer.querySelector('img, ha-svg-icon, svg');
        if (existingLogo && !existingLogo.classList.contains('ha-rebrand-login-logo')) {
          existingLogo.style.display = 'none';

          const img = document.createElement('img');
          img.src = config.logo;
          img.alt = config.brand_name || 'Logo';
          img.className = 'ha-rebrand-login-logo';
          img.style.cssText = 'height: 80px; width: auto; max-width: 200px; object-fit: contain; display: block; margin: 0 auto 16px;';

          if (config.logo_dark) {
            const isDarkMode = document.documentElement.classList.contains('dark') ||
                              document.body.classList.contains('dark') ||
                              window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (isDarkMode) {
              img.src = config.logo_dark;
            }
          }

          existingLogo.parentElement.insertBefore(img, existingLogo);
        }
      }
    }
  }

  /**
   * Replace logo on the loading screen (ha-init-page)
   */
  function replaceLoadingScreenLogo() {
    if (!config?.logo) return;

    // Find ha-init-page element (loading screen)
    const haInitPage = document.querySelector('ha-init-page');
    if (!haInitPage?.shadowRoot) return;

    const shadowRoot = haInitPage.shadowRoot;

    // Find the main logo - look for ha-svg-icon first, then large SVGs
    // The main logo is typically a ha-svg-icon with the HA house icon
    const haSvgIcon = shadowRoot.querySelector('ha-svg-icon');
    if (haSvgIcon && !haSvgIcon.classList.contains('ha-rebrand-hidden')) {
      haSvgIcon.classList.add('ha-rebrand-hidden');
      haSvgIcon.style.display = 'none';

      // Create replacement image
      const img = document.createElement('img');
      img.src = config.logo;
      img.alt = config.brand_name || 'Logo';
      img.className = 'ha-rebrand-loading-logo';
      img.style.cssText = 'height: 120px; width: auto; max-width: 240px; object-fit: contain;';

      // Support dark mode
      if (config.logo_dark) {
        const isDarkMode = document.documentElement.classList.contains('dark') ||
                          document.body.classList.contains('dark') ||
                          window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (isDarkMode) {
          img.src = config.logo_dark;
        }
      }

      haSvgIcon.parentElement.insertBefore(img, haSvgIcon);
    }

    // Hide the Open Home Foundation footer if configured
    if (config.hide_open_home_foundation !== false) {
      // Method 1: Find links to openhomefoundation
      const footerLinks = shadowRoot.querySelectorAll('a[href*="openhomefoundation"], a[href*="home-assistant"]');
      footerLinks.forEach(link => {
        if (!link.classList.contains('ha-rebrand-hidden')) {
          link.classList.add('ha-rebrand-hidden');
          link.style.display = 'none';
        }
      });

      // Method 2: Find elements with "Open Home Foundation" or "HOME ASSISTANT" text
      const allElements = shadowRoot.querySelectorAll('*');
      allElements.forEach(el => {
        const text = el.textContent || '';
        if ((text.includes('Open Home Foundation') || text.includes('HOME ASSISTANT') || text.includes('OPEN HOME FOUNDATION'))
            && !el.classList.contains('ha-rebrand-hidden')) {
          // Check if this element or its parent contains only this text (no important children)
          if (el.children.length === 0 || el.tagName === 'A') {
            el.classList.add('ha-rebrand-hidden');
            el.style.display = 'none';
          } else {
            // Try to find and hide the specific text container
            const parent = el.closest('a, div[class*="footer"], div[class*="bottom"], span');
            if (parent && parent !== shadowRoot.host && !parent.classList.contains('ha-rebrand-hidden')) {
              parent.classList.add('ha-rebrand-hidden');
              parent.style.display = 'none';
            }
          }
        }
      });
    }
  }

  /**
   * Apply primary color to the entire interface
   * This changes --primary-color CSS variable which affects buttons, links, etc.
   */
  function applyPrimaryColor() {
    if (!config?.primary_color) return;

    // Create or update style element for color overrides
    let styleEl = document.getElementById('ha-rebrand-colors');
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = 'ha-rebrand-colors';
      document.head.appendChild(styleEl);
    }

    // Apply the primary color via CSS custom properties
    styleEl.textContent = `
      :root {
        --primary-color: ${config.primary_color} !important;
        --light-primary-color: ${config.primary_color}40 !important;
        --dark-primary-color: ${config.primary_color} !important;
      }
      html {
        --primary-color: ${config.primary_color} !important;
        --light-primary-color: ${config.primary_color}40 !important;
        --dark-primary-color: ${config.primary_color} !important;
      }
    `;

    console.log('[HA Rebrand] Applied primary color:', config.primary_color);
  }

  /**
   * Apply all rebrand changes
   */
  function applyRebrand() {
    if (!config) return false;

    replaceFavicon();
    replaceDocumentTitle();
    const sidebarReplaced = replaceSidebar();
    replaceLogos();
    replaceText();
    applyPrimaryColor();

    return sidebarReplaced;
  }

  /**
   * Wait for sidebar to appear using MutationObserver instead of polling
   * This is more efficient than the old 30-second polling approach
   */
  function waitForSidebar() {
    return new Promise((resolve) => {
      // First, try immediate application
      if (applyRebrand()) {
        console.log('[HA Rebrand] Successfully applied branding immediately');
        isInitialized = true;
        resolve(true);
        return;
      }

      // Use MutationObserver to wait for sidebar
      const observer = new MutationObserver((mutations, obs) => {
        if (applyRebrand()) {
          console.log('[HA Rebrand] Successfully applied branding after DOM ready');
          isInitialized = true;
          obs.disconnect();
          resolve(true);
        }
      });

      // Only observe home-assistant element for better performance
      const ha = document.querySelector('home-assistant');
      if (ha) {
        observer.observe(ha, { childList: true, subtree: true });
      } else {
        // Fallback: observe body but only for direct children
        observer.observe(document.body, { childList: true });
      }

      // Timeout after 10 seconds instead of 30
      setTimeout(() => {
        observer.disconnect();
        if (!isInitialized) {
          console.warn('[HA Rebrand] Timeout waiting for sidebar, applying available changes');
          applyRebrand();
          isInitialized = true;
        }
        resolve(isInitialized);
      }, 10000);
    });
  }

  /**
   * Set up mutation observer to handle dynamic content
   * Uses targeted observation for better performance
   */
  function setupMutationObserver() {
    // Disconnect existing observer if any
    if (mainObserver) {
      mainObserver.disconnect();
    }

    let debounceTimer = null;

    mainObserver = new MutationObserver((mutations) => {
      // Debounce the rebrand application
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        applyRebrand();
      }, 150);
    });

    // Try to observe only the main content area for better performance
    const ha = document.querySelector('home-assistant');
    if (ha?.shadowRoot) {
      const haMain = ha.shadowRoot.querySelector('home-assistant-main');
      if (haMain) {
        mainObserver.observe(haMain, { childList: true, subtree: true });
      } else {
        // Fallback: observe home-assistant shadow root
        mainObserver.observe(ha.shadowRoot, { childList: true, subtree: true });
      }
    } else {
      // Fallback: observe body but with limited depth
      mainObserver.observe(document.body, { childList: true, subtree: true });
    }

    // Disconnect observer after timeout to prevent memory leaks
    setTimeout(() => {
      if (mainObserver) {
        mainObserver.disconnect();
        console.log('[HA Rebrand] Observer disconnected after timeout');
      }
    }, OBSERVER_TIMEOUT);

    // Also observe for route changes
    window.addEventListener('location-changed', () => {
      setTimeout(applyRebrand, 100);
    });

    // Handle popstate for browser navigation
    window.addEventListener('popstate', () => {
      setTimeout(applyRebrand, 100);
    });
  }

  /**
   * Initialize the rebrand injector
   */
  async function init() {
    console.log('[HA Rebrand] Initializing...');

    const configLoaded = await fetchConfig();
    if (!configLoaded) {
      configRetryCount++;
      if (configRetryCount < MAX_CONFIG_RETRIES) {
        console.warn(`[HA Rebrand] Could not load configuration, retrying in ${CONFIG_RETRY_INTERVAL / 1000} seconds... (attempt ${configRetryCount}/${MAX_CONFIG_RETRIES})`);
        setTimeout(init, CONFIG_RETRY_INTERVAL);
      } else {
        console.error('[HA Rebrand] Failed to load configuration after maximum retries. Rebrand disabled.');
      }
      return;
    }

    // Reset retry count on success
    configRetryCount = 0;

    // Wait for sidebar using event-based approach (replaces 30-second polling)
    await waitForSidebar();

    // Set up mutation observer for dynamic content
    setupMutationObserver();
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export for debugging
  window.HARebrand = {
    getConfig: () => config,
    refresh: applyRebrand,
    reloadConfig: async () => {
      await fetchConfig();
      applyRebrand();
    }
  };

})();
