import logging


class CalipsoResourceKubernetesService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('CalipsoResourceKubernetesService initialized')

    def run_resource(self, username, experiment, public_name):
        self.logger.debug('CalipsoResourceKubernetesService run_resource')
        return NotImplemented

    def rm_resource(self, resource_name):
        self.logger.debug('CalipsoResourceKubernetesService rm_resource')
        return NotImplemented

    def stop_resource(self, resource_name):
        self.logger.debug('CalipsoResourceKubernetesService stop_resource')
        return NotImplemented

    def list_resources(self, username):
        self.logger.debug('CalipsoResourceKubernetesService list_resources')
        return NotImplemented
