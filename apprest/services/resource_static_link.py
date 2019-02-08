import logging


class CalipsoResourceStaticLinkService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('CalipsoResourceStaticLinkService initialized')

    def run_resource(self, username, experiment, public_name):
        self.logger.debug('CalipsoResourceStaticLinkService run_resource')
        return NotImplemented

    def rm_resource(self, resource_name):
        self.logger.debug('CalipsoResourceStaticLinkService rm_resource')
        return NotImplemented

    def stop_resource(self, resource_name):
        self.logger.debug('CalipsoResourceStaticLinkService stop_resource')
        return NotImplemented

    def list_resources(self, username):
        self.logger.debug('CalipsoResourceStaticLinkService list_resources')
        return NotImplemented
