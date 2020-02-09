from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Investors)
admin.site.register(Funds)
admin.site.register(Commitments)
admin.site.register(FundingCalls)
admin.site.register(FundingCallsComposition)
