from django.contrib import admin

# Register your models here.
import hello_world.models as m


admin.site.register(m.Users)
admin.site.register(m.User_Feedback)
admin.site.register(m.Offender)
admin.site.register(m.Authority)
admin.site.register(m.Trusted_Contact)
admin.site.register(m.Prediction)
admin.site.register(m.Message)
admin.site.register(m.Observable_Account)
admin.site.register(m.History)
# admin.site.register()
# admin.site.register()