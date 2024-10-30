<!-- @format -->

# Сверка [СВО]

   <img src="https://img.shields.io/badge/Version-1.0.3[pogreb]%20-blue" alt="Sverka">
   <img src="https://img.shields.io/badge/License-MIT-brightgreen" alt="License">

Программа для обработки данных формата XLSX и CSV.

## Содержание

- [Технологии](#технологии)
- [Использование](#использование)
  - [Настройка перед использованием](#настройка-перед-использованием)
- [Разработка](#разработка)
  - [Компиляция](#компиляция)

## Технологии

- [Python 3.8.7](https://www.python.org/downloads/release/python-387/)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [pandas](https://pandas.pydata.org/)

## Разработка

### Компиляция:

```sh
pyinstaller  --icon=ic.ico --onefile --windowed --name Сверка gui.py
```

```sh
pyinstaller  sverka.spec
```
