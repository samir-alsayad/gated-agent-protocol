# Intent: CLI File Organizer

## Context
A command-line tool that automatically organizes files in a directory based on file type, date, or custom rules. Designed for users who accumulate downloads or project files and need a quick way to restore order.

## Goals
- **G-01**: Provide a single command to sort files into categorized subdirectories.
- **G-02**: Support customizable rules via a configuration file.
- **G-03**: Ensure no data loss—never overwrite or delete files silently.

## Constraints
- **C-01**: WHEN the tool encounters a file type not in the config, THE system SHALL move it to an `unsorted/` directory.
- **C-02**: IF a file with the same name exists in the target directory, THEN THE system SHALL append a timestamp suffix rather than overwriting.
- **C-03**: WHEN the `--dry-run` flag is provided, THE system SHALL print the proposed changes without executing them.
- **C-04**: THE system SHALL log all file movements to a `organizer.log` file in the target directory.
