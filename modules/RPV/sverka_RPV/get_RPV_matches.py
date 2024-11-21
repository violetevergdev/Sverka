import os
import pandas as pd
from settings.config import settings as conf


def get_RPV_matches(c, xml_db, xlsx_db, man_db, adv8_db):
    # Выполняем запрос
    query = c.execute(f'''SELECT 
    x.*, p.*, adv.*,
    x."Сумма выплаты РФ" - p.Сумма_pfr as Разница_сумм,
    CASE
    WHEN x.Фамилия <> p.Фамилия_pfr THEN 'Фамилия'
    WHEN x.Имя <> p.Имя_pfr THEN 'Имя'
    WHEN x.Отчество IS NULL AND p.Отчество_pfr IS NOT NULL THEN 'Отчество'
    WHEN x.Отчество IS NOT NULL AND p.Отчество_pfr IS NULL THEN 'Отчество'
    WHEN x.Отчество <> p.Отчество_pfr THEN 'Отчество'
    ELSE '--'
END AS Расхождение,
    CASE
    WHEN n.СНИЛС = p.СНИЛС_pfr THEN n.pw
    ELSE 0
END AS 'Смерть'
FROM {xml_db} AS x
LEFT JOIN {xlsx_db} AS p ON (
    x.СНИЛС = p.СНИЛС_pfr OR
    (x.СНИЛС IS NULL AND x.Фамилия = p.Фамилия_pfr AND x.Имя == p.Имя_pfr AND x."Дата рождения" = p."Дата рождения_pfr")
    )
LEFT JOIN {man_db} AS n ON n.СНИЛС = p.СНИЛС_pfr
LEFT JOIN {adv8_db} AS adv ON p.СНИЛС_pfr = adv.СНИЛС
ORDER BY x.Фамилия''')

    # Забираем значение столбцов
    column_names = [col[0] for col in c.description]
    # Получаем DataFrame
    results = pd.DataFrame(query)
    # Устанавливаем выходной путь
    out = os.path.join(conf.out_path, 'Обработанный список РПВ.xlsx')
    # Выгружаем результат
    results.to_excel(out, header=column_names, index=False, engine='openpyxl')


