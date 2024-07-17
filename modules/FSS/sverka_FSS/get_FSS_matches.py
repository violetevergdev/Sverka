import os
import pandas as pd


def get_FSS_matches(c, folder_path):
    # Выполняем запрос
    query = c.execute('''select distinct *
from fss_base as f
join vib_fss_base as v on
     f.СНИЛС == v.npers
group by f.СНИЛС''')

    # Получаем DataFrame
    results = pd.DataFrame(query, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(folder_path, 'Обработанный список ФСС.xlsx')

    # Записываем данные
    writer = pd.ExcelWriter(out)
    results.to_excel(writer, index=False)

    writer.close()