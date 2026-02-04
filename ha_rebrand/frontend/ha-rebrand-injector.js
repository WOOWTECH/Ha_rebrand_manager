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
  let isApplying = false;  // Re-entrance guard to prevent feedback loops
  let titleObserverCreated = false;  // Prevent multiple title observers
  let waitForSidebarRafPending = false;  // Prevent multiple RAF callbacks flooding

  // Cached element references for performance
  let cachedSidebar = null;
  let cachedHaMain = null;

  /**
   * Parse color string to RGB values
   * Supports hex (#RGB, #RRGGBB) and rgb/rgba formats
   */
  function parseColor(color) {
    if (!color) return null;
    color = color.trim();

    // Handle hex colors
    if (color.startsWith('#')) {
      const hex = color.slice(1);
      if (hex.length === 3) {
        return {
          r: parseInt(hex[0] + hex[0], 16),
          g: parseInt(hex[1] + hex[1], 16),
          b: parseInt(hex[2] + hex[2], 16)
        };
      }
      if (hex.length === 6) {
        return {
          r: parseInt(hex.slice(0, 2), 16),
          g: parseInt(hex.slice(2, 4), 16),
          b: parseInt(hex.slice(4, 6), 16)
        };
      }
    }

    // Handle rgb/rgba colors
    const rgbMatch = color.match(/rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
    if (rgbMatch) {
      return {
        r: parseInt(rgbMatch[1]),
        g: parseInt(rgbMatch[2]),
        b: parseInt(rgbMatch[3])
      };
    }

    return null;
  }

  /**
   * Calculate relative luminance of a color
   * Returns value between 0 (black) and 1 (white)
   * Uses WCAG 2.1 formula for relative luminance
   */
  function getLuminance(rgb) {
    if (!rgb) return 0.5;
    const { r, g, b } = rgb;
    const [rs, gs, bs] = [r, g, b].map(c => {
      c = c / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
  }

  /**
   * Detect if Home Assistant is in dark mode
   * Uses multiple detection methods in priority order:
   * 1. color-scheme meta tag (most reliable for HA)
   * 2. CSS variable luminance check
   * 3. Legacy class checks
   * 4. System preference fallback
   */
  function isHADarkMode() {
    // Method 1: Check color-scheme meta tag (most reliable for HA)
    // HA sets this meta tag based on theme in themes-mixin.ts
    const colorSchemeMeta = document.querySelector('meta[name="color-scheme"]');
    if (colorSchemeMeta) {
      const content = colorSchemeMeta.getAttribute('content');
      if (content === 'dark') return true;
      if (content === 'light') return false;
    }

    // Method 2: Check primary background color luminance
    const bgColor = getComputedStyle(document.documentElement)
      .getPropertyValue('--primary-background-color').trim();
    if (bgColor) {
      const rgb = parseColor(bgColor);
      if (rgb && getLuminance(rgb) < 0.2) return true;
    }

    // Method 3: Legacy class checks (for compatibility with other setups)
    if (document.body.classList.contains('dark')) return true;
    if (document.documentElement.classList.contains('dark')) return true;

    // Method 4: System preference (fallback)
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) return true;

    return false;
  }

  /**
   * Update all rebrand logos based on current theme
   */
  function updateLogosForTheme() {
    if (!config?.logo_dark) return;
    const isDark = isHADarkMode();
    const logos = document.querySelectorAll('.ha-rebrand-logo');
    logos.forEach(logo => {
      if (logo.tagName === 'IMG') {
        logo.src = isDark ? config.logo_dark : config.logo;
      }
    });
  }

  /**
   * Set up theme change observers for dark mode detection
   * Watches meta tag, body class, and system preference
   */
  function setupThemeObservers() {
    if (window._rebrandThemeObserversSet) return;
    window._rebrandThemeObserversSet = true;

    // Observer for color-scheme meta tag changes (primary method for HA)
    const colorSchemeMeta = document.querySelector('meta[name="color-scheme"]');
    if (colorSchemeMeta) {
      const metaObserver = new MutationObserver(updateLogosForTheme);
      metaObserver.observe(colorSchemeMeta, { attributes: true, attributeFilter: ['content'] });
    }

    // Observer for body class changes (legacy support)
    const bodyObserver = new MutationObserver(updateLogosForTheme);
    bodyObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });

    // Listen for system preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateLogosForTheme);
  }

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
   * Note: Only creates observer once to prevent multiple observers stacking up
   */
  function replaceDocumentTitle() {
    if (!config?.document_title) return;

    const originalTitle = document.title;

    // Replace "Home Assistant" in title (only if it produces a different result)
    // This prevents infinite loop when document_title contains "Home Assistant"
    const newTitle = originalTitle.replace(/Home Assistant/gi, config.document_title);
    if (newTitle !== originalTitle) {
      document.title = newTitle;
    } else if (originalTitle === '') {
      document.title = config.document_title;
    }

    // Only create title observer once to prevent multiple observers stacking up
    if (!titleObserverCreated) {
      titleObserverCreated = true;

      // Monitor title changes
      const titleObserver = new MutationObserver(() => {
        const currentTitle = document.title;
        const newTitle = currentTitle.replace(/Home Assistant/gi, config.document_title);
        // Only update if the replacement actually changes the title
        // This prevents infinite loop when document_title contains "Home Assistant"
        if (newTitle !== currentTitle) {
          document.title = newTitle;
        }
      });

      const titleElement = document.querySelector('title');
      if (titleElement) {
        titleObserver.observe(titleElement, { childList: true, characterData: true, subtree: true });
      }
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
            if (isHADarkMode()) {
              customLogo.src = config.logo_dark;
            }
            // Set up theme change observers (handles meta tag, body class, and system preference)
            setupThemeObservers();
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

  // Cache for pre-compiled replacement patterns (performance optimization)
  let compiledReplacements = null;

  /**
   * Escape special regex characters in a string
   */
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * Compile replacement rules into regex patterns (called once)
   */
  function compileReplacements() {
    if (!config?.replacements || Object.keys(config.replacements).length === 0) {
      compiledReplacements = null;
      return;
    }
    compiledReplacements = Object.entries(config.replacements).map(([search, replace]) => ({
      pattern: new RegExp(escapeRegExp(search), 'g'),
      replacement: replace
    }));
  }

  /**
   * Replace text throughout the page using replacements config
   * Optimized: Uses pre-compiled regex and limits traversal scope
   */
  function replaceText() {
    if (!compiledReplacements || compiledReplacements.length === 0) return;

    // Limit traversal to main content area for better performance
    const rootElement = document.querySelector('home-assistant-main') ||
                       document.querySelector('ha-panel-lovelace') ||
                       document.body;

    const walker = document.createTreeWalker(
      rootElement,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );

    const nodesToUpdate = [];
    let node;

    while (node = walker.nextNode()) {
      const text = node.textContent;
      let newText = text;
      let changed = false;

      // Use pre-compiled regex for faster replacement
      for (const { pattern, replacement } of compiledReplacements) {
        const result = newText.replace(pattern, replacement);
        if (result !== newText) {
          newText = result;
          changed = true;
        }
      }

      if (changed) {
        nodesToUpdate.push({ node, newText });
      }
    }

    // Apply updates in batch
    nodesToUpdate.forEach(({ node, newText }) => {
      node.textContent = newText;
    });

    // Also check shadow DOMs of custom elements (with limited scope)
    replaceShadowDOMText(rootElement);
  }

  // Maximum depth for shadow DOM traversal to prevent stack overflow
  const MAX_SHADOW_DOM_DEPTH = 10;

  /**
   * Recursively replace text in shadow DOMs
   * IMPORTANT: Must exit early if no replacements to prevent infinite DOM traversal
   * @param {ShadowRoot|Element} root - The root element to start traversal from
   * @param {number} depth - Current recursion depth (defaults to 0)
   */
  function replaceShadowDOMText(root, depth = 0) {
    // Exit early if no replacements or empty replacements object
    // This prevents expensive DOM traversal when there's nothing to replace
    if (!config?.replacements || Object.keys(config.replacements).length === 0) return;
    if (!compiledReplacements || compiledReplacements.length === 0) return;

    // Prevent infinite recursion / stack overflow with deep shadow DOM nesting
    if (depth >= MAX_SHADOW_DOM_DEPTH) {
      console.warn('[HA Rebrand] Max shadow DOM depth reached, stopping traversal');
      return;
    }

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
        const nodesToUpdate = [];
        while (node = walker.nextNode()) {
          let text = node.textContent;
          let newText = text;
          let changed = false;

          // Use pre-compiled regex for faster replacement (consistent with replaceText())
          for (const { pattern, replacement } of compiledReplacements) {
            const result = newText.replace(pattern, replacement);
            if (result !== newText) {
              newText = result;
              changed = true;
            }
          }

          if (changed) {
            nodesToUpdate.push({ node, newText });
          }
        }

        // Apply updates in batch (avoids DOM mutation during traversal)
        nodesToUpdate.forEach(({ node, newText }) => {
          node.textContent = newText;
        });

        // Recurse into shadow DOM with incremented depth
        replaceShadowDOMText(el.shadowRoot, depth + 1);
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
          if (config.logo_dark && isHADarkMode()) {
            img.src = config.logo_dark;
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

          if (config.logo_dark && isHADarkMode()) {
            img.src = config.logo_dark;
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
      if (config.logo_dark && isHADarkMode()) {
        img.src = config.logo_dark;
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
   * Note: Each function has its own early-exit checks for missing config values
   * Uses re-entrance guard to prevent feedback loops from MutationObserver
   */
  function applyRebrand() {
    if (!config) return false;
    if (isApplying) return false;  // Prevent re-entrance during DOM modifications

    isApplying = true;
    try {
      replaceFavicon();
      replaceDocumentTitle();
      const sidebarReplaced = replaceSidebar();
      replaceLogos();
      // replaceText() and replaceShadowDOMText() now have proper early-exit checks
      // to prevent expensive DOM traversal when no replacements are configured
      replaceText();
      applyPrimaryColor();

      return sidebarReplaced;
    } finally {
      isApplying = false;
    }
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
      // Use requestAnimationFrame to break synchronous mutation loop
      // Only schedule one RAF callback at a time to prevent queue flooding
      const observer = new MutationObserver((mutations, obs) => {
        // Only schedule one RAF callback at a time
        if (waitForSidebarRafPending) return;
        waitForSidebarRafPending = true;

        requestAnimationFrame(() => {
          waitForSidebarRafPending = false;

          // Disconnect BEFORE making changes to prevent feedback loop
          obs.disconnect();

          if (applyRebrand()) {
            console.log('[HA Rebrand] Successfully applied branding after DOM ready');
            isInitialized = true;
            resolve(true);
            return;
          }

          // Reconnect if not successful yet (sidebar not found)
          const ha = document.querySelector('home-assistant');
          if (ha) {
            obs.observe(ha, { childList: true, subtree: true });
          } else {
            obs.observe(document.body, { childList: true });
          }
        });
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
   * Uses targeted observation and filtering for better performance
   */
  function setupMutationObserver() {
    // Disconnect existing observer if any
    if (mainObserver) {
      mainObserver.disconnect();
    }

    let debounceTimer = null;

    mainObserver = new MutationObserver((mutations) => {
      // Filter: only process relevant mutations (performance optimization)
      const hasRelevantChanges = mutations.some(mutation => {
        // Only care about added nodes
        if (mutation.type !== 'childList' || mutation.addedNodes.length === 0) {
          return false;
        }
        // Check if any added node is HA-related
        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const tagName = node.tagName?.toLowerCase() || '';
            if (tagName.startsWith('ha-') || tagName.startsWith('hui-') ||
                tagName === 'home-assistant-main' || tagName === 'ha-sidebar') {
              return true;
            }
          }
        }
        return false;
      });

      if (!hasRelevantChanges) return;

      // Debounce with longer interval (300ms) for better performance
      if (debounceTimer) clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        applyRebrand();
      }, 300);
    });

    // Try to observe only the main content area for better performance
    const ha = document.querySelector('home-assistant');
    if (ha?.shadowRoot) {
      const haMain = ha.shadowRoot.querySelector('home-assistant-main');
      if (haMain) {
        // Observe haMain without subtree for better performance
        mainObserver.observe(haMain, { childList: true, subtree: false });
        // Also observe haMain's shadowRoot if exists
        if (haMain.shadowRoot) {
          mainObserver.observe(haMain.shadowRoot, { childList: true, subtree: false });
        }
      } else {
        // Fallback: observe home-assistant shadow root
        mainObserver.observe(ha.shadowRoot, { childList: true, subtree: false });
      }
    } else {
      // Fallback: observe body but without subtree
      mainObserver.observe(document.body, { childList: true, subtree: false });
    }

    // Disconnect observer after timeout to prevent memory leaks
    setTimeout(() => {
      if (mainObserver) {
        mainObserver.disconnect();
        mainObserver = null;
        console.log('[HA Rebrand] Observer disconnected after timeout');
      }
    }, OBSERVER_TIMEOUT);

    // Also observe for route changes (only add once)
    if (!window._rebrandRouteListenerAdded) {
      window._rebrandRouteListenerAdded = true;
      window.addEventListener('location-changed', () => {
        setTimeout(applyRebrand, 100);
      });
      // Handle popstate for browser navigation
      window.addEventListener('popstate', () => {
        setTimeout(applyRebrand, 100);
      });
    }
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

    // Compile replacement patterns once for better performance
    compileReplacements();

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
