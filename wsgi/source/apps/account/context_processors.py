from django.conf import settings




def open_forget_password(context):
    return {'OPEN_FORGET_PASSWORD': settings.OPEN_FORGET_PASSWORD}


def open_register(context):
    return {'OPEN_REGISTER': settings.OPEN_REGISTER}
