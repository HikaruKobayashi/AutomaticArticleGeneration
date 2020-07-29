import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# WordPressのデータ
WP_URL = os.environ.get("WP_URL_Key")
WP_USERNAME = os.environ.get("WP_USERNAME_Key")
WP_PASSWORD = os.environ.get("WP_PASSWORD_Key")