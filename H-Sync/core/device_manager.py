import os
import importlib

class DeviceManager:
    def __init__(self):
        self.log = {}

    def load(self):
        for folder in os.listdir("plugins"):
            module_name = f"plugins.{folder}.{folder}_driver"
            try:
                module = importlib.import_module(module_name)
                cls = getattr(module, f"{folder.capitalize()}Device")
                for device in cls.discover():
                    self.log[device.name] = device
            except (ModuleNotFoundError, AttributeError):
                continue

    def list_devices(self):
        return list(self.log.keys())

    def get_device(self, name):
        return self.log.get(name)

    def toggle_device(self):
        if not self.log:
            return
        device = next(iter(self.log.values()))
        device.toggle()
