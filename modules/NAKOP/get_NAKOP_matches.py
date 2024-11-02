import os
import pandas as pd
from settings.config import settings as conf


def get_NAKOP_matches(c, osfr_db, loc_db, man_db, popay_db, wpr_db):
    # Обрабатываем запрос на вывод тех, кто не попал в заявку
    q_dont_loc = c.execute(f"""SELECT l.* FROM {loc_db} as l
LEFT JOIN {osfr_db} as o ON l.СНИЛС = o.СНИЛС
WHERE o.ФИО IS NULL""")

    # Получаем DataFrame
    results_dl = pd.DataFrame(q_dont_loc, columns=[col[0] for col in c.description])

    # Обрабатываем входящий файл OSFR с MAN (на что затрачивается большее кол-во времени)
    c.execute(f'''CREATE TABLE res as SELECT *
                    FROM {osfr_db} as o
LEFT JOIN {man_db} as m on o.СНИЛС == m.MAN_NPERS
    ''')

    # Получаем все столбцы для таблицы f и исключаем MAN_ID, final_id
    c.execute("PRAGMA table_info(res)")
    columns_f = [row[1] for row in c.fetchall() if row[1] not in ['MAN_ID', 'final_id']]

    # Получаем все столбцы для таблицы p и исключаем POPAY_ID, POPAY_NVP, POPAY_VIDVPL
    c.execute(f"PRAGMA table_info({popay_db})")
    columns_p = [row[1] for row in c.fetchall() if row[1] not in ['POPAY_ID', 'POPAY_NVP', 'POPAY_VIDVPL']]

    columns_f_str = ', '.join([f'f."{col}"' for col in columns_f])
    columns_p_str = ', '.join([f'p."{col}"' for col in columns_p])

    # Выполняем запрос
    query = c.execute(f'''WITH filtered_man as (SELECT *,
                         CASE
                             WHEN COUNT(m.MAN_ID) OVER (PARTITION BY m.MAN_NPERS) > 1
                                 THEN (SELECT p.POPAY_ID FROM popay_base as p WHERE p.POPAY_ID = m.MAN_ID LIMIT 1)
                             ELSE m.MAN_ID
                             END AS final_id
                  FROM res as m)
SELECT
    {columns_f_str},
    {columns_p_str},
    w2.WPR_NAME,
CASE
    WHEN p.POPAY_AMOUNT IS NOT NULL
        THEN f."Сумма ЕВ" - p.POPAY_AMOUNT
    ElSE -1 * f."Сумма ЕВ"
    END AS "Разница сумм"
FROM
    filtered_man as f
left join {popay_db} as p on f.final_id = p.POPAY_ID
left join {wpr_db} as w1 on w1.WPR_KOD = p.POPAY_NVP and f.MAN_RA == w1.WPR_RA
left join {wpr_db} as w2 on w2.WPR_KOD = w1.WPR_NUS and f.MAN_RA == w2.WPR_RA
where final_id is not null 
''')

    # Получаем DataFrame
    results = pd.DataFrame(query, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(conf.out_path, 'Обработанный список [Накопительные].xlsx')

    # Записываем данные
    writer = pd.ExcelWriter(out)
    results.to_excel(writer, index=False, sheet_name='Sheet1')
    results_dl.to_excel(writer, index=False, sheet_name='Отс. в заявке')

    # Ширина по содержимому
    worksheet = writer.sheets['Sheet1']
    for i, col in enumerate(results):
        max_length = max(results[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    writer.close()
