from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Book,Borrowing, Notification, supplier,Reaches,Order, Invoice, Video
from embed_video.admin import AdminVideoMixin


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'regNo','is_staff')


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(Borrowing)
admin.site.register(Notification)
admin.site.register(supplier)
admin.site.register(Reaches)
admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(Video, MyModelAdmin)