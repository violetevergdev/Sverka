import sys
import os
from dotenv import load_dotenv

# Функция для получения окружения, если мы в production, то берется из MEIPASS, в develop берется из configuration
def get_env(name):
    load_dotenv()
    env = os.getenv(name)

    if env is None:
        env_path = os.path.join(sys._MEIPASS, '.env')
        load_dotenv(env_path)

        env = os.getenv('ENV_FOR_DYNACONF')
    return env

# Получаем значение окружения
env = get_env('ENV_FOR_DYNACONF')

