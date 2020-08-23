from django.contrib import admin

from account.models import User, OTP

admin.site.register([User, OTP])
