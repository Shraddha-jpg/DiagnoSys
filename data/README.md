# Data Directory

This folder contains all runtime and generated data for the project.

## Structure

- `global_systems.json` — Tracks all systems across instances.
- `global_logs.txt` — Aggregated logs from all instances.
- `data_instance_{port}/` — Per-instance data folders (metrics, logs, configs).

## Guidelines

- Do not manually edit files in this folder.
- Clean up old data using the `clear.py` utility if needed.
- Back up important data before running destructive operations.

## Example

```
data/
  global_systems.json
  global_logs.txt
  data_instance_5001/
    system.json
    volume.json
    ...
``` 