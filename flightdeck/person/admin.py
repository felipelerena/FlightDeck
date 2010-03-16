from django.contrib import admin

from models import Profile, Limit

class ProfileAdmin(admin.ModelAdmin):
	pass
admin.site.register(Profile, ProfileAdmin)

class LimitAdmin(admin.ModelAdmin):
	pass
admin.site.register(Limit, LimitAdmin)
