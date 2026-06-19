from django.contrib import admin
from .models import chaivarity, chaireview, store, chaicertificate

# Register your models here.
class chaiReviewInline(admin.TabularInline):
    model = chaireview
    extra = 2

class chaivarityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'date_added')
    inlines = [chaiReviewInline]

class storeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    filter_horizontal = ('chai_varities',)  

class chaicertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'chai')            

admin.site.register(chaivarity, chaivarityAdmin)
admin.site.register(chaireview)
admin.site.register(store, storeAdmin)
admin.site.register(chaicertificate, chaicertificateAdmin)
