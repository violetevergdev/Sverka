import os
import pandas as pd
from settings.config import settings as conf

def get_OPEK_matches(c, opek_db, oid_db, id_db, vpl_db):
    # Выполняем запрос
    query_child = c.execute(f'''select *  
from {opek_db} as opek
join {oid_db} as oid on opek."СНИЛС ребенка" == oid.OID_MAN_NPERS
left join {id_db} as id on oid.OID_MAN_OID == id.ID_MAN_ID
where "СНИЛС взрослого" == ID_MAN_NPERS''')

    results_child = pd.DataFrame(query_child, columns=[col[0] for col in c.description])

    query_parent = c.execute(f'''select * 
from {opek_db} as opek
left join {vpl_db} as vpl on opek."СНИЛС взрослого" == vpl.PO_NPERS
''')

    results_parent = pd.DataFrame(query_parent, columns=[col[0] for col in c.description])

    # Устанавливаем выходной путь
    out = os.path.join(conf.out_path, 'Обработанный список ОПЕКУНЫ.xlsx')
    # Записываем данные
    writer = pd.ExcelWriter(out)
    results_child.to_excel(writer, index=False, sheet_name='Ребенок')
    results_parent.to_excel(writer, index=False, sheet_name='Родитель')

    # Ширина по содержимому
    worksheet = writer.sheets['Ребенок']
    for i, col in enumerate(results_child):
        max_length = max(results_child[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    worksheet = writer.sheets['Родитель']
    for i, col in enumerate(results_parent):
        max_length = max(results_parent[col].astype(str).map(len).max(), len(col)) + 1
        worksheet.set_column(i, i, max_length)

    writer.close()
