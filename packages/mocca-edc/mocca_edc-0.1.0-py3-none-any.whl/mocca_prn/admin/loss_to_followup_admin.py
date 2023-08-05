from django.contrib import admin
from edc_ltfu.modeladmin_mixin import LossToFollowupModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from mocca_prn.models.loss_to_followup import LossToFollowupHiv, LossToFollowupNcd

from ..admin_site import mocca_prn_admin
from ..forms import LossToFollowupForm
from ..models import LossToFollowup


@admin.register(LossToFollowup, site=mocca_prn_admin)
class LossToFollowupAdmin(
    LossToFollowupModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = LossToFollowupForm


@admin.register(LossToFollowupHiv, site=mocca_prn_admin)
class LossToFollowupHivAdmin(
    LossToFollowupModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = LossToFollowupForm


@admin.register(LossToFollowupNcd, site=mocca_prn_admin)
class LossToFollowupNcdAdmin(
    LossToFollowupModelAdminMixin, ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = LossToFollowupForm
