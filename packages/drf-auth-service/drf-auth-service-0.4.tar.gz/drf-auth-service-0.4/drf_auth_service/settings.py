from datetime import timedelta

from django.apps import apps
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

from drf_auth_service.common.constants import SENDINBLUE_BACKEND_NAME, MAILCHIMP_BACKEND_NAME, TWILIO_BACKEND_NAME
from drf_auth_service.common.enums import RegisterType

auth_user = getattr(django_settings, 'AUTH_USER_MODEL', None) or 'drf_auth_service.SSOUser'
auth_module, user_model = auth_user.rsplit(".", 1)

User = apps.get_model(auth_module, user_model)
SSO_SETTINGS_NAMESPACE = "SSO"


class ObjDict(dict):
    def __getattribute__(self, item):
        try:
            value = self[item]
            if isinstance(value, str):
                value = import_string(value)
            elif isinstance(value, (list, tuple)):
                value = [import_string(val) if isinstance(val, str) else val for val in value]
            self[item] = value
        except KeyError:
            value = super(ObjDict, self).__getattribute__(item)

        return value

    def __set_name__(self, owner, name):
        self.__name__ = 'dict'


default_sso_settings = {
    "WORK_MODE": "single",
    "COOKIE_KEY": "single",
    "DOMAIN_ADDRESS": "drf_auth_service",
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "SENDINBLUE_RESET_PASS_TEMPLATE": '',
    "SENDINBLUE_CONFIRMATION_TEMPLATE": '',
    "SEND_IN_BLUE_API_KEY": '',
    "MAILCHIMP_RESET_PASS_TEMPLATE": '',
    "MAILCHIMP_CONFIRMATION_TEMPLATE": '',
    "MAILCHIMP_USERNAME": '',
    "MAILCHIMP_SECRET_KEY": '',
    "SEND_CONFIRMATION": True,
    "RESET_PASSWORD_EXPIRE": 24,
    "DEFAULT_FROM_NUMBER": '+12055370083',
    "SEND_RESET_PASSWORD_URL": 'example.com/reset-password',
    "SEND_CONFIRMATION_URL": 'example.com/confirm-email',
    "TWILIO_ACCOUNT_SID": "AC6b3fc1744aa63d35235a4fb01241e71a",
    "TWILIO_AUTH_TOKEN": "a3e0f68829427c69dbb94cb4e95ff638",
    "SMS_CONFIRMATION_MESSAGE": "Confirmation code {{code}}",
    "SMS_RESET_PASSWORD_MESSAGE": "Reset password code {{code}}",
    "REGISTER_TYPES": list(dict(RegisterType.choices).keys()),
    "EMAIL_HOST": "185.181.231.245",
    "EMAIL_PORT": 587,
    "EMAIL_USERNAME": "notification@hostmonitor.org",
    "EMAIL_PASSWORD": "qg3DAQ2NHX",
    "HTML_RESET_PASSWORD_SUBJECT": "Reset password receive",
    "HTML_DEFAULT_FROM_EMAIL": "info@ebs.com",
    "HTML_CONFIRMATION_SUBJECT": "Confirmation link",
    "EMAIL_USE_TLS": True,
    "HTML_EMAIL_RESET_TEMPLATE": "example/path/to/template",
    "HTML_EMAIL_CONFIRM_TEMPLATE": "example/path/to/template",
    "SERIALIZERS": ObjDict({
        "USER_RETURN_SERIALIZER": "drf_auth_service.users.serializers.ReturnUserBaseSerializer",
        "USER_SERIALIZER": "drf_auth_service.users.serializers.UserBaseSerializer",
        "BLOCK_USER_SERIALIZER": "drf_auth_service.users.serializers.BockUserSerializer",
        "USER_CONFIRM_SERIALIZER": "drf_auth_service.users.serializers.UserConfirmSerializer",
        "USER_IDENTIFIER": "drf_auth_service.users.serializers.UserIdentifierSerializer",
        "SOCIAL_RETURN_SERIALIZER": "drf_auth_service.socials.serializers.ReturnSocialSerializer",
        "SOCIAL_SERIALIZER": "drf_auth_service.socials.serializers.SocialSerializer",
        "SERVICE_SERIALIZER": "drf_auth_service.services.serializers.ServiceSerializer",
        "REGISTER_SERIALIZER": "drf_auth_service.authentication.serializers.RegisterSerializer",
        "REGISTER_RETURN_SERIALIZER": "drf_auth_service.authentication.serializers.ReturnRegisterSerializer",
        "SEND_RESET_PASSWORD_SERIALIZER": "drf_auth_service.authentication.serializers.SendResetPasswordSerializer",
        "RESET_PASSWORD_CONFIRMATION_SERIALIZER": "drf_auth_service.authentication.serializers.ResetPasswordConfirmSerializer",
        "RETURN_SUCCESS_SERIALIZER": "drf_auth_service.authentication.serializers.ReturnSuccessSerializer",
        "SET_PASSWORD_SERIALIZER": "drf_auth_service.users.serializers.UserSetPasswordSerializer",
    }),
    "VIEWS": ObjDict({
        "USER_VIEWS": "drf_auth_service.users.views.UserViewSet",
        "SERVICE_VIEWS": "drf_auth_service.services.views.ServiceViewSet",
        "AUTHENTICATION_VIEWS": "drf_auth_service.authentication.views.AuthenticationViewSet",
    }),
    "PERMISSIONS": ObjDict({
        "USER_PERMISSIONS": "drf_auth_service.users.permissions.USER_PERMISSIONS",
        "AUTHENTICATION_PERMISSIONS": "drf_auth_service.authentication.permissions.AUTHENTICATION_PERMISSIONS"
    }),
    "BACKENDS": ObjDict({
        "SMS_BACKEND": "drf_auth_service.common.sms_backends.TwilioBackend",
        "EMAIL_BACKEND": "drf_auth_service.common.email_backends.HtmlTemplateBackend",
        "REGISTER_BACKENDS": [
            'drf_auth_service.common.register_backends.EmailBackend',
            'drf_auth_service.common.register_backends.PhoneBackend',
            'drf_auth_service.common.register_backends.PhoneCodeBackend',
            'drf_auth_service.common.register_backends.NicknameBackend',
        ]
    }),
    "ENUMS": ObjDict({
        "REGISTER_TYPES": "drf_auth_service.common.enums.RegisterType",
        "SOCIAL_TYPES": "drf_auth_service.common.enums.SocialTypes",
    })
}

