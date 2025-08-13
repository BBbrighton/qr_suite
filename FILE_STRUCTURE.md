# QR Suite File Structure

```
qr_suite/
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI/CD
├── docs/                             # Documentation
│   ├── DYNAMIC_HOOKS_README.md
│   ├── MANUAL_QR_CREATION_GUIDE.md
│   ├── MIGRATION_GUIDE.md
│   ├── QR_LINK_FIXES.md
│   └── TEMPLATE_USAGE_GUIDE.md
├── qr_suite/                         # Main app directory
│   ├── __init__.py
│   ├── __version__.py               # Version info
│   ├── api.py                       # API endpoints
│   ├── boot.py                      # Boot session configuration
│   ├── hooks.py                     # App hooks (dynamic doctype_js)
│   ├── install.py                   # Installation scripts
│   ├── modules.txt                  # Module list
│   ├── patches.txt                  # Database patches
│   ├── tasks.py                     # Scheduled tasks
│   ├── config/                      # App configuration
│   │   ├── __init__.py
│   │   ├── desktop.py              # Desktop icons
│   │   └── qr_suite.py             # Module config
│   ├── patches/                     # Database migrations
│   │   ├── __init__.py
│   │   └── add_qr_link_fields.py
│   ├── public/                      # Static assets
│   │   ├── build.json
│   │   └── js/
│   │       └── qr_suite_doctype.js # DocType integration
│   ├── qr_suite/                    # Module directory
│   │   ├── __init__.py
│   │   ├── modules.txt
│   │   ├── doctype/                # DocTypes
│   │   │   ├── __init__.py
│   │   │   ├── qr_link/
│   │   │   ├── qr_scan_log/
│   │   │   ├── qr_settings/
│   │   │   ├── qr_settings_detail/
│   │   │   └── qr_template/
│   │   ├── report/                 # Reports
│   │   │   ├── __init__.py
│   │   │   ├── qr_scan_analytics/
│   │   │   └── qr_usage_report/
│   │   └── utils/                  # Utility modules
│   │       └── __init__.py
│   ├── templates/                   # Web templates
│   │   ├── __init__.py
│   │   └── pages/
│   │       └── __init__.py
│   ├── utils/                       # App utilities
│   │   ├── __init__.py
│   │   └── qr_code_generator.py
│   └── www/                         # Web pages
│       └── qr/                      # QR redirect handler
│           ├── __init__.py
│           ├── index.html
│           └── index.py
├── scripts/                         # Utility scripts
│   ├── final_cleanup.sh
│   └── migrate_fields.sh
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_changes.py
│   ├── test_dynamic_hooks.py
│   ├── verify_installation.py
│   └── verify_qr_dynamic.py
├── .editorconfig                    # Editor configuration
├── .eslintrc                        # ESLint configuration
├── .gitignore                       # Git ignore rules
├── .pre-commit-config.yaml          # Pre-commit hooks
├── AUTHORS.md                       # Contributors
├── CHANGELOG.md                     # Version history
├── CONTRIBUTING.md                  # Contribution guidelines
├── INSTALL.md                       # Installation guide
├── license.txt                      # MIT License
├── MANIFEST.in                      # Python package manifest
├── package.json                     # NPM package info
├── pyproject.toml                   # Python project config
├── README.md                        # Main documentation
├── requirements.txt                 # Python dependencies
└── setup.py                         # Python setup script
```

## Key Components

### Core Files
- `hooks.py` - Dynamic doctype_js generation
- `api.py` - REST API endpoints
- `qr_code_generator.py` - QR generation logic

### DocTypes
- **QR Link** - Main QR code records
- **QR Template** - Reusable configurations
- **QR Settings** - Global settings and permissions
- **QR Scan Log** - Scan tracking

### Frontend
- `qr_suite_doctype.js` - Universal button injection

### Backend
- Dynamic hooks system
- Template-based generation
- Token and direct URL modes
- Comprehensive API

## Installation Ready
All files required for GitHub installation are included:
- setup.py
- MANIFEST.in
- package.json
- requirements.txt
- __version__.py
