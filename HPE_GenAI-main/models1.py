class System:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }



class Node:
    def __init__(self, id, name, system_id):
        self.id = id
        self.name = name
        self.system_id = system_id

    def to_dict(self):
        return {"id": self.id, "name": self.name, "system_id": self.system_id}

# In models1.py
class Volume:
    def __init__(self, id, name, system_id, is_exported=False, exported_host_id=None, workload_size=0, snapshot_settings=None, replication_settings=None):
        self.id = id
        self.name = name
        self.system_id = system_id
        self.is_exported = is_exported
        self.exported_host_id = exported_host_id
        self.workload_size = workload_size
        self.snapshot_settings = snapshot_settings or {}
        self.replication_settings = replication_settings or {}

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "system_id": self.system_id,
            "is_exported": self.is_exported,
            "exported_host_id": self.exported_host_id,
            "workload_size": self.workload_size,
            "snapshot_settings": self.snapshot_settings,
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


# In models1.py
class Settings:
    def __init__(self, id, system_id, name, type, value):
        self.id = id
        self.system_id = system_id
        self.name = name
        self.type = type
        self.value = value

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "name": self.name,
            "type": self.type,
            "value": self.value
        }
