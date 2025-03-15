
import json
import os
import uuid
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
    
    def remove_system_from_global(self, system_id):
        """Removes a system from global_systems.json when deleted."""
        try:
            with open(self.global_file, "r") as f:
                global_systems = json.load(f)

            # Remove the system with the matching ID
            updated_systems = [sys for sys in global_systems if sys["id"] != system_id]

            with open(self.global_file, "w") as f:
                json.dump(updated_systems, f, indent=4)

            print(f"✅ System {system_id} removed from global_systems.json")

        except Exception as e:
            raise Exception(f"❌ Failed to remove system from global tracking: {str(e)}")
    def delete_related_resources(self, resource_type, system_id):
        """Deletes all resources (nodes, volumes, settings) associated with a system."""
        file_path = os.path.join(self.data_dir, f"{resource_type}.json")
        existing_data = self.load_resource(resource_type)

        # Keep only resources that DO NOT belong to the deleted system
        updated_data = [item for item in existing_data if item["system_id"] != system_id]

        try:
            with open(file_path, "w") as f:
                json.dump(updated_data, f, indent=4)

            print(f"✅ All {resource_type} related to system {system_id} deleted.")

        except Exception as e:
            raise Exception(f"❌ Failed to delete {resource_type} for system {system_id}: {str(e)}")
        
    def update_snapshot_in_settings(self, system_id, volume_id, snapshot_frequency):
        """Ensures snapshot settings for the volume are stored in settings.json."""
        file_path = os.path.join(self.data_dir, "settings.json")

        # If settings.json does not exist, create it
        if not os.path.exists(file_path):
            print("⚠️ settings.json does not exist, creating a new file...")
            with open(file_path, "w") as f:
                json.dump([], f, indent=4)

        settings = self.load_resource("settings")

        # Find or create the system settings entry
        system_setting = next((s for s in settings if s["system_id"] == system_id), None)

        if not system_setting:
            print(f"⚠️ No settings found for system {system_id}, creating a new entry.")
            system_setting = {
                "id": str(uuid.uuid4()),  # Generate a unique settings ID
                "system_id": system_id,
                "volume_snapshots": {}  # Initialize snapshot tracking
            }
            settings.append(system_setting)  # Add new settings entry

        # Update snapshot settings for the specific volume
        system_setting["volume_snapshots"][volume_id] = snapshot_frequency
        print(f"✅ Updated settings: {settings}")

        # Save changes back to settings.json
        try:
            with open(file_path, "w") as f:
                json.dump(settings, f, indent=4)
            print(f"✅ Snapshot settings updated successfully for volume {volume_id} in system {system_id}")

        except Exception as e:
            raise Exception(f"❌ Failed to update snapshot settings in settings.json: {str(e)}")
    
    def update_replication_in_settings(self, system_id, remote_replication, replication_target):
        """Updates remote replication settings in settings.json."""
        settings = self.load_resource("settings")

        # Find the system settings entry
        system_setting = next((s for s in settings if s["system_id"] == system_id), None)

        if not system_setting:
            # If no settings exist for this system, create one
            system_setting = {
                "id": str(uuid.uuid4()),
                "system_id": system_id,
                "remote_replication": False,
                "replication_target": None
            }
            settings.append(system_setting)

        # Update replication settings
        system_setting["remote_replication"] = remote_replication
        system_setting["replication_target"] = replication_target

        # Save changes
        try:
            file_path = os.path.join(self.data_dir, "settings.json")
            with open(file_path, "w") as f:
                json.dump(settings, f, indent=4)

            print(f"✅ Replication settings updated for system {system_id}")

        except Exception as e:
            raise Exception(f"❌ Failed to update replication settings in settings.json: {str(e)}")




class Settings:
    def __init__(self, id, system_id):
        self.id = id
        self.system_id = system_id
        

    def to_dict(self):
        return {
            "id": self.id,
            "system_id": self.system_id,
            
        }
