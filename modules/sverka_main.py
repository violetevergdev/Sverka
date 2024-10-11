
from modules.Common.customization.db_connection import db_connection
from modules.pogreb.start_POG_sver import start_POG_sver


# Запуск скриптов в зависимости от типа сверки и условия выборки
def sver_main():
    in_path = './IN'

    try:
        # Подключение к БД
        conn, c = db_connection()

        err = start_POG_sver(in_path, conn, c)
        if err:
            return err

    except Exception as e:
        err = 'Ошибка сверки: ' + str(e)
        return err
    finally:
        conn.close()


if __name__ == '__main__':
    sver_main()
