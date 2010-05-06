from django.contrib import admin

from models_old import Jet, JetVersion, Cap, CapVersion

class JetAdmin(admin.ModelAdmin):
	pass
admin.site.register(Jet, JetAdmin)


class JetVersionAdmin(admin.ModelAdmin):
	pass
admin.site.register(JetVersion, JetVersionAdmin)

class CapAdmin(admin.ModelAdmin):
	pass
admin.site.register(Cap, CapAdmin)


class CapVersionAdmin(admin.ModelAdmin):
	pass
admin.site.register(CapVersion, CapVersionAdmin)

