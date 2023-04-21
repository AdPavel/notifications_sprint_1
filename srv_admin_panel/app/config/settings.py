import os
from pathlib import Path
from split_settings.tools import include

from dotenv import load_dotenv

load_dotenv()

include(
    'components/common.py',
    'components/apps_and_middleware.py',
    'components/auth.py',
    'components/template.py',
    'components/database.py',
)
