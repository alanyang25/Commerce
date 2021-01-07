from django.contrib import admin
from .models import *
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    def save_model(self, request, instance, form, change):
        user = request.user 
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.edited_by = user
        instance.save()
        form.save_m2m()
        return instance

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)

