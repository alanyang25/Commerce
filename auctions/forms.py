from django import forms
from .models import *

class ListingModelForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'category', 'description', 'current_price', 'image_link')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'current_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_link': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'title': 'Title',
            'category': 'Category',
            'image_link': 'Photo url',
            'description': 'Description',
            'current_price': 'Starting price'
        }

class BidModelForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid_price',)
        widgets = {
            'bid_price': forms.NumberInput(attrs={'class': 'form-control', 
                        'style': 'width:180px; margin:auto; box-shadow:none'}),
        }

        labels = {
            'bid_price':'',
        }

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_title', 'comment_content',)
        widgets = {
            'comment_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject',
                                                'style': 'box-shadow:none'}),
            'comment_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Your comment',
                                                'style':'margin-top:10px; box-shadow:none'}),
        }
        labels = {
            'comment_title':'',
            'comment_content':'',
        }
        