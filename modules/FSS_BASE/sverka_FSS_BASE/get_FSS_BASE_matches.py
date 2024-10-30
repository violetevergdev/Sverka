import os
import pandas as pd

def get_FSS_BASE_matches(c, fss_db, vib_db, out_dir='OUT'):
    if os.getenv('ENV_FOR_DYNACONF') == 'test':
        out_dir = 'C:\Violet\DEV_PROJ\WORKING\Sverka\OUT'

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
    out = os.path.join(out_dir, 'Обработанный список ФСС-БАЗА.xlsx')

    # Записываем данные
    writer = pd.ExcelWriter(out)
    results.to_excel(writer, index=False)

    writer.close()
