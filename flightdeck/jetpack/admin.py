from django.contrib import admin

from models import Jet, JetVersion, Cap, CapVersion

class JetAdmin(admin.ModelAdmin):
	pass
admin.site.register(Jet, JetAdmin)


class JetVersionAdmin(admin.ModelAdmin):
	pass
admin.site.register(JetVersion, JetVersionAdmin)

