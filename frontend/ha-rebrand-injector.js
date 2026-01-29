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
  const POLL_INTERVAL = 500; // ms between DOM checks
  const MAX_POLLS = 60; // Maximum number of polls (30 seconds)
  const CONFIG_RETRY_INTERVAL = 2000; // ms between config fetch retries
  const MAX_CONFIG_RETRIES = 5; // Maximum config fetch retry attempts

  let config = null;
  let pollCount = 0;
  let configRetryCount = 0;
  let isInitialized = false;

  /**
   * Fetch rebrand configuration from the API
   */
  async function fetchConfig() {
    try {
      // Add cache-busting query parameter to avoid browser caching
      const cacheBuster = `?_t=${Date.now()}`;
      const response = await fetch(REBRAND_CONFIG_URL + cacheBuster, {
        credentials: 'same-origin',  // Include auth cookies
        cache: 'no-store'  // Force no caching
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
   */
  function replaceSidebar() {
    // Try to find the sidebar through Shadow DOM hierarchy
    let sidebar = document.querySelector('ha-sidebar');

    // If not found directly, try through home-assistant shadow DOM
    if (!sidebar) {
      const ha = document.querySelector('home-assistant');
      if (ha?.shadowRoot) {
        const haMain = ha.shadowRoot.querySelector('home-assistant-main');
        if (haMain?.shadowRoot) {
          sidebar = haMain.shadowRoot.querySelector('ha-sidebar');
        }
      }
    }

    if (!sidebar) return false;

    const shadowRoot = sidebar.shadowRoot;
    if (!shadowRoot) return false;

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

            // Listen for theme changes
            const themeObserver = new MutationObserver(() => {
              const isDark = document.body.classList.contains('dark');
              customLogo.src = isDark ? config.logo_dark : config.logo;
            });
            themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
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

    return sidebarReplaced;
  }

  /**
   * Poll for DOM changes and apply rebrand
   */
  function pollAndApply() {
    pollCount++;

    const success = applyRebrand();

    if (!success && pollCount < MAX_POLLS) {
      setTimeout(pollAndApply, POLL_INTERVAL);
    } else if (success) {
      console.log('[HA Rebrand] Successfully applied branding');
      isInitialized = true;

      // Set up mutation observer for dynamic content
      setupMutationObserver();
    }
  }

  /**
   * Set up mutation observer to handle dynamic content
   */
  function setupMutationObserver() {
    const observer = new MutationObserver((mutations) => {
      // Debounce the rebrand application
      clearTimeout(window._rebrandTimeout);
      window._rebrandTimeout = setTimeout(() => {
        applyRebrand();
      }, 100);
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });

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

    // Start polling for DOM
    pollAndApply();
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
