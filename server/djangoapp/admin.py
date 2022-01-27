from django.contrib import admin
from .models import CarMake, CarModel


class CarModelTabularAdmin(admin.StackedInline):
    model = CarModel
    extra = 3
    classes = ['collapse', 'wide']
class CarModelAdmin(admin.ModelAdmin):
    model = CarModel
    list_filter = ('carMake__name','car_type')
    search_fields= ['name', 'car_type', 'carMake__name']
class CarMakeAdmin(admin.ModelAdmin):
    model = CarMake
    inlines = [CarModelTabularAdmin]
    extra = 3
    classes = ['collapse', 'wide']
    search_fields = ['name']
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
