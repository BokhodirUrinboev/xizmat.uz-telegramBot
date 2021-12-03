import os
import platform
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admin_id = int(os.getenv("ADMIN_ID", default='730471485'))
GROUP_ID = int(os.getenv("GROUP_ID", default='-1001435867002'))
PGUSER = os.getenv("DB_USER")
PGPASSWORD = os.getenv("DB_PASS")
DATABASE = str(os.getenv("DB_NAME"))
DB_HOST = str(os.getenv("DB_HOST"))


REDIS_HOST = str(os.getenv("REDIS_HOST", default="localhost"))
REDIS_PORT = int(os.getenv("REDIS_PORT", default=6379))
REDIS_DB_FSM = int(os.getenv("REDIS_DB_FSM", default=0))
REDIS_DB_JOBSTORE = int(os.getenv("REDIS_DB_JOBSTORE", default=1))
ip = os.getenv("ip")
host = "localhost"
admins = [
    admin_id
]
I18N_DOMAIN = 'suv_soz'
path = os.getcwd()
# webhook settings
WEBHOOK_HOST = str(os.getenv("DOMAIN_NAME_FOR_WEBHOOK"))
WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = "0.0.0.0" # or ip
WEBAPP_PORT = os.getenv("WEBAPP_PORT", 3001)
BASE_DIR = os.path.abspath(os.path.join(path, os.curdir))
LOCALES_DIR = ''
if platform.system() == 'Windows':
    LOCALES_DIR = BASE_DIR + '\\locales'
elif platform.system() == 'Linux':
    LOCALES_DIR = BASE_DIR + '/locales'

# Database connection URI
POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{DB_HOST}/{DATABASE}"


aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
