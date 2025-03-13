import os
import pandas as pd
from settings.config import settings as conf

def get_CHAES_matches(c, xlsx_db, popay_db, wpr_db):
    # Обрабатываем popay на удаление ненужных дублей
    c.execute(f'''create table pn as
WITH ranked_data AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY NPERS
            ORDER BY
                CASE WHEN PW == 0 THEN 1
                    ELSE 2
                END,
                DPW DESC
        ) AS rn
    FROM {popay_db}
)
SELECT NPERS, RA, DPW, NVP, PW, SCHET
FROM ranked_data
WHERE rn=1
        ''')
    c.execute(f'CREATE INDEX snils_chaes_pn_ind ON {popay_db} (NPERS)')

    query = c.execute(f'''
    select x.*, pn.DPW, pn.PW ,pn.SCHET, w2.BIK, w2.NAME from {xlsx_db} as x
left join pn on x.СНИЛС == pn.NPERS
left join {wpr_db} as w1 on w1.KOD = pn.NVP and pn.RA == w1.RA
left join {wpr_db} as w2 on w2.KOD = w1.NUS and pn.RA == w2.RA
    ''')

    results = pd.DataFrame(query, columns=[col[0] for col in c.description])
    out = os.path.join(conf.out_path, 'Обработанный список [ЧАЭС].xlsx')

    writer = pd.ExcelWriter(out)
    results.to_excel(writer, index=False, sheet_name='Sheet1')

    # Ширина по содержимому
    worksheet = writer.sheets['Sheet1']
    for i, col in enumerate(results):
        max_length = max(results[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    writer.close()

