class System:
    def __init__(self, id, name, remote_replication=False, replication_target=None):
        self.id = id
        self.name = name
        self.remote_replication = remote_replication
        self.replication_target = replication_target

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "remote_replication": self.remote_replication,
            "replication_target": self.replication_target
        }


class Node:
    def __init__(self, id, name, system_id):
        self.id = id
        self.name = name
        self.system_id = system_id

    def to_dict(self):
        return {"id": self.id, "name": self.name, "system_id": self.system_id}

class Volume:
    def __init__(self, id, name, system_id):
        self.id = id
        self.name = name
        self.system_id = system_id

    def to_dict(self):
        return {"id": self.id, "name": self.name, "system_id": self.system_id}

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
    def __init__(self, id, system_id, volume_snapshots=None, replication_type="synchronous"):
        self.id = id
        self.system_id = system_id
        self.volume_snapshots = volume_snapshots if volume_snapshots else {}
        self.replication_type = replication_type  # New field

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "volume_snapshots": self.volume_snapshots,
            "replication_type": self.replication_type
        }
