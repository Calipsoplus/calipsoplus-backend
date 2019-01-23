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
            result_quota = CalipsoUserQuota.objects.get(calipso_user=calipso_user)
            if not result_quota:
                self.logger.debug('Default quota not found, for user:%s ' % username)

                quota = CalipsoUserQuota()
                quota.max_simultaneous = MAX_CONTAINER_PER_USER
                quota.memory = MAX_RAM_PER_USER
                quota.cpu = MAX_CPU_PER_USER
                quota.hdd = MAX_STORAGE_PER_USER
                quota.calipso_user = calipso_user
                quota.save()

                return quota
            else:
                self.logger.debug('Returning quota for username:%s' % username)
                return result_quota

        except Exception as e:
            self.logger.debug('Error to get calipso_user from quota, error:%s' % e)
            raise NotFound

    def change_user_quota(self, username, max_simulations, memory, cpu, hdd):
        self.logger.debug('Modifying default quota')
        try:
            user = User.objects.get(username=username)
            calipso_user = CalipsoUser.objects.get(user=user)
            result_quota = CalipsoUserQuota.objects.get(calipso_user=calipso_user)

            result_quota.max_simultaneous = max_simulations
            result_quota.memory = memory
            result_quota.cpu = cpu
            result_quota.hdd = hdd
            result_quota.save()

            self.logger.debug('Quota updated for username:%s' % username)

        except Exception as e:
            self.logger.debug('Error to get calipso_user from quota, error:%s' % e)
            raise NotFound


