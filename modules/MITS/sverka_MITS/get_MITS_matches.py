import os
import pandas as pd
from settings.config import settings as conf

def get_MITS_matches(c, mits_db, vib_db):
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

    query_mobil_by_recip = c.execute(f'''SELECT 
        *
    FROM {mits_db} AS m
    JOIN {vib_db} AS v ON
        m."Смерть мобил" NOT LIKE '' and m."СНИЛС получателя" = v.СНИЛС
    ORDER BY m."ФИО получателя"''')

    # Получаем DataFrame смерти мобил по получателям
    results_mobil_by_recip = pd.DataFrame(query_mobil_by_recip, columns=[col[0] for col in c.description])

    query_mobil_by_tutor = c.execute(f'''SELECT 
           *
       FROM {mits_db} AS m
       JOIN {vib_db} AS v ON
           m."Смерть мобил" NOT LIKE '' and m."СНИЛС л-о" = v.СНИЛС
       ORDER BY m."ФИО получателя"''')

    # Получаем DataFrame смерти мобил по получателям
    results_mobil_by_tutor = pd.DataFrame(query_mobil_by_tutor, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(conf.out_path, 'Обработанный список МиЦ.xlsx')
    # Записываем данные
    writer = pd.ExcelWriter(out)
    results_tutor.to_excel(writer, index=False, sheet_name='Опекуны')
    results_recipients.to_excel(writer, index=False, sheet_name='Получатели')
    results_mobil_by_tutor.to_excel(writer, index=False, sheet_name='Смерть мобил опекуны')
    results_mobil_by_recip.to_excel(writer, index=False, sheet_name='Смерть мобил получатели')



    # Ширина по содержимому
    worksheet = writer.sheets['Опекуны']
    for i, col in enumerate(results_tutor):
        max_length = max(results_tutor[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    worksheet = writer.sheets['Получатели']
    for i, col in enumerate(results_recipients):
        max_length = max(results_recipients[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    worksheet = writer.sheets['Смерть мобил опекуны']
    for i, col in enumerate(results_mobil_by_tutor):
        max_length = max(results_mobil_by_tutor[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    worksheet = writer.sheets['Смерть мобил получатели']
    for i, col in enumerate(results_mobil_by_recip):
        max_length = max(results_mobil_by_recip[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    writer.close()
