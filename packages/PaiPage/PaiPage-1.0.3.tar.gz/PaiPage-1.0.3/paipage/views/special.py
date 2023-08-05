__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import traceback

from django.http import HttpResponse

from paipage import config, const

from .params import Params

__all__ = [
	'handler404', 'handler500',
]


def handler404(request, *args, **argv):
	params = Params(request)
	layout = config.template_layout_default + const.HTML_EXT
	params.update({
		'layout_template': layout,
		'title': config.language_available[params['lang']]['error404'],
		'description': '',
	})
	return HttpResponse(params.render_file('ot-output'), status=404)


def handler500(request, *args, **argv):
	params = Params(request)
	layout = config.template_layout_default + const.HTML_EXT
	params.update({
		'layout_template': layout,
		'title': config.language_available[params['lang']]['error500'],
		'description': '',
	})
	return HttpResponse(params.render_file('ot-output'), status=500)
