---
name: remove-text-replacements
status: backlog
created: 2026-02-04T08:57:20Z
progress: 0%
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

- [ ] Task 1: Remove backend code (const.py + __init__.py)
- [ ] Task 2: Remove injector functions (ha-rebrand-injector.js)
- [ ] Task 3: Remove panel UI and methods (ha-rebrand-panel.js)
- [ ] Task 4: Remove translation strings (all JSON files)
- [ ] Task 5: Verify backward compatibility

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

- [ ] 001.md - Remove backend replacement code (parallel: false)
- [ ] 002.md - Remove injector replacement functions (parallel: true, depends_on: 001)
- [ ] 003.md - Remove panel UI and methods (parallel: true, depends_on: 001)
- [ ] 004.md - Remove translation strings (parallel: true)
- [ ] 005.md - Verify backward compatibility (parallel: false, depends_on: 001-004)

Total tasks: 5
Parallel tasks: 3 (002, 003, 004 can run concurrently after 001)
Sequential tasks: 2 (001 first, 005 last)
Estimated total effort: 5-7.5 hours
