from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = True
ALLOWED_HOSTS = [
    "bugamba.uat.ug.mocca.clinicedc.org",
    "bukulula.uat.ug.mocca.clinicedc.org",
    "buwambo.uat.ug.mocca.clinicedc.org",
    "bwizibwera.uat.ug.mocca.clinicedc.org",
    "kajjansi.uat.ug.mocca.clinicedc.org",
    "kasangati.uat.ug.mocca.clinicedc.org",
    "kasanje.uat.ug.mocca.clinicedc.org",
    "kinoni.uat.ug.mocca.clinicedc.org",
    "kojja.uat.ug.mocca.clinicedc.org",
    "kyamulibwa.uat.ug.mocca.clinicedc.org",
    "kyazanga.uat.ug.mocca.clinicedc.org",
    "mpigi.uat.ug.mocca.clinicedc.org",
    "muduma.uat.ug.mocca.clinicedc.org",
    "namayumba.uat.ug.mocca.clinicedc.org",
    "namulonge.uat.ug.mocca.clinicedc.org",
    "ruhoko.uat.ug.mocca.clinicedc.org",
    "sekiwunga.uat.ug.mocca.clinicedc.org",
    "tikalu.uat.ug.mocca.clinicedc.org",
    "bagamoyo.uat.tz.mocca.clinicedc.org",
    "buguruni.uat.tz.mocca.clinicedc.org",
    "rugambwa.uat.tz.mocca.clinicedc.org",
    "consolata.uat.tz.mocca.clinicedc.org",
    "kinondoni.uat.tz.mocca.clinicedc.org",
    "kisarawe.uat.tz.mocca.clinicedc.org",
    "magomeni.uat.tz.mocca.clinicedc.org",
    "mbagala.uat.tz.mocca.clinicedc.org",
    "mnazi.uat.tz.mocca.clinicedc.org",
    "sinza.uat.tz.mocca.clinicedc.org",
    "vincent.uat.tz.mocca.clinicedc.org",
    "tambuka.uat.tz.mocca.clinicedc.org",
    "tandale.uat.tz.mocca.clinicedc.org",
    "tegeta.uat.tz.mocca.clinicedc.org",
    "temeke.uat.tz.mocca.clinicedc.org",
    "yombo.uat.tz.mocca.clinicedc.org",
    "localhost",
]
