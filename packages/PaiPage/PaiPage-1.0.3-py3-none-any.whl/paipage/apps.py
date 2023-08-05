__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.apps import AppConfig

from .config import configure_final


class PaiPaiConfig(AppConfig):
    name = 'paipage'

    def ready(self):
    	configure_final()
