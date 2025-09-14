from django import forms
from .models import RegisterBusiness, Product
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
class BusinessRegistration(forms.ModelForm):
    class Meta:
        model = RegisterBusiness
        fields = ('name_of_business','type_of_business', 'email', 'phone_number', 'description',)
        
# class updateUserForm(UserChangeForm):
#     email = forms.EmailField(label="", widget=forms.TextInput) 
#     first_name = forms.CharField(label="", max_length=100)
#     last_name = forms.CharField(label="", max_length=100)

#     class Meta:
#         model = User
#         fields = ("Username", "first_name", "last_name" , "email")    
        
      
class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields= ( 'name','price', 'description','image','is_sale', 'sale_price',)
        widgets={
            # 'image': forms.ImageField(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'price': forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            # 'is_sale':forms.BooleanField(attrs={'class':'form-control'}),
        }