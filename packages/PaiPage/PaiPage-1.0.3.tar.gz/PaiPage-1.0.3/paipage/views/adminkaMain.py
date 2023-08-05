__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import json

from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from paipage import config

from .params import Params


class AdminkaMainView(View):
	@method_decorator(staff_member_required)
	def get(self, request):
		params = Params(request)
		params['site_name'] = config.site_name
		params['debug'] = settings.DEBUG
		return HttpResponse(params.render_file('am-main'))
