from django.contrib import admin
from home.models import Foot1_Nav, Site_Profile, Slider, Banner,  Top_Nav

# Register your models here.

class Site_ProfileAdmin(admin.ModelAdmin):
    list_display = ['title','company','status']

class SliderAdmin(admin.ModelAdmin):
    list_display = ['name']

class BannerAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Site_Profile,Site_ProfileAdmin)
admin.site.register(Slider,SliderAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.register(Top_Nav)
admin.site.register(Foot1_Nav)
