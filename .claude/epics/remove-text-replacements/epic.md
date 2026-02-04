---
name: remove-text-replacements
status: completed
created: 2026-02-04T08:57:20Z
updated: 2026-02-04T09:18:53Z
progress: 100%
prd: .claude/prds/remove-text-replacements.md
github: [Will be updated when synced to GitHub]
---

# Epic: Remove Text Replacements Feature

## Overview

Remove the unused Text Replacements functionality from the Ha_rebrand custom component. This is a straightforward deletion task - no new code needs to be written. The goal is to simplify the codebase by removing ~250-300 lines of code while maintaining backward compatibility with existing configurations.

## Architecture Decisions

- **Silent ignore pattern**: Keep config schema flexible to silently ignore `replacements` entries in existing configs rather than rejecting them
- **No feature flags**: Complete removal rather than feature toggle (feature is confirmed unused)
- **Atomic removal**: All removal done in single pass to avoid partial states

## Technical Approach

### Backend Changes (Python)
- Remove constants from `const.py`
- Remove WebSocket and HTTP endpoint handling from `__init__.py`
- Ensure config loader doesn't fail on existing `replacements` entries

### Frontend Changes (JavaScript)
- Remove DOM manipulation functions from `ha-rebrand-injector.js`
- Remove UI section and associated methods from `ha-rebrand-panel.js`

### Translations
- Remove all replacement-related strings from JSON files

## Implementation Strategy

1. Start with backend (Python) to remove the data layer
2. Update frontend (JavaScript) to remove UI and logic
3. Clean up translations
4. Test backward compatibility

## Task Breakdown Preview

- [x] Task 1: Remove backend code (const.py + __init__.py)
- [x] Task 2: Remove injector functions (ha-rebrand-injector.js)
- [x] Task 3: Remove panel UI and methods (ha-rebrand-panel.js)
- [x] Task 4: Remove translation strings (all JSON files)
- [x] Task 5: Verify backward compatibility

## Dependencies

- None - this is a self-contained removal with no external dependencies

## Success Criteria (Technical)

- Admin panel loads without Text Replacements section
- No JavaScript errors in browser console
- No Python errors in Home Assistant logs
- Existing configs with `replacements` entries load without errors
- All other features (logo, favicon, colors, sidebar) continue working
- ~250-300 lines of code removed

## Estimated Effort

- **Total tasks**: 5
- **Complexity**: Low (pure deletion, no new logic)
- **Risk**: Low (isolated feature, backward compatible)
- **Critical path**: Backend removal must precede frontend testing

## Tasks Created

- [x] 001.md - Remove backend replacement code (commit: 16d6877)
- [x] 002.md - Remove injector replacement functions (commit: 2fcc922)
- [x] 003.md - Remove panel UI and methods (commit: f8d0b3e)
- [x] 004.md - Remove translation strings (commit: e1d8c5b)
- [x] 005.md - Verify backward compatibility (all checks passed)

Total tasks: 5
Completed: 5/5
Lines removed: ~304 from production code
