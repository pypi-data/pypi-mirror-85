#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from gettext import gettext as _
from logging import getLogger

from astersay.agi import Agi
from astersay.exceptions import AgiHangupError
from astersay.conf import settings
from astersay.dialog import Dialog


logger = getLogger(__name__)


class App:

    agi = None
    settings = None
    stream = None
    is_stopped = False

    def __init__(self, **agi_kwargs):
        logger_debug = logger.debug
        logger_debug(_('Инициализация приложения начата.'))
        # Сначала запускаем создание базовых каталогов и настроек.
        settings.configure()
        logger_debug(_('Включены настройки для каталога по-умолчанию.'))

        # Запускается чтение входных параметров CGI.
        agi = Agi(**agi_kwargs)
        logger_debug(_('Создан экземпляр AGI: %s'), agi)
        params = agi.params
        dialog_name = params.get('agi_arg_1')
        settings.set_dialog_name(dialog_name)
        logger_debug(_('Установлено имя диалога: %s'), settings.dialog_name)
        if 'agi_arg_2' in params and params['agi_arg_2']:
            settings.work_dir = wd = params['agi_arg_2']
            logger_debug(_('Устанавливается рабочий каталог: %s'), wd)
            # Снова запускаем создание каталогов и настроек (уже конкретных).
            settings.configure()
            logger_debug(_('Включены настройки для каталога %s.'), wd)

        self.agi = agi
        self.settings = settings
        logger_debug(_('Инициализация приложения выполнена.'))

    def start(self):
        assert self.agi
        assert self.settings
        assert self.stream
        dialog = Dialog(self.agi, self.settings, self.stream)
        dialog.run()

    def stop(self):
        self.is_stopped = True

    def run(self, stream=None):
        try:
            if not stream:
                stream = open(3, 'rb')
            self.stream = stream
            self.start()
            self.stop()
        except AgiHangupError as e:
            logger.info(str(e))
        except Exception as e:
            logger.error(str(e), exc_info=e)
