from django.contrib import admin
from .models import (
    TypeRisk,
    Profile,
    Stock,
    TypeStock,
    DeltaPrice,
    Package,
    Branch,
    Currency
)


admin.site.register(TypeRisk)
admin.site.register(Profile)
admin.site.register(Stock)
admin.site.register(TypeStock)
admin.site.register(DeltaPrice)
admin.site.register(Package)
admin.site.register(Branch)
admin.site.register(Currency)