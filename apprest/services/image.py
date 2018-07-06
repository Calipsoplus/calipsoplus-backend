import logging

from apprest.models.image import CalipsoAvailableImages


class CalipsoAvailableImagesServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_available_image(self, public_name):
        self.logger.debug('Getting one AvailableImage: ' + public_name)
        try:
            selected_image = CalipsoAvailableImages.objects.get(public_name=public_name)
            self.logger.debug('Available image got')
            return selected_image
        except CalipsoAvailableImages.DoesNotExist as e:
            self.logger.debug('Available image %s not found', public_name)
            self.logger.error(e)
            raise e
