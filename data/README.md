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


## Instance Details

Each `data_instance_{port}` folder represents a specific simulated system configured to test different high latency scenarios:

- `data_instance_5001/` — Simulates high latency resulting from elevated system saturation levels.
- `data_instance_5002/` — Simulates high latency caused by excessive system capacity utilization.
- `data_instance_5003/` and `data_instance_5004/` — Represent the source and target systems for simulating high latency due to replication link issues.

These controlled setups facilitate targeted testing of system performance under various latency conditions.

