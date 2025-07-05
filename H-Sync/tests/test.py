from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import logging
import time

logging.basicConfig(level=logging.DEBUG)

class MyListener(ServiceListener):
    def add_service(self, zc, type, name):
        print("Service discovered:", name)

    def update_service(self, zc, type, name):
        pass

    def remove_service(self, zc, type, name):
        pass

zc = Zeroconf()
browser = ServiceBrowser(zc, "_googlecast._tcp.local.", MyListener())

time.sleep(10)
zc.close()