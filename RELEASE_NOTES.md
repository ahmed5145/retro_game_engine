# Release Notes

## Version 0.1.2 (2025-03-08)

### Bug Fixes
- Fixed text animation initialization in UI system
  - Text animation progress now correctly resets when text is updated
  - Animation speed changes now properly update animation state
- Fixed collision detection edge cases
  - Corrected penetration depth calculations for all collision directions
  - Improved accuracy of collision normal determination
  - Fixed right and bottom collision handling

### Improvements
- Improved test coverage to 92%
- Removed pytest collection warnings
- Enhanced code organization and readability
- Added comprehensive documentation
  - Updated README.md with features, installation, and usage guides
  - Added CHANGELOG.md to track version history
  - Improved inline code documentation

### Known Issues
- None

### Upgrading
No breaking changes were introduced in this release. Users can safely upgrade from version 0.1.1.
