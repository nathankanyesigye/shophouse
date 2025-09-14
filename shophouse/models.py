from django.db import models

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
                            
                               
class Product(models.Model):
    Category= models.ForeignKey(Categories,on_delete=models.CASCADE, default=1)
    name      =  models.CharField(max_length=25, default="")
    description = models.TextField()
    price       = models.IntegerField()
    image = models.ImageField(upload_to= 'shophouse/media/')
    is_sale = models.BooleanField(default=False)
    # sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    sale_price = models.IntegerField()
    def   __str__(self):
        return self.name
    
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

class RegisterBusiness(models.Model):
    name_of_business =  models.CharField(max_length=120)
    type_of_business =  models.CharField(max_length=120)
    email=  models.EmailField(default="")
    address = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    
    
    def __str__(self):
        return self.name_of_business

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"

    
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
