from django.contrib import admin

from models import Jetpack, Version

class JetpackAdmin(admin.ModelAdmin):
	pass
admin.site.register(Jetpack, JetpackAdmin)


class VersionAdmin(admin.ModelAdmin):
	pass
admin.site.register(Version, VersionAdmin)

