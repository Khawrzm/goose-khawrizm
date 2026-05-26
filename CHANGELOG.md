# Changelog

All notable changes to the Goose × KHAWRIZM Extension.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-05-26

### Added
- ✨ **Professional Interactive Demo** (`demo-pro.html`)
  - Bilingual support (Arabic/English)
  - Tab-based navigation (Intent Processing, EchoWall, Comparison)
  - Advanced animations and visual effects
  - Mobile-responsive design
  - Real-time root extraction with visual feedback

- 📚 **Extended Arabic Roots Database** (50+ roots)
  - New file: `config/arabic_roots_extended.json`
  - 25 action roots (BUILD, WRITE, SENSE, etc.)
  - 10 entity types (home, system, device, etc.)
  - Confidence scores for each mapping
  - Bilingual meanings (Arabic + English)

- 🧠 **SARC Processor Module** (`src/sarc_processor.py`)
  - Advanced trilateral root extraction
  - Diacritic removal
  - Word-to-root indexing
  - Database statistics
  - Singleton pattern for efficiency

- 📡 **EchoWall API Integration** (`src/echowall_api.py`)
  - Multiple connection modes (Simulation, Serial, MQTT, REST)
  - ESP32-S3 hardware support
  - Real-time sensing data
  - Privacy guarantees enforcement
  - Dataclass-based result structure

### Improved
- 🎨 Enhanced demo with better UX
- 📖 Better code organization
- 🔧 Modular architecture

### Technical Details
- Lines of code: 1,500+ → 4,000+
- Modules: 3 → 6
- Database entries: 15 → 50+
- Supported languages: Arabic → Arabic + English

## [0.1.0] - 2026-05-26

### Added
- 🎉 Initial release
- ✅ Basic Arabic intent processing
- ✅ EchoWall simulation
- ✅ Sovereignty verification
- ✅ Zero Big Tech dependencies
- ✅ Complete documentation (Arabic + English)
- ✅ Test suite (15 tests)
- ✅ GitHub Pages site

### Core Features
- `process_arabic_intent()` - Extract trilateral roots
- `sense_environment()` - Simulate EchoWall sensing
- `verify_sovereignty()` - Detect Big Tech dependencies

### Documentation
- README.md (442 lines)
- QUICKSTART.md (Arabic quick start guide)
- LICENSE (Apache 2.0 + Sovereignty clause)

### Infrastructure
- GitHub Actions CI/CD
- Pytest test suite
- Ruff linting
- Type hints with mypy

---

## Links

- **GitHub**: https://github.com/Khawrzm/goose-khawrizm
- **Website**: https://khawrzm.github.io/goose-khawrizm/
- **Parent Project**: https://github.com/Khawrzm/echowall
