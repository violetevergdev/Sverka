import os
import pandas as pd


def get_MITS_matches(c, folder_path):
    # Выполняем запрос
    query_tutor = c.execute('''SELECT 
    *
FROM mits_base AS m
JOIN vib_msp_base AS v ON
    m."Дата смерти л-о" NOT LIKE '' and m."СНИЛС л-о" = v.СНИЛС
ORDER BY m."ФИО получателя"''')

    # Получаем DataFrame опекунов
    results_tutor = pd.DataFrame(query_tutor, columns=[col[0] for col in c.description])

    query_recipients = c.execute('''SELECT 
    *
FROM mits_base AS m
JOIN vib_msp_base AS v ON
    m."Дата смерти получателя" NOT LIKE '' and m."СНИЛС получателя" = v.СНИЛС
ORDER BY m."ФИО получателя"''')

    # Получаем DataFrame получателей
    results_recipients = pd.DataFrame(query_recipients, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(folder_path, 'Обработанный список МиЦ.xlsx')
    # Записываем данные
    writer = pd.ExcelWriter(out)
    results_tutor.to_excel(writer, index=False, sheet_name='Опекуны')
    results_recipients.to_excel(writer, index=False, sheet_name='Получатели')

    writer.close()
