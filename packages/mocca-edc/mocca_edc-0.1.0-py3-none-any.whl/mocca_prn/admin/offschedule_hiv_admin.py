from django.contrib import admin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import mocca_prn_admin
from ..models import OffScheduleHiv
from .modeladmin_mixins import EndOfStudyModelAdminMixin


@admin.register(OffScheduleHiv, site=mocca_prn_admin)
class OffScheduleHivAdmin(EndOfStudyModelAdminMixin, SimpleHistoryAdmin):

    pass
