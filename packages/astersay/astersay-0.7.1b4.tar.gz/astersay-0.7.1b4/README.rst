================
asterisk-dialogs
================

Набор приложений и Python-библиотека для работы Asterisk с различными
голосовыми моделями. Пакет устанавливает в систему 4 запускаемых приложения:

1. `astersay` - скрипт инициализации рабочего каталога.
2. `astersay-cgi` - CGI(AGI) для прямого указания в диалплане астериска.
3. `astersay-dev` - эмулятор AGI для разработки диалогов в интерактивном
   режиме без участия Asterisk.
4. `astersay-t2v` - консольная команда для конвертации "text-to-voice",
   возвращает на stdout путь к файлу голоса без его расширения.


Поддерживаемые бэкэнды
----------------------

Распознавание:

1. astersay.backends.yandex.YandexRecognizer
2. astersay.backends.vosk.VoskRecognizer

Синтез речи:

1. astersay.backends.yandex.YandexSynthesizer

По мере развития проекта эти списки будут увеличиваться.


Установка
---------

Для продакшн-серверов с Asterisk:

.. code-block:: shell

    pip3 install astersay

Для разработки диалогов и работы виртуального сервера DummyAsterisk необходим
PyAudio. Для его установки нужно предварительно в системе иметь dev-пакеты.

Для Debian-based:

.. code-block:: shell

    sudo apt install gcc portaudio19-dev
    pip3 install astersay[dev]

Для RedHat-based:

.. code-block:: shell

    sudo yum install gcc portaudio-devel
    pip3 install astersay[dev]


Настройка
---------

Проинициализируйте рабочий каталог от пользователя, запускающего Asterisk
на сервере или пользователя, которым будет вестись разработка диалогов.
Заметьте, что права на запись в этот каталог у пользователя должны быть.
Рабочий каталог по-умолчанию: `~/.config/astersay`.

.. code-block:: shell

    astersay
    # или
    astersay -w /var/custom-work-directory

Откройте редактором нужные JSON-файлы, который выдала программа.
Измените бэкэнды при необходимости в `main.json`, уровень логгирования в
`logging.json` и, например, заполните в `yandex.json` данные для авторизации
в сервисе:

* key_id
* service_account_id
* folder_id

Не забудьте создайть файл `~/.config/astersay/yandex_private.pem` с полученным
от Яндекса приватным ключём.

Затем проверьте готовность к работе. По-умолчанию использется синтезатор речи
Yandex, при условии, что он не был заменён в `main.json` другим.

.. code-block:: shell

    astersay --check

Вывод в консоли скажет о готовности.


Использование в диалплане
-------------------------

Для использования в диалплане для AGI получите полный путь к cgi-скрипту для
своей системы.

.. code-block:: shell

    which astersay-cgi

Полученный путь укажите в диалплане как AGI-программу. Для неё есть 2
необязательных параметра:

1. Название модели далога.
2. Путь к рабочему каталогу.


Консольная конвертация
----------------------

Без запуска Asterisk на любом компьютере возможна конвертация текста в
WAV-файлы. Для этого передайте команде "Text-To-Voice" текст одним из
следующих способов:

.. code-block:: shell

    astersay-t2v -t "Мой текст с пробелами."
    astersay-t2v -f text.txt
    astersay-t2v -f text.txt -w /var/custom-work-directory

В выводе будет путь к голосовому файлу без расширения.


Для вывода справки по параметрам запустите:

.. code-block:: shell

    astersay-t2v --help


Разработка диалогов
-------------------

Запуск эмуляции Asterisk позволяет разрабатывать диалоги без реального сервера.
Для этого запустите интерактивный режим командой:

.. code-block:: shell

    astersay-dev

Остановите программу клавишами: `Ctrl+C`.


Для вывода справки по параметрам запустите:

.. code-block:: shell

    astersay-dev --help

Найдите в рабочем каталоге файл `dialogs/default.json`, скопируйте его под
другим именем в тот же каталог, например в `dialogs/first_dialog.json` или
`dialogs/subdir/first_dialog.json`, и отредактируйте под свои нужды.

Запустите свой диалог так:

.. code-block:: shell

    astersay-dev -m first_dialog
    # или
    astersay-dev -m ~/.config/astersay/dialogs/first_dialog.json
    # или
    astersay-dev -m first_dialog -w /var/custom-work-directory
    # или
    astersay-dev -m subdir/first_dialog -w /var/custom-work-directory

Расширение '.json' можно не указывать.

Заметьте, что эмулятор отображает только ход процесса AGI, а не логгирует
ошибки и информацию из диалога. Для отображения лог-файлов используйте
консольную утилиту `tail`:

.. code-block:: shell

    tail -f /var/custom-work-directory/logs/*.log
