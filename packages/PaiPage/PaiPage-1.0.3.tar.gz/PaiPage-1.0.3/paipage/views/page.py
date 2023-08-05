__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import json

import jinja2

from django.shortcuts import render, render_to_response
from django.views import View
from django.http import Http404

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt

from paipage import config
from paipage.const import PATH_INDEX, HTML_EXT
from paipage.models import Page
from paipage.templating import render_page_full

from .params import Params


class PageView(View):
	def get(self, request, path=PATH_INDEX, lang=None):
		params = Params(request, lang=lang)
		lang = params['lang']

		page = Page.objects.filter(url=path).first()
		if page is None:
			raise Http404

		text = page.get_text(lang)

		if text is None:
			config.logger.error(f'No lang "{lang}" for page "{path}"')
			layout = config.template_layout_default + HTML_EXT
			other_langs = list(page.texts.all())
			params.update({
				'current': page,
				'layout_template': layout,
				'title': config.language_available[params['lang']]['errorNoLang'],
				'description': '',
				'other_langs': other_langs,
			})
			return HttpResponse(params.render_file('ot-nolang'))

		else:
			text.text_full = params.render_str(text.text_full)
			return render_page_full(params, page, text)


@method_decorator(csrf_exempt, name='dispatch')
class PagePreView(View):
	@method_decorator(staff_member_required)
	def post(self, request, ind):
		text = json.loads(request.body.decode('utf-8'))
		params = Params(request)

		page = Page.objects.filter(pk=ind).first()
		if page is None:
			raise Http404

		try:
			text['text_full'] = params.render_str(text['text_full'])
			return render_page_full(params, page, text)
		except jinja2.exceptions.TemplateError as ex:
			params['title'] = 'Template error!'
			params['description'] = repr(ex)
			return HttpResponse(params.render_file('ot-output'))
