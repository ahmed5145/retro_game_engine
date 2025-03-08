# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-03-XX

### Added
- Entity Component System (ECS)
  - Component-based architecture
  - Entity templates and prefabs
  - Event system for entity communication
  - Efficient entity queries

- Scene Management
  - Multiple scene support with transitions
  - Scene persistence
  - Environment variables per scene
  - Camera system with various behaviors

- Enhanced Rendering
  - Layer support with configurable depth
  - Parallax scrolling effects
  - Screen-space effects
  - Batched sprite rendering

- Improved Physics & Collision
  - Rectangle and circle collision detection
  - Spatial partitioning
  - Raycast collision detection
  - Platform physics
  - Collision groups and masks

- Audio System
  - Sound effect and music support
  - Multiple audio channels
  - Volume control
  - Sound priority system

- User Interface
  - Text rendering with bitmap fonts
  - Menu system
  - HUD elements
  - Dialog boxes with text animation
  - Screen-space UI anchoring

### Fixed
- Text animation initialization in UI system
- Collision detection edge cases
- Test class warnings in ECS tests
- Various minor bug fixes and improvements

### Changed
- Improved documentation with comprehensive examples
- Enhanced test coverage (now at 92%)
- Optimized rendering performance
- Refactored component system for better efficiency

### Deprecated
- None

### Removed
- None

## [0.1.0] - 2024-02-XX

### Added
- Initial release
- Basic 2D rendering
- Simple sprite system
- Tile-based map system
- Basic collision detection
- Input handling (keyboard and mouse)
- Basic scene management
- Test framework setup

[0.2.0]: https://github.com/ahmed5145/retro-game-engine/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ahmed5145/retro-game-engine/releases/tag/v0.1.0
