from django import forms
from .models import CommentRating, Asset

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentRating
        fields = ['comment', 'rating']

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_name', 'description', 'images', 'category']

# class AssetUploadForm(forms.ModelForm):
#     images = forms.ImageField(required=True, error_messages={'invalid': ("Image files only.")}, widget=forms.FileInput)
#     class Meta:
#         model = Asset
#         fields = ('asset_name', 'description', 'city', 'state', 'country', 'profile_picture')

#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'