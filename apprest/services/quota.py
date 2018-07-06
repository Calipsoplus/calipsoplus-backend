import logging

from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound

from apprest.models.quota import CalipsoUserQuota
from apprest.models.user import CalipsoUser
from calipsoplus.settings_calipso import MAX_CONTAINER_PER_USER, MAX_RAM_PER_USER, MAX_CPU_PER_USER, \
    MAX_STORAGE_PER_USER


class CalipsoUserQuotaServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_default_quota(self, username):
        self.logger.debug('Getting default quota')
        try:
            user = User.objects.get(username=username)
            calipso_user = CalipsoUser.objects.get(user=user)
            result_quota = CalipsoUserQuota.objects.filter(calipso_user=calipso_user)
            if len(result_quota) == 0:
                self.logger.debug('default quota not found, for user:%s ' % username)
                quota = (CalipsoUserQuota(),)
                quota[0].max_simultaneous = MAX_CONTAINER_PER_USER
                quota[0].memory = MAX_RAM_PER_USER
                quota[0].cpu = MAX_CPU_PER_USER
                quota[0].hdd = MAX_STORAGE_PER_USER
                return quota

            else:
                self.logger.debug('returning quota per username:%s' % username)
                return result_quota

        except Exception as e:
            self.logger.debug('Error to get calipso_user from quota, error:%s' % e)
            raise NotFound


