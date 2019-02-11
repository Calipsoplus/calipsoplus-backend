import logging


class CalipsoResourceVirtualMachineService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('CalipsoResourceVirtualMachineService initialized')

    def run_resource(self, username, experiment, public_name):
        self.logger.debug('CalipsoResourceVirtualMachineService run_resource')
        return NotImplemented

    def rm_resource(self, resource_name):
        self.logger.debug('CalipsoResourceVirtualMachineService rm_resource')
        return NotImplemented

    def stop_resource(self, resource_name):
        self.logger.debug('CalipsoResourceVirtualMachineService stop_resource')
        return NotImplemented

    def list_resources(self, username):
        self.logger.debug('CalipsoResourceVirtualMachineService list_resources')
        return NotImplemented
