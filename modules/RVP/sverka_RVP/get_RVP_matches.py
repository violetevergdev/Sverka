import os
import pandas as pd


def get_RVP_matches(c, xml_db, xlsx_db, vib_db, out_path='OUT'):
    # Выполняем запрос
    query = c.execute(f'''SELECT 
    x.*, p.*,
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
    (x.СНИЛС IS NULL AND x.Фамилия = p.Фамилия_pfr AND x.Имя = p.Имя_pfr AND x."Дата рождения" = p."Дата рождения_pfr")
    )
LEFT JOIN {vib_db} AS n ON n.СНИЛС = p.СНИЛС_pfr
ORDER BY x.Фамилия''')

    # Забираем значение столбцов
    column_names = [col[0] for col in c.description]
    # Получаем DataFrame
    results = pd.DataFrame(query)
    # Устанавливаем выходной путь
    out = os.path.join(out_path, 'Обработанный список РВП.xlsx')
    # Выгружаем результат
    results.to_excel(out, header=column_names, index=False, engine='openpyxl')


