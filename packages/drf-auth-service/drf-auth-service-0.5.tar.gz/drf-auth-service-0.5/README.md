# -- Authorization service -- :closed_lock_with_key:

#### -> What is SSO (Single sign-on)? :lock_with_ink_pen:
**Single sign-on (SSO)** is an authentication scheme that allows a user to log in with
a single ID and password to any of several related, yet independent, software systems.


#### -> What is Authentication Service? :lock:
**An authentication service** is a mechanism, analogous to the use of passwords on time-sharing systems,
for the secure authentication of the identity of network clients by servers and vice versa,
without presuming the operating system integrity of either.


#### -> What features does this project have? :zap:
- [X] _Login by **register_type** value from user model_
- [X] _Register with confirmation flow managed by **RegisterBackend**_
- [X] _Reset Password with multiple options **phone/email** managed by register_type of user_
- [X] _Social authentication **~~Apple~~/Facebook/Google**_
- [X] _**Service** model approach for login and register_
- [X] _User **block/unblock/set-password/** feature based on secret token_


#### -> How does this package work and how to configure? :fire:
First of all this package can be used as **Stand-Alone Authentication Service** and as **Single Sign-on Service**.
It depends on your needs and can be configured with
`SSO = {WORK_MODE='stand_alone/multiple_services'}`.
This package have default settings for **register backends, html templates, sms backends**
and I will show below some examples how to override this settings with your own.

##### - User - :family:
User model is based on swappable settings from django model and to config your own model
of user you just have to give model to `AUTH_USER_MODEL = 'users.CustomUser'`

```
from sso.models import AbstractSSOUser

# Add phone number to user table
class CustomUser(AbstractSSOUser):
    phone_number = models.CharField(max_length=120)
```

#### - Backends - :package:
In case you want to use your own backends you will have to override 
```
SSO = {'BACKENDS': {"REGISTER_BACKENDS": [
            'apps.common.backends.CustomRegisterBackend',
        ]}`
```
```
from sso.common.backends import BaseBackend
from sso.common.managers import PhoneManager

from apps.users.models import CustomUser

class CustomRegisterBackend(BaseBackend):
    name = 'email'
    manager = PhoneManager

    def register_user(self):
        user = CustomUser.objects.create(username=self.request.data['username'], service=self.request.service,
                          register_type=self.name,
                          phone_number=self.request.data['phone_number'])
        return user
```
In order to work with **RegisterBacked** it's a must to inherit **BaseBackend** from sso package:
- name --> register_type name, based on this name received in register body will identify what register backend to use
- manager --> What manager **(PhoneManager/EmailManager)** to use for sending confirmation
 in case you have this functionality
 
#### - Sms Backends - :envelope:

At the moment we have only **TwilioBackend** which can be easily change with
```
"SMS_BACKEND": "apps.common.backends.CustomPhoneProvider"
```

```
from sso.common.sms_backends import TwilioBackend

class CustomPhoneProvider(TwilioBackend):
    def send_reset_password(self, user):
        self.send(message=self.get_message(self.template_reset, user), to_phone=user.phone_number)

    def send_confirmation(self, user):
        self.send(message=self.get_message(self.template_confirm, user), to_phone=user.phone_number)
``` 

#### - Email Backend - :mailbox_closed:

We have 3 options for email backends **(MailchimpBackend/SendInBlueBackend/HtmlTemplateBackend)** 
with default **HtmlTemplateBackend**, in order to change or add new backend just add to sso settings
```
"EMAIL_BACKEND": "sso.common.email_backends.SendInBlueBackend"
```

#### - Views/Serializers/Permissions -

Every view/serializer/permission can be change from sso settings and a good example how to do this
```SSO = {
    "SERIALIZERS": {
        "REGISTER_SERIALIZER": "apps.authentication.serializers.RegisterSerializer"
    }
}
```

```
class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    username = serializers.EmailField(required=True)
    register_type = serializers.HiddenField(default=RegisterType.EMAIL)

    def validate(self, attrs):
        if CustomUser.objects.filter(
                 username=attrs['username'], service=self.context['request'].service).exists():
            raise ValidationError({'username': f"User '{attrs['username']}' already exists"})

        return attrs
``` 

# - Available Settings - :mag_right:

| Setting | Description |
| ---     | --- |
|`WORK_MODE` | 
|`COOKIE_KEY` | cookie_key for use in login for multiple apps
|`DOMAIN_ADDRESS` | Domain address used in cookie
|`REFRESH_TOKEN_LIFETIME` | `timedelta(days=30)` used as jwt token refresh time
|`SENDINBLUE_RESET_PASS_TEMPLATE` | Template id for reset password from sendinblue
|`SENDINBLUE_CONFIRMATION_TEMPLATE` | Template id for confirmation from sendinblue
|`SEND_IN_BLUE_API_KEY` | SendInBlue setting
|`MAILCHIMP_RESET_PASS_TEMPLATE` | Template id for reset password from sendinblue
|`MAILCHIMP_CONFIRMATION_TEMPLATE` | Template id for confirmation from Mailchimp
|`MAILCHIMP_USERNAME` | Mailchimp setting
|`MAILCHIMP_SECRET_KEY` | Mailchimp setting
|`SEND_CONFIRMATION` | Boolean if you want to send confirmation on register
|`RESET_PASSWORD_EXPIRE` | token expiration hours for reset password and confirmation token
|`DEFAULT_FROM_NUMBER` | Twilio setting
|`SEND_RESET_PASSWORD_URL` | Base url where is append token `example.com/reset-password`
|`SEND_CONFIRMATION_URL` | Base url where is append token 'example.com/confirm-email'
|`TWILIO_ACCOUNT_SID` | Twilio setting
|`TWILIO_AUTH_TOKEN` | "Twilio setting
|`SMS_CONFIRMATION_MESSAGE` | Sms message on confirmation example: `Confirmation code {{code}}`
|`SMS_RESET_PASSWORD_MESSAGE` | Sms message on reset password example: "Reset password code {{code}}"
|`REGISTER_TYPES` | Available register types
|`EMAIL_HOST` | Emails smtp setting
|`EMAIL_PORT` | Emails smtp setting
|`EMAIL_USERNAME` | Emails smtp setting
|`EMAIL_PASSWORD` | Emails smtp setting
|`HTML_DEFAULT_FROM_EMAIL` | Emails smtp setting
|`EMAIL_USE_TLS` | Emails smtp setting
|`HTML_RESET_PASSWORD_SUBJECT` | Subject on reset password
|`HTML_CONFIRMATION_SUBJECT` | Subject on confirmation
|`HTML_EMAIL_RESET_TEMPLATE` | Path to reset password template if no one is defined, default is used
|`HTML_EMAIL_CONFIRM_TEMPLATE` | Path to confirmation template if no one is defined, default is used
|`SERIALIZERS` | Here is a Dict of serializers that you can override
|`VIEWS` | Here is a Dict of views that you can override
|`PERMISSIONS` | Here is a Dict of permissions that you can override
|`BACKENDS` | Here is a Dict of backends that you can override
|`ENUMS` | Here is a Dict of enums that you can override