from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  =  models.CharField(max_length=50)
    user_name  =  models.CharField(max_length=50)
    email      = models.CharField(max_length=50)
    profile_picture = models.FileField()
    password = models.CharField(max_length=50)
    bio_data = models.TextField()

    
class Categories(models.Model):
    name = models.CharField(max_length=25,default="")
    
    def  __str__(self):
        return self.name

class RegisterBusiness(models.Model):
    VERIFICATION_STATUS = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name_of_business = models.CharField(max_length=120)
    type_of_business = models.CharField(max_length=120)
    email = models.EmailField(default="")
    address = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_STATUS,
        default='pending'
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name_of_business} ({self.get_verification_status_display()})"

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"
                            
class Product(models.Model):
    business = models.ForeignKey(RegisterBusiness, on_delete=models.CASCADE, null=True)
    Category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=25, default="")
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='shophouse/media/')
    is_sale = models.BooleanField(default=False)
    sale_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.business.name_of_business}"
        
    def clean(self):
        super().clean()
        if self.business and self.business.verification_status != 'approved':
            raise ValidationError("Products can only be added by verified businesses.")
    
class Customer(models.Model):
    UserName         = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.UserName 
    
    class Meta:
        ordering = ['UserName']

    

from datetime import date

    

class Login(models.Model):
    name      =  models.TextField()
    email = models.TextField()
    password       = models.TextField()
    
class  Order(models.Model):
    product= models.ForeignKey(Product ,on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    quantity =  models.PositiveIntegerField(default=1)
    address =  models.TextField(default="")
    orderDate  = models.DateField(auto_now_add= True)
    phone =  models.CharField(max_length=10, default="", blank=True)
    status = models.BooleanField(default=False) # False means not delivered yet, True means it is Delivered
    login =  models.ForeignKey(Login, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.orderDate)+ " "+ str(self.status) + " " + str(self.product)



     
class OrderItems(models.Model):
    pass

  #cart 
class Cart(models.Model):
    cart_id = models.CharField(max_length=1500,blank=True)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.name
    
    
 
    

    
    

# Create your models here.
