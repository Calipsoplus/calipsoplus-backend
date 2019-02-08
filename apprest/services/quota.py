import logging

from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound

from apprest.models.quota import CalipsoUserQuota
from apprest.models.user import CalipsoUser
from apprest.services.container import CalipsoContainersServices
from apprest.services.image import CalipsoAvailableImagesServices
from apprest.utils.exceptions import QuotaMaxSimultaneousExceeded, QuotaCpuExceeded, QuotaMemoryExceeded, \
    QuotaHddExceeded
from calipsoplus.settings_calipso import MAX_RESOURCES_PER_USER, MAX_RAM_PER_USER, MAX_CPU_PER_USER, \
    MAX_STORAGE_PER_USER


image_service = CalipsoAvailableImagesServices()
container_service = CalipsoContainersServices()


class CalipsoUserQuotaServices:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_default_quota(self, username):
        self.logger.debug('Getting default quota')
        try:
            user = User.objects.get(username=username)
            calipso_user = CalipsoUser.objects.get(user=user)
            try:
                result_quota = CalipsoUserQuota.objects.get(calipso_user=calipso_user)
                return result_quota

            except CalipsoUserQuota.DoesNotExist as e:
                self.logger.debug(
                    'Default quota for user:%s, not found, we will use default settings' % username)

                quota = CalipsoUserQuota()
                quota.max_simultaneous = MAX_RESOURCES_PER_USER
                quota.memory = MAX_RAM_PER_USER
                quota.cpu = MAX_CPU_PER_USER
                quota.hdd = MAX_STORAGE_PER_USER

                return quota

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

    def calculate_available_quota(self, username):
        self.logger.debug('CalipsoResourceDockerContainerService run_resource')
        max_simultaneous = 0
        max_cpu = 0
        max_memory = 0
        max_hdd = 0

        list_of_containers = container_service.list_container(username=username)

        for container in list_of_containers:
            image = image_service.get_available_image(public_name=container.public_name)
            max_simultaneous += 1
            max_cpu += image.cpu
            max_memory += int(image.memory[:-1])
            max_hdd += int(image.hdd[:-1])
            self.logger.debug("container with public_name=%s" % container.public_name)

        quota_per_user = self.get_default_quota(username=username)
        self.logger.debug("num_containers_per_user = %d" % len(list_of_containers))
        self.logger.debug(
            'user:%s used:%d quota.max:%d' % (username, max_simultaneous, quota_per_user.max_simultaneous))
        self.logger.debug('user:%s cpu_used:%d > quota.max_cpu:%d' % (username, max_cpu, quota_per_user.cpu))
        self.logger.debug(
            'user:%s max_ram_used:%dG > quota_user.max_ram:%s' % (username, max_memory, quota_per_user.memory))
        self.logger.debug('user:%s max_hdd:%dG quota.max_hdd:%s' % (username, max_hdd, quota_per_user.hdd))
        if max_simultaneous >= quota_per_user.max_simultaneous:
            self.logger.warning(
                'user:%s used:%d > quota.max:%d' % (username, max_simultaneous, quota_per_user.max_simultaneous))
            raise QuotaMaxSimultaneousExceeded("Max machines exceeded")
        if max_cpu >= quota_per_user.cpu:
            self.logger.warning('user:%s cpu_used:%d > quota.max_cpu:%d' % (username, max_cpu, quota_per_user.cpu))
            raise QuotaCpuExceeded("Max cpus exceeded")
        if max_memory >= int(quota_per_user.memory[:-1]):
            self.logger.warning(
                'user:%s max_ram_used:%dG > quota_user.max_ram:%s' % (username, max_memory, quota_per_user.memory))
            raise QuotaMemoryExceeded("Max memory exceeded")
        if max_hdd >= int(quota_per_user.hdd[:-1]):
            self.logger.warning('user:%s max_hdd:%dG quota.max_hdd:%s' % (username, max_hdd, quota_per_user.hdd))
            raise QuotaHddExceeded("Max hdd exceeded")
