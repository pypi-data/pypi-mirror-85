from . import IaaS


class NoneIaas(IaaS):
    @classmethod
    def connect(cls, url, config):
        return cls()

    def list_machines(self):
        return []
