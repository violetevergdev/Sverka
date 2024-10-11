import os
import pandas as pd

def get_POG_matches(c, vip_db, zayav_db, out_dir='OUT'):
    # Выполняем запрос
    query = c.execute(f'''SELECT *
FROM {vip_db} AS v
LEFT JOIN {zayav_db} AS f ON v."СНИЛС получателя" == f."СНИЛС заявителя"''')

    # Получаем DataFrame
    results = pd.DataFrame(query, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(out_dir, 'Обработанный список [погребение].xlsx')

    # Записываем данные
    writer = pd.ExcelWriter(out)
    results.to_excel(writer, index=False)

    writer.close()