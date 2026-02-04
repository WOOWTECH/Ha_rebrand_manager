---
name: remove-text-replacements
description: Remove the unused Text Replacements feature from Ha_rebrand custom component
status: backlog
created: 2026-02-04T06:05:46Z
---

# PRD: Remove Text Replacements Feature

## Executive Summary

Remove the Text Replacements functionality from the Ha_rebrand custom component. This feature allows users to define text-to-text mappings that get applied across the Home Assistant interface. The feature is unused and adds unnecessary complexity to the codebase. Complete removal of all related code, UI elements, and documentation while maintaining backward compatibility with existing configurations.

## Problem Statement

The Text Replacements feature:
- Is not being used by the target user base
- Adds maintenance overhead and code complexity
- Increases the attack surface (regex processing, DOM manipulation)
- Adds performance overhead (MutationObserver, DOM traversal)

Removing this feature will simplify the codebase and reduce maintenance burden.

## User Stories

### Primary User Story
As a Ha_rebrand maintainer, I want to remove the Text Replacements feature so that the codebase is simpler and easier to maintain.

### Acceptance Criteria
- All Text Replacements UI elements are removed from the admin panel
- All backend code handling replacements is removed
- Existing configurations with replacements entries do not cause errors
- The component continues to function normally for all other features

## Requirements

### Functional Requirements

**FR1: Remove Frontend UI**
- Remove the "Text Replacements" section from ha-rebrand-panel.js
- Remove input fields for adding new replacements
- Remove the replacements list display
- Remove delete buttons for replacement entries

**FR2: Remove Frontend Logic**
- Remove `compileReplacements()` function from ha-rebrand-injector.js
- Remove `replaceText()` function
- Remove `replaceShadowDOMText()` function
- Remove replacement-related calls from `applyRebrand()`
- Remove `_newReplaceKey` and `_newReplaceValue` properties
- Remove `_addReplacement()` and `_removeReplacement()` methods

**FR3: Remove Backend Logic**
- Remove `CONF_REPLACEMENTS` handling from __init__.py
- Remove replacements from WebSocket API (`ha_rebrand/update_config`, `ha_rebrand/get_config`)
- Remove replacements from HTTP endpoints
- Keep config schema flexible to silently ignore existing replacement entries

**FR4: Clean Up Constants**
- Remove `CONF_REPLACEMENTS` constant from const.py
- Remove `DEFAULT_REPLACEMENTS` constant from const.py

**FR5: Update Translations**
- Remove replacement-related strings from strings.json
- Remove replacement-related strings from translations/en.json
- Remove replacement-related strings from translations/zh-Hant.json

### Non-Functional Requirements

**NFR1: Backward Compatibility**
- Existing configurations with `replacements` entries must not cause errors
- Component must load and function normally even if old config has replacements

**NFR2: No Breaking Changes**
- All other Ha_rebrand features must continue working
- Logo replacement, favicon replacement, color theming, sidebar customization unaffected

## Success Criteria

1. Admin panel loads without Text Replacements section
2. No JavaScript errors related to missing replacement functions
3. No Python errors when loading configs with old replacement entries
4. All other rebranding features work correctly
5. Code reduction of approximately 200+ lines

## Constraints & Assumptions

### Constraints
- Must maintain backward compatibility with existing config files
- Cannot break other features during removal

### Assumptions
- No users actively depend on this feature
- Feature removal will not require a major version bump

## Out of Scope

- Adding alternative text customization features
- Modifying other rebranding features
- Updating version numbers or release notes

## Dependencies

- None - this is a self-contained removal

## Files to Modify

### Backend (Python)
| File | Action | Changes |
|------|--------|---------|
| `ha_rebrand/const.py` | Edit | Remove `CONF_REPLACEMENTS` and `DEFAULT_REPLACEMENTS` |
| `ha_rebrand/__init__.py` | Edit | Remove replacement handling from config, WebSocket, HTTP endpoints |

### Frontend (JavaScript)
| File | Action | Changes |
|------|--------|---------|
| `ha_rebrand/frontend/ha-rebrand-injector.js` | Edit | Remove `compileReplacements()`, `replaceText()`, `replaceShadowDOMText()`, related calls |
| `ha_rebrand/frontend/ha-rebrand-panel.js` | Edit | Remove replacement UI section, properties, and methods |

### Translations
| File | Action | Changes |
|------|--------|---------|
| `ha_rebrand/strings.json` | Edit | Remove replacement-related strings |
| `ha_rebrand/translations/en.json` | Edit | Remove replacement-related strings |
| `ha_rebrand/translations/zh-Hant.json` | Edit | Remove replacement-related strings |

## Implementation Steps

### Step 1: Update const.py
- Remove `CONF_REPLACEMENTS = "replacements"`
- Remove `DEFAULT_REPLACEMENTS = {}`

### Step 2: Update __init__.py
- Remove `CONF_REPLACEMENTS` from imports
- Remove replacements from config schema (or keep as optional ignored field)
- Remove replacements handling from `async_setup_entry()`
- Remove replacements from WebSocket handlers
- Remove replacements from HTTP endpoint responses
- Remove replacements from config save logic

### Step 3: Update ha-rebrand-injector.js
- Remove `compileReplacements()` function
- Remove `replaceText()` function
- Remove `replaceShadowDOMText()` function
- Remove `this.replacements` and `this.compiledReplacements` properties
- Remove replacement calls from `applyRebrand()`
- Remove `escapeRegExp()` helper if only used for replacements

### Step 4: Update ha-rebrand-panel.js
- Remove `_newReplaceKey` and `_newReplaceValue` properties
- Remove `_addReplacement()` method
- Remove `_removeReplacement()` method
- Remove the entire "Text Replacements" UI section from render template
- Remove replacement-related CSS styles

### Step 5: Update Translation Files
- Remove all keys containing "replacement" from:
  - `strings.json`
  - `translations/en.json`
  - `translations/zh-Hant.json`

### Step 6: Test Backward Compatibility
- Create a test config with replacements defined
- Verify component loads without errors
- Verify other features work correctly

## Verification Plan

1. **Unit Test**: Verify config loads with old replacement entries (no errors)
2. **Manual Test**: Load admin panel and confirm no Text Replacements section
3. **Manual Test**: Verify logo, favicon, sidebar, color features still work
4. **Console Check**: Confirm no JavaScript errors in browser console
5. **Log Check**: Confirm no Python errors in Home Assistant logs

## Estimated Impact

- **Lines Removed**: ~250-300 lines across all files
- **Risk Level**: Low (feature is isolated and unused)
- **Breaking Changes**: None (backward compatible)
