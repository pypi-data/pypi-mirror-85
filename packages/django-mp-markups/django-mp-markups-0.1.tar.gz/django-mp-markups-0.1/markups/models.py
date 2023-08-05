
from django.db import models
from django.utils.translation import ugettext_lazy as _

from manufacturers.signals import manufacturer_replaced


class Markup(models.Model):

    value = models.FloatField(_('Mark-up, %'))

    category = models.ForeignKey(
        'categories.Category',
        verbose_name=_('Category'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='markups'
    )

    manufacturer = models.ForeignKey(
        'manufacturers.Manufacturer',
        verbose_name=_('Manufacturer'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='markups'
    )

    def __str__(self):

        label = _('Product mark-up')

        if self.id:
            label += ' #{}'.format(self.id or '')

        return label

    @classmethod
    def replace_manufacturer(cls, sender, src_id, dst_id, **kwargs):
        cls.objects.filter(manufacturer=src_id).update(manufacturer_id=dst_id)

    class Meta:
        verbose_name = _('Product mark-up')
        verbose_name_plural = _('Products mark-ups')


manufacturer_replaced.connect(Markup.replace_manufacturer)


class MarkupField(models.ForeignKey):

    def __init__(
            self,
            to=Markup,
            verbose_name=_('Murkup'),
            related_name='products',
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            **kwargs):
        super().__init__(
            to=to,
            verbose_name=verbose_name,
            related_name=related_name,
            on_delete=on_delete,
            blank=blank,
            null=null,
            **kwargs)
