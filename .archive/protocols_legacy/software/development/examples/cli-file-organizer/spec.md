# Specification: CLI File Organizer

## Architecture
```
cli-file-organizer/
├── main.py           # Entry point, CLI argument parsing
├── organizer.py      # Core logic for file categorization
├── config.py         # Config file loader
└── logger.py         # File movement logging
```

## Properties
- **P-01**: The tool SHALL be idempotent—running it twice on the same directory produces the same result.
- **P-02**: The tool SHALL NOT modify files outside the specified target directory.
- **P-03**: All file operations SHALL be atomic—a crash mid-operation leaves no partial state.
- **P-04**: The config file format SHALL be YAML with a documented schema.

## Dependencies
- Python 3.9+
- PyYAML for config parsing
- No external file system libraries (stdlib only)
