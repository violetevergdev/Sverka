# Сверка РВП
 
Программа для обработки данных из форматов XML, CSV и XLSX. Включает в себя два сценария: обработка файлов и выборка данных CSV для обработки. Реализована посредством интеграции SQLite и Selenuim.

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
    * [Настройка перед использованием](#настройка-перед-использованием)
    * [Использование](#использование)
- [Разработка](#разработка)
    * [Компиляция](#компиляция)
- [Содержание конфигурационных файлов](#содержание-конфигурационных-файлов)

## Технологии
- [Python 3.8.7](https://www.python.org/downloads/release/python-387/)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [selenium](https://pypi.org/project/selenium/)
- [pandas](https://pandas.pydata.org/)

## Использование

#### Настройка перед использованием

Для настройки необходимо создать в корне диска C: директорию ``For_programs``, в ней создать подкаталог ``soft`` и в нем разместить gecodriver.exe и директорию ``Mozilla Firefox`` (либо использовать уже установленный, для этого в ``modules.NVP.browser_init`` нужно удалить 8 строку, где задается путь до исполняемого файла браузера)

Также в ``For_programs`` необходимо иметь директорию ``VIB_Config`` в которой будут находиться конфигурационные файлы (для сервера по Москве и по области), структура документа указана в ``config.vib_conf.json``

### Использование

При запуске сценария ``Выбока`` программа выполнит задачу по Москве и по области.

При запуске сценария ``Обработка`` программа на вход принимает директорию, в которой находятся все необходимые для обработки файлы.

Структура этой директории должна выглядеть следующим образом:

```
РВП (dir) =>
    КАРТОТЕКА РАЗОВОЙ (dir)  =>
    НВП (dir) =>
    Spisok.XML
```
Ключевую роль играют названия директорий, если они будут называться иначе, то программа выдаст ошибку.

В директории НВП должны располагаться csv файлы выгруженные посредством запуска выборки. Картотека включает в себя xls и xlsx файлы.

После запуска обработки появиться информационное окно, после прочтения его нужно закрыть, иначе обработка так и не завершится.

Когда на экране появится сообщение о том, что обработка завершена, в корень каталога, где находятся все рабочие файлы, добавится Excel документ – Обработанный список РПВ. 

## Разработка

### Компиляция:
```sh
pyinstaller  --icon=ic.ico --onefile --windowed --name sverka gui.py
```

```sh
pyinstaller  sverka.spec
```

## Содержание конфигурационных файлов

При первом запуске программы вам необходимо указать свой логин и пароль от НВП, указывается он в разделе “user”:
```json
  "user": {
    "login": "",
    "password": ""
  }
```
В разделе "useful-btn" указаны все ID веб. элементов (кнопок), с которыми взаимодействует выборка

В разделе "vib-fields" указаны все ID check элементов полей выборок, которые в свою очередь подразделяются на подразделы database, table, field

Раздел "filling-data" включает в себя все ID веб. форм, в которые задаются необходимые нам значения, а также указаны сами значения. Он также подразделяется на подразделы. Например,

```json
"filling-data": {
    "dsm": {
      "dsm_type_select": "указывает на ID выпадающего меню",
      "dsm_type_option": "указывает ID необходимого значения в выпадающем списке(int)",
      "dsm_type_set_ot": "указывает на ID поля, в которое должно быть установлено значение",
      "dsm_type_set_ot_keys": "указывает на устанавливаемое значение и т.п.",
    },
}
```

