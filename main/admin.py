from django.contrib import admin

# Register your models here.
from main.models import Quote
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'text',)

admin.site.register(Quote, QuoteAdmin)
