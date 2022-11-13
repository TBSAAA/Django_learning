import random

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django_redis import get_redis_connection

from utils.encrypt import md5
from web import models
from scripts import send_sms


class LoginForm(forms.Form):
    role = forms.ChoiceField(
        label='Role',
        choices=(("2", "user"), ("1", "admin")),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username",
        min_length=3,
        max_length=32,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "password"}, render_value=True),
        min_length=6,
        max_length=64,
        validators=[RegexValidator(r'^[0-9]+$', 'Password must be numeric.'), ],
    )

    def clean_password(self):
        return md5(self.cleaned_data['password'])

    def clean(self):
        user = self.cleaned_data.get('username')
        pwd = self.cleaned_data.get('password')
        if user and pwd:
            pass
        else:
            raise ValidationError("Overall error.")
        # 1. No return value, default self.cleaned_data
        # 2. Return value, self.cleaned_data=returned value
        # 3. Error, ValidationError -> self.add_error(None, e)

    def _post_clean(self):
        pass


class mobileLoginForm(forms.Form):
    role = forms.ChoiceField(
        choices=(("2", "user"), ("1", "admin")),
        widget=forms.Select(attrs={"class": "form-control"}),

    )
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "mobile"}),
        validators=[RegexValidator(r'^04\d{8}$', 'Wrong format of phone number'), ],

    )
    code = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "code"}),
        validators=[RegexValidator(r'^\d{4}$', 'Wrong format of code'), ],
    )

    def clean_code(self):
        mobile = self.cleaned_data.get('mobile')
        code = self.cleaned_data['code']
        if not mobile:
            return code

        conn = get_redis_connection("default")
        cache_code = conn.get(mobile)
        if not cache_code:
            raise ValidationError("Code expired.")
        if code != cache_code.decode('utf-8'):
            raise ValidationError("Code error.")
        return code

class MobileForm(forms.Form):
    role = forms.ChoiceField(
        label="role",
        choices=(("2", "customer"), ("1", "admin")),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    mobile = forms.CharField(
        label="mobile",
        validators=[RegexValidator(r'^04\d{8}$', 'Wrong format of phone number'), ]
    )

    def clean_mobile(self):
        role = self.cleaned_data.get('role')
        mobile = self.cleaned_data['mobile']
        if not role:
            return mobile
        # 1. make sure mobile exists
        if role == "1":
            exists = models.Administrator.objects.filter(active=1, mobile=mobile).exists()
        else:
            exists = models.Customer.objects.filter(active=1, mobile=mobile).exists()
        if not exists:
            raise ValidationError("Mobile number does not exist.")
        # 2. send msg and random verification code
        code = random.randint(1000, 9999)
        v_code = True
        # Because sending SMS requires payment, so wait until the project is completed before opening.
        # v_code = send_sms.send_sms(mobile, code)
        if v_code:
            # 3. save verification code to redis
            conn = get_redis_connection("default")
            conn.set(mobile, code, ex=60)
        else:
            raise ValidationError("Failed to send verification code.")
        print(code)
        return mobile
