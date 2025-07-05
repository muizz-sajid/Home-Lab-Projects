from abc import ABC, abstractmethod

class Device(ABC):

    @classmethod
    @abstractmethod
    def discover(cls):
        """used to discover devices"""

    @abstractmethod
    def turn_on(self):
        """to turn the device on"""

    @abstractmethod
    def turn_off(self):
        """to turn the device off"""

    @abstractmethod
    def get_status(self) -> dict:
        """to return the current status"""

    def toggle(self):
        status = self.get_status()
        if status.get("is_active", False):
            self.turn_off()
        else:
            self.turn_on()
