# GAP CLI Reference

The `gap` command line interface is the primary way to interact with the Gated Agent Protocol.

## Global Options
*   `--help`: Show help message.

## Commands

### `gap check`
Validates the status of a project against its manifest.

```bash
gap check status [MANIFEST_PATH]
```

### `gap scribe`
Generates artifacts from templates.

```bash
gap scribe create [STEP_NAME] --manifest [MANIFEST_PATH]
```
*   `--force`: Bypass state checks (useful for testing).
*   `--dry-run`: Print output to stdout instead of writing file.

### `gap gate`
Manages approval workflows.

```bash
gap gate list
gap gate approve [STEP_NAME]
```
