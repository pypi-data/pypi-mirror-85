
from django.utils.translation import ugettext_lazy as _

SEX_MALE = 1
SEX_FEMALE = 2
SEX_BOTH = 3

SEX_CHOICES = (
    (SEX_MALE, _('Male')),
    (SEX_FEMALE, _('Female')),
    (SEX_BOTH, _('Both')),
)
