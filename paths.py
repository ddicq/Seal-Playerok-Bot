"""
Центральный модуль путей Seal Playerok Bot.

Код и ресурсы остаются в каталоге репозитория.
Изменяемые данные на Render хранятся на Persistent Disk:
SEAL_DATA_DIR=/var/data
"""
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.environ.get("SEAL_DATA_DIR", ROOT_DIR))

# Изменяемые данные — на постоянном диске Render.
BOT_SETTINGS_DIR = os.path.join(DATA_DIR, "bot_settings")
BOT_DATA_DIR = os.path.join(DATA_DIR, "bot_data")
ERROR_STATS_DIR = os.path.join(BOT_DATA_DIR, "error_stats")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
STORAGE_DIR = os.path.join(DATA_DIR, "storage")
CACHE_DIR = os.path.join(STORAGE_DIR, "cache")

# Ресурсы и плагины — в репозитории (только чтение на Render).
BOT_IMAGES_DIR = os.path.join(ROOT_DIR, "bot_images")
START_IMAGES_DIR = os.path.join(BOT_IMAGES_DIR, "start_images")
START_BANNER_IMAGE_FILE = os.path.join(START_IMAGES_DIR, "хелуин тюлень.png")
RANDOM_CUTE_IMAGES_DIR = os.path.join(BOT_IMAGES_DIR, "random_cute_images")
PLUGINS_DIR = os.path.join(ROOT_DIR, "plugins")

# Настройки.
CONFIG_FILE = os.path.join(BOT_SETTINGS_DIR, "config.json")
MESSAGES_FILE = os.path.join(BOT_SETTINGS_DIR, "messages.json")
CUSTOM_COMMANDS_FILE = os.path.join(BOT_SETTINGS_DIR, "custom_commands.json")
AUTO_DELIVERIES_FILE = os.path.join(BOT_SETTINGS_DIR, "auto_deliveries.json")
AUTO_RESTORE_ITEMS_FILE = os.path.join(BOT_SETTINGS_DIR, "auto_restore_items.json")
AUTO_RAISE_ITEMS_FILE = os.path.join(BOT_SETTINGS_DIR, "auto_raise_items.json")
AUTO_COMPLETE_ITEMS_FILE = os.path.join(BOT_SETTINGS_DIR, "auto_complete_items.json")
QUICK_REPLIES_FILE = os.path.join(BOT_SETTINGS_DIR, "quick_replies.json")
PROXY_LIST_FILE = os.path.join(BOT_SETTINGS_DIR, "proxy_list.json")

# Данные.
SALT_FILE = os.path.join(BOT_DATA_DIR, ".salt")
STATS_FILE = os.path.join(BOT_DATA_DIR, "stats.json")
DEALS_MONITOR_FILE = os.path.join(BOT_DATA_DIR, "deals_to_monitor.json")
INITIALIZED_USERS_FILE = os.path.join(BOT_DATA_DIR, "initialized_users.json")
AUTO_RAISE_ITEMS_TIMES_FILE = os.path.join(BOT_DATA_DIR, "auto_raise_items_times.json")
AUTO_REMINDER_DEALS_FILE = os.path.join(BOT_DATA_DIR, "auto_reminder_deals.json")
PLAYEROK_CONNECTION_HEALTH_FILE = os.path.join(BOT_DATA_DIR, "playerok_connection_health.json")
AUTO_DELIVERY_HISTORY_FILE = os.path.join(BOT_DATA_DIR, "auto_delivery_history.json")

LATEST_LOG_FILE = os.path.join(LOGS_DIR, "latest.log")
ANNOUNCEMENT_TAG_FILE = os.path.join(CACHE_DIR, "announcement_tag.txt")


def ensure_dirs():
    """Создаёт каталоги данных; не пытается создавать каталоги ресурсов в репозитории."""
    for directory in (
        BOT_SETTINGS_DIR,
        BOT_DATA_DIR,
        ERROR_STATS_DIR,
        LOGS_DIR,
        STORAGE_DIR,
        CACHE_DIR,
    ):
        os.makedirs(directory, exist_ok=True)


def get_path(*parts) -> str:
    """Возвращает путь к файлу относительно корня репозитория."""
    return os.path.join(ROOT_DIR, *parts)
