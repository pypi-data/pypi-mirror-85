__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import json

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from paipage import config
from paipage.const import LANG_NO
from paipage.models import Page, PageText

from .params import Params


class AdminkaStructureView(View):
	@method_decorator(staff_member_required)
	def get(self, request):
		params = Params(request)
		params.scripted['all_pages'] = Page.get_all()
		params.scripted['language_selectable'] = list(config.language_available.keys())
		params.scripted['default_page'] = config.template_page_default
		params.scripted['default_layout'] = config.template_layout_default
		params.scripted['handler_forms'] = {
			key: handler.form_elements
			for key, handler in config.template_handlers.items()
			if handler.form_elements is not None
		}
		params.selectables['template_layout'] = config.template_layout_list
		params.selectables['template_page'] = config.template_page_list
		return HttpResponse(params.render_file('am-struct'))


@method_decorator(csrf_exempt, name='dispatch')
class AdminkaPageView(View):
	@method_decorator(staff_member_required)
	def get(self, request, pk):
		params = Params(request)
		page = get_object_or_404(Page, pk=pk)
		texts = [t.as_dict() for t in page.texts.all()]
		params.scripted['the_page'] = page.as_dict()
		params.scripted['texts'] = {t['language']: t for t in texts}
		params.scripted['language_selectable'] = list(config.language_available.keys())
		params.scripted['default_page'] = config.template_page_default
		params.scripted['default_layout'] = config.template_layout_default
		params.scripted['handler_forms'] = {
			key: handler.form_elements
			for key, handler in config.template_handlers.items()
			if handler.form_elements is not None
		}
		params.selectables['language'] = params.scripted['language_selectable'] + [LANG_NO]
		params.selectables['template_layout'] = config.template_layout_list
		params.selectables['template_page'] = config.template_page_list
		return HttpResponse(params.render_file('am-page'))

	@method_decorator(staff_member_required)
	def post(self, request, pk=-1):
		j = json.loads(request.body.decode('utf-8'))
		if pk == -1:
			page = Page(created_by=request.user)
		else:
			page = get_object_or_404(Page, pk=pk)

		res = {
			'success': True,
			'comment': '-',
		}

		if res['success']:
			new_url = j['url']
			if new_url != page.url:
				other = Page.objects.filter(url=new_url).first()
				if other is not None:
					res['success'] = False
					res['comment'] = 'The address is already in use'
				else:
					page.url = new_url

		if res['success']:
			new_upper = j['upper']
			if new_upper is not None:
				new_upper = int(new_upper)
			print(f'Upper new: {new_upper}, old: {page.upper}')
			if new_upper != page.upper:
				if new_upper == pk:
					res['success'] = False
					res['comment'] = 'Cannot link page to itself'
				if new_upper is not None:
					temp_upper = new_upper
					while True:
						if temp_upper is None:
							break
						temp = get_object_or_404(Page, pk=temp_upper)
						if temp.upper:
							temp_upper = temp.upper.pk
						else:
							break
						if temp_upper == new_upper:
							break  # prevent looping
						if pk == temp_upper:
							res['success'] = False
							res['comment'] = 'Cannot link page to itself'
				if new_upper is None:
					page.upper = None
				else:
					page.upper = get_object_or_404(Page, pk=new_upper)

		if res['success']:
			page.layout = j['template_layout']
			page.layout = '' if page.layout is None else page.layout
			page.template = j['template_page']
			page.template = '' if page.template is None else page.template
			if 'other_settings' in j:
				page.other_settings = json.dumps(j['other_settings'])
			else:
				page.other_settings = '{}'

		if res['success']:
			page.updated_by = request.user
			page.save()
			res['obj'] = page.as_dict()

		return HttpResponse(json.dumps(res))


@method_decorator(csrf_exempt, name='dispatch')
class AdminkaPageTextView(View):
	@method_decorator(staff_member_required)
	def post(self, request, pk, lang):
		# `lang` is old lang, it may be changed
		j = json.loads(request.body.decode('utf-8'))
		page = get_object_or_404(Page, pk=pk)
		text = page.get_text(lang)

		res = {
			'success': True,
			'comment': '-',
		}

		if text is None:
			text = PageText(page=page, created_by=request.user, language=j['language'])
		elif lang != j['language']:
			existing = PageText.objects.filter(page=page, language=j['language']).first()
			if existing is not None:
				res['success'] = False
				res['comment'] = 'Cannot replace existing text language'
			else:
				text.language = j['language']

		if res['success']:
			text.title = j['title']
			text.keywords = j['keywords']
			text.description = j['description']
			text.text_short = j['text_short']
			text.text_full = j['text_full']
			text.updated_by = request.user
			text.save()

		return HttpResponse(json.dumps(res))
