__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

from jinja2 import Environment, FileSystemLoader


def safe_json(input):
	return input.replace('</script>', '<\\/script>')


def page_by_url(path):
	from paipage.models import Page
	page = Page.objects.filter(url=path).first()
	if page is None:
		raise ValueError(f'Missing page_by_url("{path}")')
	return page


def make_env(template_dirs, config):
	env = Environment(loader=FileSystemLoader(template_dirs))
	env.filters['safe_json'] = safe_json
	env.globals.update({
		'config': config,
		'page_by_url': page_by_url,
	})
	return env
