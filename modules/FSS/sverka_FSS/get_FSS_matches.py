import os
import pandas as pd
from settings.config import settings as conf


def get_FSS_matches(c, fss_db, vib_db):
    # Выполняем запрос
    query = c.execute(f'''select distinct *
from {fss_db} as f
join {vib_db} as v on
     f.СНИЛС == v.npers
group by f.СНИЛС''')

    # Получаем DataFrame
    results = pd.DataFrame(query, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(conf.out_path, 'Обработанный список ФСС.xlsx')

    # Записываем данные
    writer = pd.ExcelWriter(out)
    results.to_excel(writer, index=False)

    worksheet = writer.sheets['Sheet1']
    for i, col in enumerate(results):
        max_length = max(results[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    writer.close()