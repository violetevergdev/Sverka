from typing import Any


def format_snils_with_fill_zero(unvalid_snils):
    """ Функция для приведения СНИЛС в привычный 14-ти символьный вид

    В том числе -
            - заполянет недостающие нули в начале
            - расставляет "тире" и "пробел" в необходимых местах
    """

    if unvalid_snils == "":
        return None

    snils_str = str(unvalid_snils)

    if '.' in snils_str:
        s = list(snils_str[:-2])
    else:
        s = list(snils_str)

    while len(s) != 11:
        s.insert(0, '0')

    s.insert(3, '-')
    s.insert(7, '-')
    s.insert(11, ' ')
    return "".join(s)

def format_date_from_dot_to_dash(date):
    """
    Функция преобразовывает дату из формата с точками в формат с "тире"
    :param date: 'dd.mm.yyyy'
    :return: 'dd-mm-yyyy'
    """
    if "-" in date or date == "":
        return date
    else:
        s = date.split('.')
        new_date = s[2] + '-' + s[1] + '-' + s[0]
        return new_date

def to_str_type(num: Any) -> str:
    """ Функция преобразовывает значение в тип str

    В том числе -
        - удаляет "." и сл. символы после преобразования от float
    """
    if type(num) == str:
        return num

    s = str(num)
    if '.' in s:
        return s.split('.')[0]
    return s