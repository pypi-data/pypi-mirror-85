__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import json

from django.db.models import Count
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from paipage import config
from paipage.config import configure_final
from paipage import const
from paipage.models import Page, GlobalSetting

from .params import Params


class AdminkaPluginsView(View):
	@method_decorator(staff_member_required)
	def get(self, request):
		params = Params(request)
		params.scripted['pluginsInstalled'] = {
			name: config.plugins_installed[name].as_dict()
			for name in config.plugins_installed
		}
		params.scripted['pluginsMeta'] = config.get_plugin_meta_plain()

		params.scripted['template_layout_default'] = config.template_layout_default
		params.scripted['template_page_default'] = config.template_page_default

		params.scripted['page_templates'] = {
			d['template']: d['count']
			for d in Page.objects.values('template').annotate(count=Count('template'))
		}
		params.scripted['layout_templates'] = {
			d['layout']: d['count']
			for d in Page.objects.values('layout').annotate(count=Count('layout'))
		}

		return HttpResponse(params.render_file('am-plugins'))

	@method_decorator(staff_member_required)
	def post(self, request):
		j = json.loads(request.body.decode('utf-8'))

		pluginsMeta = j['pluginsMeta']
		plugins_meta = [
			const.PluginMeta(**kwargs)
			for kwargs in pluginsMeta
		]

		config.plugins_meta = plugins_meta
		GlobalSetting.set_json('plugins_meta', config.get_plugin_meta_plain(), by=request.user)
		configure_final()

		res = {
			'success': True,
			'comment': '-',
		}

		return HttpResponse(json.dumps(res))
