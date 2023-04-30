from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    'components/common.py',
    'components/apps_and_middleware.py',
    'components/auth.py',
    'components/template.py',
    'components/database.py',
    'components/celery.py',
)
