from django.contrib import admin
from django.utils import timezone
from .models import (
    RegisterBusiness, Product, Categories, Login, Profile,
    OrderItems, Customer, Order, Cart, CartItem
)

@admin.register(RegisterBusiness)
class RegisterBusinessAdmin(admin.ModelAdmin):
    list_display = ('name_of_business', 'owner', 'verification_status', 'registration_date', 'verification_date')
    list_filter = ('verification_status', 'type_of_business')
    search_fields = ('name_of_business', 'owner__username', 'email')
    actions = ['approve_businesses', 'reject_businesses']
    
    def approve_businesses(self, request, queryset):
        queryset.update(verification_status='approved', verification_date=timezone.now())
    approve_businesses.short_description = "Approve selected businesses"
    
    def reject_businesses(self, request, queryset):
        queryset.update(verification_status='rejected', verification_date=timezone.now())
    reject_businesses.short_description = "Reject selected businesses"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'Category', 'price', 'is_sale', 'created_at')
    list_filter = ('business__verification_status', 'Category', 'is_sale')
    search_fields = ('name', 'description', 'business__name_of_business')

# Register other models with default admin interface
admin.site.register(Categories)
admin.site.register(Login)
admin.site.register(Profile)
admin.site.register(OrderItems)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
