import os
import pandas as pd


def get_matches(c, out_path):
    # Выполняем запрос
    query = c.execute('''SELECT 
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
END AS 'Смерть',
    CASE
    WHEN n.СНИЛС = p.СНИЛС_pfr THEN n.Район
    ELSE 0
END AS 'Район'
FROM xml_base AS x
LEFT JOIN pfr_base AS p ON (
    x.СНИЛС = p.СНИЛС_pfr OR
    (x.СНИЛС IS NULL AND x.Фамилия = p.Фамилия_pfr AND x.Имя = p.Имя_pfr AND x."Дата рождения" = p."Дата рождения_pfr")
    )
LEFT JOIN nvp_base AS n ON n.СНИЛС = p.СНИЛС_pfr
ORDER BY x.Фамилия''')

    # Забираем значение столбцов
    column_names = [col[0] for col in c.description]
    # Получаем DataFrame
    results = pd.DataFrame(query)
    # Устанавливаем выходной путь
    out = os.path.join(out_path, 'Обработанный список РВП.xlsx')
    # Выгружаем результат
    results.to_excel(out, header=column_names, index=False, engine='openpyxl')


