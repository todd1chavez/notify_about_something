import os

from dotenv import load_dotenv



# Подгружаем переменные окружения
dotenv_path = os.path.abspath(
    os.path.join(os.path.dirname( __file__ ), '.', '.env')
)

if os.path.exists(dotenv_path): load_dotenv(dotenv_path)
else: raise Exception('Не найден файл .env')


# Конфигурация для телеграм бота
TELEGRAM_ADMIN_ID: str = os.getenv('TELEGRAM_ADMIN_ID')
TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')

