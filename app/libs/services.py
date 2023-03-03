class Services:
    def __init__(self):
        self.__services = {}

    def register(self, key, service_instance):
        self.__services[key] = service_instance

    def get(self, key):
        return self.__services[key]


services = Services()
