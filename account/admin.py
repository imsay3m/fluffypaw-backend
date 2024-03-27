from django.contrib import admin

from .models import UserAccount


# Register your models here.
class UserAccountModelAdmin(admin.ModelAdmin):
    list_display = ["user", "account_no", "first_name", "last_name", "balance", "image"]

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


admin.site.register(UserAccount, UserAccountModelAdmin)
