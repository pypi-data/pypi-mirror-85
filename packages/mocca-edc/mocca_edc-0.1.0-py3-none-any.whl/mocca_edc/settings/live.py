from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
ALLOWED_HOSTS = [
    "bugamba.ug.mocca.clinicedc.org",
    "bukulula.ug.mocca.clinicedc.org",
    "buwambo.ug.mocca.clinicedc.org",
    "bwizibwera.ug.mocca.clinicedc.org",
    "kajjansi.ug.mocca.clinicedc.org",
    "kasangati.ug.mocca.clinicedc.org",
    "kasanje.ug.mocca.clinicedc.org",
    "kinoni.ug.mocca.clinicedc.org",
    "kojja.ug.mocca.clinicedc.org",
    "kyamulibwa.ug.mocca.clinicedc.org",
    "kyazanga.ug.mocca.clinicedc.org",
    "mpigi.ug.mocca.clinicedc.org",
    "muduma.ug.mocca.clinicedc.org",
    "namayumba.ug.mocca.clinicedc.org",
    "namulonge.ug.mocca.clinicedc.org",
    "ruhoko.ug.mocca.clinicedc.org",
    "sekiwunga.ug.mocca.clinicedc.org",
    "tikalu.ug.mocca.clinicedc.org",
    "bagamoyo.tz.mocca.clinicedc.org",
    "buguruni.tz.mocca.clinicedc.org",
    "rugambwa.tz.mocca.clinicedc.org",
    "consolata.tz.mocca.clinicedc.org",
    "kinondoni.tz.mocca.clinicedc.org",
    "kisarawe.tz.mocca.clinicedc.org",
    "magomeni.tz.mocca.clinicedc.org",
    "mbagala.tz.mocca.clinicedc.org",
    "mnazi.tz.mocca.clinicedc.org",
    "sinza.tz.mocca.clinicedc.org",
    "vincent.tz.mocca.clinicedc.org",
    "tambuka.tz.mocca.clinicedc.org",
    "tandale.tz.mocca.clinicedc.org",
    "tegeta.tz.mocca.clinicedc.org",
    "temeke.tz.mocca.clinicedc.org",
    "yombo.tz.mocca.clinicedc.org",
    "localhost",
]
