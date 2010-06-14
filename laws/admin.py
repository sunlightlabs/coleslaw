from django.contrib import admin
from laws.models import Law

class LawAdmin(admin.ModelAdmin):
    list_filter = ["title"]
    list_display = ["title", "section", "psection", "num_references"]

admin.site.register(Law, LawAdmin)
