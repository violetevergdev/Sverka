import os
import pandas as pd

def get_POG_matches(c, vip_db, zayav_db, out_dir='OUT'):
    # Выполняем запрос
    query_base_on_zayav = c.execute(f'''SELECT DISTINCT *
FROM {zayav_db} AS z
LEFT JOIN {vip_db} AS v ON v."СНИЛС получателя" == z."СНИЛС заявителя"
WHERE v."ФИО получателя" IS NULL
''')

    # Получаем DataFrame базирующейся на заявлениях
    results_base_on_zayav = pd.DataFrame(query_base_on_zayav, columns=[col[0] for col in c.description])

    query_base_on_vip = c.execute(f'''SELECT DISTINCT *
    FROM {vip_db} AS v
    LEFT JOIN {zayav_db} AS z ON v."СНИЛС получателя" == z."СНИЛС заявителя"
    WHERE z."ФИО заявителя" IS NULL''')

    # Получаем DataFrame базирующейся на выплатах
    results_base_on_vip = pd.DataFrame(query_base_on_vip, columns=[col[0] for col in c.description])

    query_base_on_zayav_dyb = c.execute(f'''SELECT *, COUNT(z."ФИО заявителя") as "Количество записей"
FROM {zayav_db} AS z
GROUP BY z."ФИО заявителя"
HAVING COUNT(z."ФИО заявителя") > 1
    ''')

    # Получаем DataFrame базирующейся на заявлениях
    results_base_on_zayav_dyb = pd.DataFrame(query_base_on_zayav_dyb, columns=[col[0] for col in c.description])

    query_base_on_vip_dyb = c.execute(f'''SELECT *, COUNT(v."ФИО получателя") as "Количество записей"
FROM {vip_db} AS v
GROUP BY v."ФИО получателя"
HAVING COUNT(v."ФИО получателя") > 1
        ''')

    # Получаем DataFrame базирующейся на заявлениях
    results_base_on_vip_dyb = pd.DataFrame(query_base_on_vip_dyb, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(out_dir, 'Обработанный список [погребение].xlsx')

    # Записываем данные
    writer = pd.ExcelWriter(out)
    results_base_on_zayav.to_excel(writer, index=False, sheet_name='Заявления')
    results_base_on_vip.to_excel(writer, index=False, sheet_name='Выплата')
    results_base_on_zayav_dyb.to_excel(writer, index=False, sheet_name='Дубли Заявления')
    results_base_on_vip_dyb.to_excel(writer, index=False, sheet_name='Дубли Выплата')

    writer.close()