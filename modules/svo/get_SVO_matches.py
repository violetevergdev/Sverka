import os
import pandas as pd

def get_SVO_matches(c, svo_db, pfr_db, out_dir='OUT'):
    # Выполняем запрос
    query = c.execute(f'''SELECT *
FROM {svo_db} AS svo
JOIN {pfr_db} AS pfr ON svo.СНИЛС == pfr.NPERS
''')

    # Получаем DataFrame базирующейся на заявлениях
    results = pd.DataFrame(query, columns=[col[0] for col in c.description])


    # Устанавливаем выходной путь
    out = os.path.join(out_dir, 'Обработанный список [СВО].xlsx')

    # Записываем данные
    writer = pd.ExcelWriter(out)
    results.to_excel(writer, index=False)

    writer.close()
