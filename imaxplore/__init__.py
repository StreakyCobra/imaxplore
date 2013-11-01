# -*- coding: utf-8 -*-

import locale
import gettext
from imaxplore.Core.Configuration import conf

current_locale, encoding = locale.getdefaultlocale()

app_name = conf('app_name')
locale_path = conf('locale_dir')
language = gettext.translation(app_name, locale_path, [current_locale])

language.install()
