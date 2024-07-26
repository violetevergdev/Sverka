import os
import pandas as pd


def get_MITS_matches(c, mits_db, vib_db, out_dir='OUT'):
    # Выполняем запрос
    query_tutor = c.execute(f'''SELECT 
    *
FROM {mits_db} AS m
JOIN {vib_db} AS v ON
    m."Дата смерти л-о" NOT LIKE '' and m."СНИЛС л-о" = v.СНИЛС
ORDER BY m."ФИО получателя"''')

    # Получаем DataFrame опекунов
    results_tutor = pd.DataFrame(query_tutor, columns=[col[0] for col in c.description])

    query_recipients = c.execute(f'''SELECT 
    *
FROM {mits_db} AS m
JOIN {vib_db} AS v ON
    m."Дата смерти получателя" NOT LIKE '' and m."СНИЛС получателя" = v.СНИЛС
ORDER BY m."ФИО получателя"''')

    # Получаем DataFrame получателей
    results_recipients = pd.DataFrame(query_recipients, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(out_dir, 'Обработанный список МиЦ.xlsx')
    # Записываем данные
    writer = pd.ExcelWriter(out)
    results_tutor.to_excel(writer, index=False, sheet_name='Опекуны')
    results_recipients.to_excel(writer, index=False, sheet_name='Получатели')

    writer.close()
