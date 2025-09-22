from django import forms
from .models import Land, LandImage, Inquiry

class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        fields = ['title', 'description', 'price', 'area', 'location', 'city', 
                  'state', 'pincode', 'land_type', 'category', 'latitude', 'longitude']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'area': forms.NumberInput(attrs={'step': '0.01'}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
        }

class LandImageForm(forms.ModelForm):
    class Meta:
        model = LandImage
        fields = ['image', 'is_primary']

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class LandSearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search by title, location, city...',
        'class': 'form-control'
    }))
    land_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Land.LAND_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Min Price', 'class': 'form-control'})
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Max Price', 'class': 'form-control'})
    )
    min_area = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Min Area (sq ft)', 'class': 'form-control'})
    )
    max_area = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Max Area (sq ft)', 'class': 'form-control'})
    )