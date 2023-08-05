__title__ = 'PaiPaige Simple plugin'
__version__ = '1.0'
__license__ = 'GPL-3.0'
__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'
description = 'Provides simple yet handy templates.'

import json

import cachetools

from django.shortcuts import get_object_or_404

from paipage import TemplateHandler
from paipage.models import Page


class PgLabeled(TemplateHandler):
	form_elements = [
		{
			'type': 'str',
			'max_len': '32',
			'code': 'label',
			'name': 'Label',
		}, {
			'type': 'str',
			'max_len': '128',
			'code': 'tags',
			'name': 'Tags',
			# TODO: add PAF type "words" to remove bad symbols
		},
	]

	def get_short(self):
		result = self.text.text_short
		label = self.page.other_settings_.get('label', '')
		if len(label) > 0:
			result += f'<br>{label}'
		return result


class PgNested(TemplateHandler):
	@staticmethod
	@cachetools.cached(cache=cachetools.TTLCache(maxsize=16, ttl=10))
	def get_children_for(page):
		cluster_settings = json.loads(page.other_settings)
		target = cluster_settings.get('target', None)
		if target is None:
			target = page
		else:
			target = get_object_or_404(Page, pk=target)

		# TODO: Filter by lang
		result = list(target.children.all())

		# Filter by tags if set
		embrace = lambda x: f' {x} '
		tags = cluster_settings.get('tags', '')
		tags = [embrace(tag) for tag in tags.split(' ') if len(tag) > 0]
		for tag in tags:
			result = [
				pg for pg in result
				if tag in embrace(pg.other_settings_.get('tags', ''))
			]

		# Order by label
		result.sort(
			reverse=cluster_settings.get('desc', True),
			key=lambda pg: pg.other_settings_.get('label', '')
		)

		# Limit by count
		count = cluster_settings.get('count', 0)
		if count > 0:
			result = result[:count]

		return result

	def should_show(self):
		return len(self.get_children()) > 0


class PgCluster(PgNested):
	form_elements = [
		{
			'type': 'select',
			'subtype': 'page',
			'allow_clear': True,
			'code': 'target',
			'name': 'Target page cluster',
		}, {
			'type': 'str',
			'max_len': '128',
			'code': 'tags',
			'name': 'Tags filter',
			# TODO: add PAF type "words" to remove bad symbols
		}, {
			'type': 'int',
			'min': '0',
			'code': 'count',
			'name': 'Max count',
			'desc': '0 value means no limit',
		}, {
			'type': 'bool',
			'code': 'desc',
			'name': 'Label order',
			'on': 'descending',
			'off': 'ascending',
			'default': True,
		},
	]


class PgContents(PgNested):

	def get_short(self):
		self.params.update({
			'children': list(self.page.children.all()),
		})
		text = ''
		if len(self.text.text_short) > 1:
			text = self.text.text_short

		template = f'''
{{% import "_utils.html" as utils with context %}}
{{{{ utils.page_contents(children, 2) }}}}
{text}
'''
		return self.params.render_str(template)


template_handlers = {
	'pg-usual': PgLabeled,
	'pg-cluster': PgCluster,
	'pg-contents': PgContents,
}
