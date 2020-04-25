from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string
from .. import models


@receiver(post_save, sender=models.Survey)
def create_unicode_code(**kwargs):
    """
    {
    'signal': <django.db.models.signals.ModelSignal object at 0x00000244A68E1B38>,
    'sender': <class 'web.models.Survey'>, 'instance': <Survey: Survey object (2)>,
    'created': True,
    'update_fields': None,
    'raw':False,
    'using':
    'default'
    }
    """
    created = kwargs.get('created', False)
    if not created:
        return
    instance = kwargs.get('instance')
    count = instance.count
    codes = []
    while count:
        _code = get_random_string(8)
        if models.SurveyCode.objects.filter(unique_code=_code).exists():
            continue
        code = models.SurveyCode(unique_code=_code, survey=instance)
        codes.append(code)
        count -= 1
    # 批量创建 bulk_create
    models.SurveyCode.objects.bulk_create(codes)
    print('创建成功！')
