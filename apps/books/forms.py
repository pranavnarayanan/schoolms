from datetime import datetime
from django import forms
from apps.books.helper import BookHelper

class FORM_BookDetails(forms.Form) :
    book_name = forms.CharField (
        max_length=150,
        min_length=2,
        required=True
    )
    book_code = forms.CharField(
        max_length=100,
        required = True
    )
    book_volume = forms.IntegerField(
        required=False
    )
    book_author = forms.CharField(
        max_length=100,
        required=True,
        min_length=1
    )
    book_publisher = forms.CharField(
        max_length=100,
        min_length=1,
        required=True
    )
    book_year = forms.IntegerField(
        max_value=datetime.now().year,
        min_value=1700,
        required=False
    )
    book_category = forms.ChoiceField(
        choices = BookHelper().getBookCategoryList(),
        required = True
    )

    def clean(self):
        data = self.cleaned_data
        return data