MAILCHIMP_REQUIRED_CONFIGS = ["MAILCHIMP_SECRET_KEY", "MAILCHIMP_RESET_PASS_TEMPLATE",
                              "MAILCHIMP_CONFIRMATION_TEMPLATE", "MAILCHIMP_SECRET_KEY"]

SENDINBLUE_REQUIRED_CONFIGS = ["SEND_IN_BLUE_API_KEY", "SENDINBLUE_RESET_PASS_TEMPLATE",
                               "SENDINBLUE_CONFIRMATION_TEMPLATE"]

HTML_EMAIL_REQUIRED_CONFIGS = ["HTML_RESET_PASSWORD_SUBJECT", "HTML_CONFIRMATION_SUBJECT", "EMAIL_HOST", "EMAIL_PORT",
                               "EMAIL_USERNAME", "EMAIL_PASSWORD", "EMAIL_USE_TLS", "HTML_EMAIL_RESET_TEMPLATE",
                               "HTML_EMAIL_CONFIRM_TEMPLATE", "HTML_DEFAULT_FROM_EMAIL"]

TWILIO_REQUIRED_CONFIGS = ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "DEFAULT_FROM_NUMBER"]
SETTINGS_TO_IMPORT_IN_DB = ["BACKENDS", "REGISTER_TYPES", "SEND_CONFIRMATION", "SMS_RESET_PASSWORD_MESSAGE",
                            "SMS_CONFIRMATION_MESSAGE", ] + SENDINBLUE_REQUIRED_CONFIGS \
                           + MAILCHIMP_REQUIRED_CONFIGS + HTML_EMAIL_REQUIRED_CONFIGS + TWILIO_REQUIRED_CONFIGS

