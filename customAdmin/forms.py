
from django import forms
from accounts.models import Account
from store.models import Product,Category,Brand,Variation
from cart.models import Coupon
from django.contrib.auth.models import User
from PIL import Image
from .models import Categoryoffer,Productoffer

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        
class VariationsForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = '__all__'
        
 
class BrandForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(
        attrs={
            "class": "form-control"
        }
    ))
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
   
    
    class Meta:
        model = Brand
        fields = ('brand_name','image', 'x', 'y', 'width', 'height', )


    def save(self):
        photo = super(BrandForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.image.path)

        return photo
  
  
class CouponForm(forms.ModelForm):
    
    class Meta:
        model = Coupon
        fields = '__all__'
    
class ProductOfferForm(forms.ModelForm):
    
    class Meta:
        model = Productoffer
        fields = '__all__'
        

class CategoryOfferForm(forms.ModelForm):
    
    class Meta:
        model = Categoryoffer
        fields = '__all__'