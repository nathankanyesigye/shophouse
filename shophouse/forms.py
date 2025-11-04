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
        fields = ('Category', 'name', 'price', 'description', 'image', 'is_sale', 'sale_price')
        widgets = {
            'Category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter product description'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter sale price if on sale'}),
        }
        labels = {
            'Category': 'Product Category',
            'name': 'Product Name',
            'price': 'Regular Price',
            'description': 'Product Description',
            'image': 'Product Image',
            'is_sale': 'On Sale?',
            'sale_price': 'Sale Price'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make Category field required
        self.fields['Category'].empty_label = "Select a category"
        self.fields['Category'].required = True
        # Make image field required
        self.fields['image'].required = True
        # Initialize sale_price with 0
        self.fields['sale_price'].initial = 0

    def clean(self):
        cleaned_data = super().clean()
        is_sale = cleaned_data.get('is_sale')
        sale_price = cleaned_data.get('sale_price')
        price = cleaned_data.get('price')

        # Validate sale price if product is on sale
        if is_sale and sale_price is not None and price is not None:
            if sale_price >= price:
                self.add_error('sale_price', 'Sale price must be less than regular price')
            if sale_price <= 0:
                self.add_error('sale_price', 'Sale price must be greater than 0')

        # Set sale_price to 0 if not on sale
        if not is_sale:
            cleaned_data['sale_price'] = 0

        return cleaned_data