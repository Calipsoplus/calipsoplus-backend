import logging

from apprest.models.facilities import CalipsoFacility


class CalipsoFacilityServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all_facilities(self):

        self.logger.debug('Getting all facilities')
        try:
            all_facilities = CalipsoFacility.objects.all()
            self.logger.debug('All application facilities got')
            return all_facilities
        except Exception as e:
            self.logger.error(e)
            raise e


