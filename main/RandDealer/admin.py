from django.contrib import admin
from .models import *

admin.site.register(Cars)
admin.site.register(CarImage)
admin.site.register(EmailVerificationToken)
admin.site.register(UserProfile)
admin.site.register(NewsletterSub)