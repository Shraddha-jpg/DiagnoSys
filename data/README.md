<h1 align="center">Data Directory </h1>

This folder contains all runtime and generated data for the project.

## Structure

- `global_systems.json` — Tracks all systems across instances.
- `global_logs.txt` — Aggregated logs across all instances.
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
    ├── host.json
    ├── io_metrics.json
    ├── logs_5001.txt
    ├── replication_metrics.json
    ├── settings.json
    ├── snapshot_log.txt
    ├── snapshots.json
    ├── system_metrics.json
    ├── system.json
    └── volume.json
``` 
