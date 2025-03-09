
import json
import os

class StorageManager:
    def __init__(self, data_dir, global_file="global_systems.json"):
        self.data_dir = data_dir
        self.global_file = global_file
        os.makedirs(data_dir, exist_ok=True)

        if not os.path.exists(self.global_file) or os.stat(self.global_file).st_size == 0:
            with open(self.global_file, "w") as f:
                json.dump([], f, indent=4)

    def load_resource(self, resource_type):
        file_path = os.path.join(self.data_dir, f"{resource_type}.json")
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f, indent=4)
            return []

        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_resource(self, resource_type, data):
        file_path = os.path.join(self.data_dir, f"{resource_type}.json")
        existing_data = self.load_resource(resource_type)

        if any(item["id"] == data["id"] for item in existing_data):
            raise ValueError(f"{resource_type} with ID {data['id']} already exists.")

        existing_data.append(data)
        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

    def add_system_to_global(self, system_id, system_name, port):
        with open(self.global_file, "r") as f:
            global_systems = json.load(f)

        if any(s["id"] == system_id for s in global_systems):
            return
        
        global_systems.append({"id": system_id, "name": system_name, "port": port})
        with open(self.global_file, "w") as f:
            json.dump(global_systems, f, indent=4)

    def get_all_systems(self):
        with open(self.global_file, "r") as f:
            return json.load(f)

    def update_resource(self, resource_type, resource_id, updated_data):
        file_path = os.path.join(self.data_dir, f"{resource_type}.json")
        existing_data = self.load_resource(resource_type)
        for i, item in enumerate(existing_data):
            if item["id"] == resource_id:
                existing_data[i] = updated_data
                break
        try:
            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)
        except Exception as e:
            raise Exception(f"Failed to update {resource_type}: {str(e)}")

    def delete_resource(self, resource_type, resource_id):
        file_path = os.path.join(self.data_dir, f"{resource_type}.json")
        existing_data = self.load_resource(resource_type)
        if resource_id is None:
            existing_data = []
        else:
            existing_data = [item for item in existing_data if item["id"] != resource_id]
        try:
            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)
        except Exception as e:
            raise Exception(f"Failed to delete {resource_type}: {str(e)}")

class Settings:
    def __init__(self, id, system_id, snapshot_frequency=None):
        self.id = id
        self.system_id = system_id
        self.snapshot_frequency = snapshot_frequency  # Frequency in minutes/hours/days

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            "snapshot_frequency": self.snapshot_frequency
        }
