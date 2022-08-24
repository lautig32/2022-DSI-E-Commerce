from django.contrib import admin

from .models import *


class AddressUserProfileInline(admin.TabularInline):
    model = AddressUserProfile
    fields = ('postal_code', 'street', 'number_adress', )
    #'province', 'location', 
    readonly_fields = ()
    show_change_link = False
    extra = 0

    line_numbering = 0

    def line_number(self, obj):
        self.line_numbering +=1
        return self.line_numbering

    line_number.short_description = '#'


class UserProfileAdmin(admin.ModelAdmin):
    inlines = (AddressUserProfileInline, )
    list_display = ('last_name', 'first_name', 'document_number', 'email', 'profile_picture_short_tag', )
    search_fields = ['document_number', 'first_name', 'last_name', 'email', ]
    ordering = ('-is_active', 'last_name', 'first_name', )
    fields = ('username', ('email', 'password', ), ('last_name', 'first_name',), 'document_number', 'number_phone',
              ('profile_picture_medium_tag', 'profile_picture',), 
              ('is_active', 'is_staff', 'is_superuser', ), 'description')
    readonly_fields = ('profile_picture_medium_tag', )
    list_filter = ('is_active',)

    def save_model(self, request, obj, form, change):
        # obj.is_staff = obj.user_type != Person.SUBSCRIBER

        if 'document_number' in form.changed_data :
            obj.username = obj.cuil_cuim

        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(UserProfile, UserProfileAdmin)
