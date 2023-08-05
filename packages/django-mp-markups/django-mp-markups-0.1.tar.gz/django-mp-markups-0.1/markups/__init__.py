
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MarkupsAppConfig(AppConfig):

    name = 'markups'
    verbose_name = _('Markups')


default_app_config = 'markups.MarkupsAppConfig'
