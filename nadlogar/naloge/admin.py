from django.contrib import admin
from .models import Test, Naloga

class TestAdmin(admin.ModelAdmin):
    pass

class NalogaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Test, TestAdmin)
admin.site.register(Naloga, NalogaAdmin)