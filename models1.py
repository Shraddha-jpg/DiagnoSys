class System:
    def __init__(self, id, name, max_throughput=200, max_capacity=1024, saturation=0, cpu_usage=0, 
                 remote_replication=False, replication_target=None):
        self.id = id
        self.name = name
        self.max_throughput = max_throughput  # MBPS
        self.max_capacity = max_capacity      # GB
        self.saturation = saturation  # System saturation percentage
        self.cpu_usage = cpu_usage    # CPU usage percentage
        self.remote_replication = remote_replication  # Remote replication flag
        self.replication_target = replication_target  # Target system for replication

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "max_throughput": self.max_throughput,
            "max_capacity": self.max_capacity,
            "saturation": self.saturation,
            "cpu_usage": self.cpu_usage,
            "remote_replication": self.remote_replication,
            "replication_target": self.replication_target
        }


class Volume:
    def __init__(self, id, name, system_id, size=0, is_exported=False, exported_host_id=None, workload_size=0, 
                 snapshot_settings=None, snapshot_frequencies=None, replication_settings=None):
        self.id = id
        self.name = name
        self.system_id = system_id
        self.size = size  # Size in GB
        self.is_exported = is_exported
        self.exported_host_id = exported_host_id
        self.workload_size = workload_size

        # ✅ Merge: Store snapshot settings & multiple snapshot frequencies
        self.snapshot_settings = snapshot_settings or {}  # Dictionary
        self.snapshot_frequencies = snapshot_frequencies if snapshot_frequencies else []  # List

        # ✅ Merge: Use list format for replication settings
        self.replication_settings = replication_settings or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "system_id": self.system_id,
            "size": self.size,
            "is_exported": self.is_exported,
            "exported_host_id": self.exported_host_id,
            "workload_size": self.workload_size,
            "snapshot_settings": self.snapshot_settings,
            "snapshot_frequencies": self.snapshot_frequencies,  # ✅ Updated
            "replication_settings": self.replication_settings
        }


class Host:
    def __init__(self, id, system_id, name, application_type, protocol):
        self.id = id
        self.system_id = system_id
        self.name = name
        self.application_type = application_type
        self.protocol = protocol

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "name": self.name,
            "application_type": self.application_type,
            "protocol": self.protocol
        }


class Settings:
    def __init__(self, id, system_id, name=None, type=None, value=None, volume_snapshots=None,
                 replication_type="synchronous", replication_target=None, replication_frequency=None, delay_sec=0):
        self.id = id
        self.system_id = system_id
        self.name = name
        self.type = type

        # ✅ Merge: Store multiple snapshot frequencies per volume
        self.volume_snapshots = volume_snapshots if volume_snapshots else {}

        # ✅ Merge: Ensure replication settings are handled properly
        self.replication_type = replication_type  # 'synchronous' or 'asynchronous'
        self.replication_target = replication_target
        self.replication_frequency = replication_frequency
        self.delay_sec = delay_sec  # 0 for sync, >0 for async

        # ✅ Preserve old setting value handling
        self.value = value if type != "replication" else None

    def to_dict(self):
        data = {
            "id": self.id,
            "system_id": self.system_id,
            "name": self.name,
            "type": self.type,
            "volume_snapshots": self.volume_snapshots,  # ✅ Updated
            "replication_type": self.replication_type,
            "replication_target": self.replication_target,
            "replication_frequency": self.replication_frequency,
            "delay_sec": self.delay_sec
        }

        if self.type != "replication":
            data["value"] = self.value
            
        return data
