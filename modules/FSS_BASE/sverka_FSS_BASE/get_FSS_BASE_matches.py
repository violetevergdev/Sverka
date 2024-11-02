import os
import pandas as pd
from settings.config import settings as conf


def get_FSS_BASE_matches(c, fss_db, vib_db):
    # Выполняем запрос
    query = c.execute(f'''SELECT
    v.fa || ' ' || v.im || ' ' || v.ot AS ФИО_НВП,
    f.*, v.dpw, v.dsm, v.npers, v.ra, v.re
FROM {fss_db} AS f
JOIN {vib_db} AS v ON f.СНИЛС == v.npers
ORDER BY f.ФИО''')

    # Получаем DataFrame
    results = pd.DataFrame(query, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(conf.out_path, 'Обработанный список ФСС-БАЗА.xlsx')

    # Записываем данные
    writer = pd.ExcelWriter(out)
    results.to_excel(writer, index=False)

    writer.close()
