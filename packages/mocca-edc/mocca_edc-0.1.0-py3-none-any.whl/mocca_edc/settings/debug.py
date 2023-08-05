import os  # noqa
from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=103)
EDC_SITES_UAT_DOMAIN = False
DEBUG = True
ALLOWED_HOSTS = [
    "kojja.ug.mocca.clinicedc.org",  # 102 intervention
    "bukulula.ug.mocca.clinicedc.org",  # 106 control
    "bagamoyo.tz.mocca.clinicedc.org",  # 201
    "bugamba.ug.mocca.clinicedc.org",  # 101
    "kinoni.ug.mocca.clinicedc.org",  # 103
    "localhost",
]
# comment: comment out if using runserver and folders read from .env
# ETC_DIR = os.path.join(BASE_DIR, "tests", "etc")  # noqa
# KEY_PATH = os.path.join(ETC_DIR, "crypto_fields")  # noqa
# end comment

if os.path.exists(BASE_DIR) and not os.path.exists(KEY_PATH):  # noqa
    os.makedirs(KEY_PATH)
    AUTO_CREATE_KEYS = True
