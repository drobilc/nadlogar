from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Uporabnik, DelovniList, Naloga

class DelovniListAdmin(admin.ModelAdmin):
    pass

class NalogaAdmin(admin.ModelAdmin):
    pass

admin.site.register(DelovniList, DelovniListAdmin)
admin.site.register(Naloga, NalogaAdmin)

admin.site.register(Uporabnik, UserAdmin)