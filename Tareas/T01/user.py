class User:
    def __init__(self):
        self.name = None
        self.password = None
        self.resource_id = None

    def set_info(self, name, password, resource_id):
        self.name = name
        self.password = password
        self.resource_id

    def get_resource_id(self):
        return self.resource_id

