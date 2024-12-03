

def create_db(c, db_name, col_names):
    sql_col = ', '.join([f"'{col}'" for col in col_names])
    c.execute(f"""CREATE TABLE IF NOT EXISTS {db_name} ({sql_col})""")