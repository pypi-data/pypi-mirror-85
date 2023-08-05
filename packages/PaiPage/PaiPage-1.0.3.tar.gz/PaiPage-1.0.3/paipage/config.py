__author__ = 'AivanF'
__copyright__ = 'Copyright 2020, AivanF'
__contact__ = 'projects@aivanf.com'

import os
import sys
import importlib
import shutil
import re

from . import const
from .const import PluginInfo, PluginMeta
from .jinja2 import make_env

__all__ = [
    'config',
    'configure',
    'configure_final',
]


class Config(const.SettingObj):
    _serialise = [
        'site_name',
        # Default values that may be overriden by DB settings
        'language_default', 'language_available',
        'template_page_default', 'template_layout_default',
        'coded_plugin_enabled', 'plugins_meta',
        # Settings
        'plugin_paths', 'logger',
        # Generated values
        'plugins_installed',
        'template_page_list', 'template_layout_list', 'template_handlers', 'jinja2',
        'common_css', 'template_dirs', 'static_dirs',
    ]
    _repr = ['site_name']

    def __init__(self):
        for name in self._serialise:
            self.__dict__[name] = None
        self._init_done = True

    def get_plugin_meta_plain(self):
        return [
            plugin_meta.as_dict()
            for plugin_meta in self.plugins_meta
        ]


config = Config()


def configure(
    site_name,
    language_default,
    language_available,
    template_page_default='pg-pure',
    template_layout_default='lo-pure',
    plugin_paths=[],
    plugin_enabled=['simple'],
    logger=None,
):

    '''
        Basic setup
    '''
    assert isinstance(site_name, str) and len(site_name) > 0
    config.site_name = site_name

    config.template_page_default = template_page_default
    config.template_layout_default = template_layout_default
    config.template_page_list = []
    config.template_layout_list = []

    for x in language_available:
        assert isinstance(x, const.Language)
    config.language_available = {x.code: x for x in language_available}
    assert isinstance(language_default, str)
    assert language_default in config.language_available
    config.language_default = language_default

    config.plugin_paths = plugin_paths
    config.coded_plugin_enabled = plugin_enabled

    if logger is None:
        import logging
        logger = logging.getLogger('paipage')
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    config.logger = logger


def attr2attr(src, dst, src_name, dst_name=None):
    if dst_name is None:
        dst_name = src_name
    if hasattr(src, src_name):
        setattr(dst, dst_name, getattr(src, src_name))


def load_plugin_code(plugin_info):
    plugin_name = plugin_info.name
    plugin_dir = plugin_info.path
    code_file = os.path.join(plugin_dir, '__init__.py')
    if os.path.exists(code_file):
        module_name = f'pai_plugin_{plugin_name}'
        module = importlib.machinery.SourceFileLoader(
            module_name, code_file).load_module()
        attr2attr(module, plugin_info, 'template_handlers')
        attr2attr(module, plugin_info, '__title__', 'title')
        attr2attr(module, plugin_info, '__version__', 'version')
        attr2attr(module, plugin_info, '__license__', 'license')
        attr2attr(module, plugin_info, '__author__', 'author')
        attr2attr(module, plugin_info, '__contact__', 'contact')
        attr2attr(module, plugin_info, 'description', 'description')


def collect_plugins(search_dir):
    search_dir = os.path.join(search_dir, 'plugins')
    if not os.path.exists(search_dir):
        return
    for plugin_name in os.listdir(search_dir):
        plugin_dir = os.path.join(search_dir, plugin_name)
        if not os.path.isdir(plugin_dir):
            continue

        plugin_info = PluginInfo(plugin_name, plugin_dir)

        # Load list of templates
        location = os.path.join(plugin_dir, 'templates')
        if os.path.exists(location):
            for filename in os.listdir(location):
                match = re.findall(const.RE_PG_FILE, filename)
                if len(match) == 1:
                    plugin_info.template_page_list.append(match[0])
                match = re.findall(const.RE_LO_FILE, filename)
                if len(match) == 1:
                    plugin_info.template_layout_list.append(match[0])

        load_plugin_code(plugin_info)

        config.plugins_installed[plugin_name] = plugin_info


def enable_plugins():
    config.common_css = []
    config.template_dirs = []
    config.static_dirs = []
    config.template_handlers = {}

    def add_common_css(plugin_dir, plugin_name, filename):
        src = os.path.join(plugin_dir, 'static', filename)
        res = f'_pai-{plugin_name}-{filename}'
        if os.path.exists(src):
            # TODO: copy to STATIC_ROOT if not DEBUG
            shutil.copyfile(src, os.path.join(plugin_dir, 'static', res))
            config.common_css.append(res)

    for plugins_meta in config.plugins_meta:
        if not plugins_meta.enabled:
            continue
        plugin_name = plugins_meta.name
        if plugin_name not in config.plugins_installed:
            raise ValueError(f'Missing enabled plugin "{plugin_name}"')
            continue
        plugin_info = config.plugins_installed[plugin_name]
        plugin_dir = plugin_info.path

        location = os.path.join(plugin_dir, 'templates')
        if os.path.exists(location):
            config.template_dirs.append(location)

        location = os.path.join(plugin_dir, 'static')
        if os.path.exists(location):
            config.static_dirs.append(location)

        add_common_css(plugin_dir, plugin_name, 'main.css')

        for name in plugin_info.template_page_list:
            if name not in config.template_page_list:
                config.template_page_list.append(name)

        for name in plugin_info.template_layout_list:
            if name not in config.template_layout_list:
                config.template_layout_list.append(name)

        config.template_handlers.update(plugin_info.template_handlers)


def configure_final():
    if const.is_migration():
        return

    from django.conf import settings
    from .models import GlobalSetting

    # # Plugins loading
    config.plugins_installed = {}
    for app in settings.INSTALLED_APPS:
        app_path = os.path.dirname(sys.modules[app].__file__)
        collect_plugins(app_path)
    for path in config.plugin_paths:
        collect_plugins(path)

    # # Plugins enabling
    saved_plugins = GlobalSetting.get_json('plugins_meta', [])
    if not saved_plugins:
        saved_plugins = [
            {'name': name, 'enabled': True}
            for name in config.coded_plugin_enabled
        ]

    if saved_plugins:
        saved_plugins = [
            PluginMeta(**kwargs) for kwargs in saved_plugins
        ]
    else:
        saved_plugins = [
            PluginMeta(name, True)
            for name in config.coded_plugin_enabled
        ]

    config.plugins_meta = []
    config.plugins_meta.append(PluginMeta('primary', True))
    config.plugins_meta.extend(saved_plugins)
    config.plugins_meta.extend(
        PluginMeta(name, False)
        for name in config.plugins_installed
    )
    config.plugins_meta = list(const.dedupe(config.plugins_meta, attr='name'))

    enable_plugins()

    config.jinja2 = make_env(template_dirs=config.template_dirs, config=config)

    # # Django settings
    settings.STATICFILES_DIRS.extend(config.static_dirs)
    settings.SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
