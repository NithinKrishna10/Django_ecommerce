
from django import forms
from store.models import Product,Category,Brand,Variation
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        
class VariationsForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = '__all__'