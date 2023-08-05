__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import sys
import operator

from django.conf import settings


def is_migration():
	return 'makemigrations' in sys.argv or 'migrate' in sys.argv


class SettingObj:
	_serialise = []
	_repr = []
	_init_done = False

	def __init__(self):
		self._init_done = True

	def __setattr__(self, name, value):
		if self._init_done:
			if name not in self.__dict__:
				raise ValueError(f'Trying to set attr "{name}" for {self}')
		self.__dict__[name] = value

	def as_dict(self):
		return {key: getattr(self, key) for key in self._serialise}

	def __repr__(self):
		fileds = ', '.join(
			list(map(lambda key: f'{key}={self.__dict__[key]!r}', self._repr))
		)
		return f'{self.__class__.__name__}({fileds})'


class PluginInfo(SettingObj):
	_serialise = [
		'title', 'description', 'version', 'license', 'author', 'contact',
		'name', 'path', 'template_page_list', 'template_layout_list',
	]
	_repr = ['name', 'version']

	def __init__(self, plugin_name, plugin_dir):
		self.title = '_none_'
		self.description = '_none_'
		self.version = '_unknown_'
		self.license = '_unknown_'
		self.author = '_unknown_'
		self.contact = '_unknown_'
		self.name = plugin_name
		self.path = plugin_dir
		self.template_page_list = []
		self.template_layout_list = []
		self.template_handlers = {}
		self._init_done = True


class PluginMeta(SettingObj):
	_serialise = [
		'name', 'enabled',
	]
	_repr = ['name', 'enabled']

	def __init__(self, name, enabled=False):
		self.name = name
		self.enabled = enabled
		self._init_done = True


def dedupe(items, key=None, attr=None):
	if isinstance(key, str):
		key_getter = lambda x: x[key]
	elif key is None:
		if attr is not None:
			key_getter = operator.attrgetter(attr)
		else:
			key_getter = lambda x: x
	else:
		key_getter = key

	seen = set()
	for item in items:
		_key = key_getter(item)
		if _key not in seen:
			yield item
			seen.add(_key)


RE_PG_FILE = r'^(pg-.+)\.html$'
RE_LO_FILE = r'^(lo-.+)\.html$'
RE_PG_NAME = r'^(pg-.+)$'
RE_LO_NAME = r'^(lo-.+)$'

HTML_EXT = '.html'
PATH_INDEX = 'index'

LANG_NO = '_'

LANG_KEY = 'lang'

REQUIRED_STRINGS = (
	'name',  # lang name
	'languages',  # lang selection menu
	'error404',  # for bad URLs
	'errorNoLang',  # for pages with no text in current lang
	'errorNoLangOther',  # "check other languages"
	'back',  # "Back" link
)


class Language:
	def __init__(self, code, strings):
		self.code = code
		for key in REQUIRED_STRINGS:
			assert key in strings, f'No string "{key}" for lang "{code}"'
		self._strings = strings

	def as_dict(self):
		return self._strings

	def __setitem__(self, key, item):
		self._strings[key] = item

	def __getitem__(self, key):
		if key in self._strings:
			return self._strings[key]
		else:
			txt = f'Missing string "{key}"'
			if settings.DEBUG:
				raise KeyError(txt)
			else:
				return f'[ {txt} ]'


lang_en = Language(
	code='en',
	strings=dict(
		name='English',
		languages='Other languages',
		error404='Page not found',
		error500='Server error :(',
		errorNoLang='Not available in this language',
		errorNoLangOther='You can read the page in another language:',
		back='Back',
	),
)
lang_ru = Language(
	code='ru',
	strings=dict(
		name='Русский',
		languages='Другие языки',
		error404='Страница не найдена',
		error500='Ошибка сервера :(',
		errorNoLang='Недоступно на этом языке',
		errorNoLangOther='Вы можете посмотреть на другом языке:',
		back='Назад',
	),
)
