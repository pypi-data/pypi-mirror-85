__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from django.contrib import admin
from . import models

for el in models.__all__:
	admin.site.register(getattr(models, el))