PHONE_NUMBER_BACKEND_CASE = []


class Settings:
    def __init__(self, default_sso_settings, explicit_overriden_settings: dict = None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}

        overriden_settings = (
                getattr(django_settings, SSO_SETTINGS_NAMESPACE, {})
                or explicit_overriden_settings
        )

        self._load_default_sso_settings()
        self._override_settings(overriden_settings)
        self._validate_configs()
        try:
            self._init_settings_to_db()
        except:
            pass

    def _load_default_sso_settings(self):
        for setting_name, setting_value in default_sso_settings.items():
            if setting_name.isupper():
                setattr(self, setting_name, setting_value)

    def _override_settings(self, overriden_settings: dict):
        for setting_name, setting_value in overriden_settings.items():
            value = setting_value
            if isinstance(setting_value, dict):
                value = getattr(self, setting_name, {})
                value.update(ObjDict(setting_value))
            setattr(self, setting_name, value)

    def _init_settings_to_db(self):
        from drf_auth_service.models import Service, Config

        if getattr(self, 'WORK_MODE') == 'single' and Service.objects.count() == 0:
            service = Service.objects.create(name='Default configs')
            configs = []

            for key, val in self.__dict__.items():
                if key in SETTINGS_TO_IMPORT_IN_DB:
                    if type(val) == ObjDict or type(val) == dict:

                        for dict_key, dict_value in val.items():
                            if not type(dict_value) == list:
                                configs.append(Config(type='str', value=dict_value, key=dict_key,
                                                      service=service))
                    elif type(val) == list:
                        value = ''
                        for list_value in val:
                            value += f"{list_value},"

                        configs.append(Config(type='str', value=value.rstrip(','), key=key,
                                              service=service))
                    else:
                        configs.append(Config(type=type(val).__name__, value=str(val), key=key,
                                              service=service))

            Config.objects.bulk_create(configs)

    def _validate_configs(self):

        if import_string(getattr(self, 'BACKENDS')['EMAIL_BACKEND']).name == SENDINBLUE_BACKEND_NAME:
            for required_conf in SENDINBLUE_REQUIRED_CONFIGS:
                if getattr(self, required_conf, '') == '':
                    raise ImproperlyConfigured(f"{required_conf} is required for {SENDINBLUE_BACKEND_NAME}")

        if import_string(getattr(self, 'BACKENDS')['EMAIL_BACKEND']).name == MAILCHIMP_BACKEND_NAME:
            for required_conf in MAILCHIMP_REQUIRED_CONFIGS:
                if getattr(self, required_conf, '') == '':
                    raise ImproperlyConfigured(f"{required_conf} is required for {MAILCHIMP_BACKEND_NAME}")

        if import_string(getattr(self, 'BACKENDS')['SMS_BACKEND']).name == TWILIO_BACKEND_NAME:
            for required_conf in TWILIO_REQUIRED_CONFIGS:
                if getattr(self, required_conf, '') == '':
                    raise ImproperlyConfigured(f"{required_conf} is required for {TWILIO_BACKEND_NAME}")


class LazySettings(LazyObject):
    def _setup(self, explicit_overriden_settings=None):
        self._wrapped = Settings(default_sso_settings, explicit_overriden_settings)


settings = LazySettings()


def reload_sso_settings(*args, **kwargs):
    global settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == SSO_SETTINGS_NAMESPACE:
        settings._setup(explicit_overriden_settings=value)


setting_changed.connect(reload_sso_settings)
