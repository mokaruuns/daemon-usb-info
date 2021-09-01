# Тестовое задание Стажер-разработчик

# Python/Go

## Тестовое задание Стажер-разработчик Python/Go

Необходимо написать демон, который при запуске будет собирать информацию о подключенных
USB устройствах, а далее в фоновом режиме отслеживать подключение новых устройств и
отключение существующих.

Актуальное состояние должно записываться в заданный в конфигурации файл в формате:
Bus ID, Device Address, Product, Manufacturer, Vendor ID, Product ID, Current State
(connected/disconnected)

При получении сигнала SIGUSR1 необходимо очищать файл от записей отключенных устройств.
Демон должен корректно останавливаться при получении сигнала SIGTERM или нажатии Ctrl-C.

Можно использовать библиотеки, нельзя использовать внешние утилиты.

## Дополнительное задание

Для отслеживания подключения и отключения устройств использовать не периодический опрос, а
механизм inotify.

## Требования к заданию

```
1. Демон будет тестироваться на Debian 10/Ubuntu 21.
2. Для Питона необходим requirements.txt
3. Для Go просим добавить собранный бинарник в репозиторий
4. Ответом на тестовое задание является ссылка на публичный репозиторий на github, где в
README.md вы должны описать метод запуска и ключи запуска демона (для Go полный
процесс сборки)
5. Не требуется предоставлять SysV Init скрипт или SystemD Unit.
```

