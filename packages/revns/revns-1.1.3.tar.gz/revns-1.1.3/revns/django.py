from django.conf import settings
from revns import BaseNotification as PureBaseNotification, MobileNotification as PureMobileNotification, \
    EmailNotification as PureEmailNotification, TemplatedEmailNotification as PureTemplatedNotification, \
    SmsNotification as PureSmsNotification


class BaseNotification(PureBaseNotification):
    def __init__(self, *args, **kwargs):
        kwargs['api_key'] = settings.CLIENT_SECRET
        kwargs['client_id'] = settings.CLIENT_ID
        stage = getattr(settings, 'STAGE')
        if stage in ['prod', 'PROD']:
            kwargs['stage'] = 'PROD'
        elif stage in ['stg', 'STG']:
            kwargs['stage'] = 'STG'
        else:
            kwargs['stage'] = 'DEV'
        super().__init__(*args, **kwargs)


class MobileNotification(BaseNotification, PureMobileNotification):
    pass

class EmailNotification(BaseNotification, PureEmailNotification):
    pass


class TemplatedNotification(BaseNotification, PureTemplatedNotification):
    pass

class SmsNotification(BaseNotification, PureSmsNotification):
    pass
