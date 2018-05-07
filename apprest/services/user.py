import logging

from apprest.models.user import CalipsoUser


class CalipsoUserServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)