from django.contrib import admin
from .models import ProductName, ProductTestData, ProductTestList, TestName
# Register your models here.


admin.site.register(ProductName)
admin.site.register(ProductTestData)
admin.site.register(ProductTestList)
admin.site.register(TestName)

