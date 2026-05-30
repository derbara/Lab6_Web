# Импорт модуля для работы с операционной системой (пути, переменные окружения)
import os

# Секретный ключ для криптографии сессий и защиты данных
SECRET_KEY = 'secret-key'

# Конфигурация подключения к базе данных (SQLite или MySQL)
SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@std-mysql.ist.mospolytech.ru/db_name'
# Отключение отслеживания изменений объектов (улучшает производительность)
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Вывод SQL запросов в консоль для отладки
SQLALCHEMY_ECHO = True

# Путь к папке для сохранения загруженных изображений
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
